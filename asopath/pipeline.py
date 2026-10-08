from __future__ import annotations

import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from . import prompts as P
from .exons import enumerate_skips
from .render import hard_to_read, main_answer, words
from .schemas import (ASODesignReport, Answer, Decision, DeliveryReport, MechanismSet, ProductReport, ProgramsReport, RNADefect)



def _compact(enum: dict, n: int = 16) -> str:
    rows = [f"  exons {o['skip']:>6} | {o['n_exons']} exons | {o['bp_removed']} bp | deletes aa {o['deleted_aa_range']} (-{o['aa_deleted']}) | "
            f"junction {o['junction']} | oligos {o['oligos_min_max']}" for o in enum["viable_in_frame_skips"][:n]]
    return (f"{enum['gene']} {enum['transcript']} ({enum['protein_aa']} aa). Target exon {enum['target_exon']}: {enum['target_exon_cds_len']} bp "
            f"(frame remainder {enum['target_exon_frame_mod3']}; skipping it alone {'IS' if enum['target_alone_in_frame'] else 'is NOT'} in frame).\n"
            f"Neighbouring CDS exon lengths (bp): {enum['exon_lengths']}\n"
            f"Viable in-frame contiguous skips containing the target, no premature stop, sorted by fewest exons then fewest aa deleted "
            f"({len(enum['viable_in_frame_skips'])} total, first {n} shown):\n" + "\n".join(rows) +
            f"\n{len(enum['rejected_skips'])} other contiguous blocks rejected (out of frame or premature stop).\n{enum['note']}")


class Pipeline:
    def __init__(self, runner, out: Path, fresh: bool = False, log=print):
        self.run, self.out, self.log = runner, out, log
        if fresh and out.exists():
            shutil.rmtree(out)
        (out / "stages").mkdir(parents=True, exist_ok=True)

    def _stage(self, name, schema, fn):
        f = self.out / "stages" / f"{name}.json"
        if f.exists():
            self.log(f"[{name}] reusing checkpoint")
            return schema.model_validate_json(f.read_text())
        self.log(f"[{name}] running")
        r = fn()
        f.write_text(r.model_dump_json(indent=1))
        return r

    def __call__(self, disease: str, gene: str, variant: str, transcript: str | None = None) -> dict:
        sysp = lambda p: p.replace("{today}", date.today().isoformat())
        case = f"Disease: {disease}\nGene: {gene}\nVariant: {variant}" + (f"\nTranscript: {transcript}" if transcript else "")

        rna = self._stage("1_rna_defect", RNADefect, lambda: self.run("rna_defect", sysp(P.RNA_DEFECT), case, RNADefect))

        self.log("[2_design_space] enumerating (Ensembl, deterministic)")
        enum = None
        if rna.target_exons:
            enum = enumerate_skips(gene, rna.target_exons[0], transcript=transcript)
            (self.out / "stages" / "2_design_space.json").write_text(json.dumps(enum, indent=1))
        space = _compact(enum) if enum else "No exon-based enumeration applicable."
        base = f"{case}\n\nRNA DEFECT:\n{rna.model_dump_json(indent=1)}\n\nDESIGN-SPACE ENUMERATION (computed from Ensembl):\n{space}"

        mech = self._stage("2b_mechanisms", MechanismSet, lambda: self.run("mechanisms", sysp(P.MECHANISMS), base, MechanismSet))
        base += "\n\nMECHANISM LIST (candidate ASO mechanisms for this lesion):\n" + mech.model_dump_json(indent=1)

        jobs = {
            "3_product": (ProductReport, P.PRODUCT, ["pubmed_search", "europepmc_search"]),
            "4_aso": (ASODesignReport, P.ASO, ["pubmed_search", "europepmc_search"]),
            "5_delivery": (DeliveryReport, P.DELIVERY, ["pubmed_search", "europepmc_search", "clinicaltrials_search"]),
            "6_programs": (ProgramsReport, P.PROGRAMS, ["clinicaltrials_search", "europepmc_search"]),
        }
        with ThreadPoolExecutor(4) as ex:
            futs = {k: ex.submit(self._stage, k, s, lambda k=k, s=s, p=p, t=t: self.run(k, sysp(p), base, s, t, web=True))
                    for k, (s, p, t) in jobs.items()}
            res = {k: f.result() for k, f in futs.items()}

        reports = "\n\n".join(f"=== {k} ===\n{v.model_dump_json(indent=1)}" for k, v in res.items())
        decision = self._stage("7_decision", Decision, lambda: self.run(
            "decision", sysp(P.DECISION), f"{base}\n\nRESEARCH REPORTS:\n{reports}", Decision))

        notes = f"{base}\n\nWORKING NOTES (judgment):\n{decision.model_dump_json(indent=1)}\n\nRESEARCH REPORTS:\n{reports}"
        answer = self._stage("8_answer", Answer, lambda: self.run("writer", sysp(P.WRITER), notes, Answer))

        bad = hard_to_read(answer)   # readability guard: bullets that are long or chain ideas with semicolons
        self.log(f"[main answer] {words(main_answer(answer))} words, {len(bad)} hard-to-read bullets")
        if bad:
            ins = "Hard-to-read bullets:\n" + "\n".join(f"- {b}" for b in bad)
            answer = self.run("editor", P.EDITOR, f"{ins}\n\nCURRENT ANSWER:\n{answer.model_dump_json(indent=1)}", Answer)
            (self.out / "stages" / "8_answer_edited.json").write_text(answer.model_dump_json(indent=1))
            self.log(f"[main answer] after edit: {words(main_answer(answer))} words, {len(hard_to_read(answer))} hard-to-read bullets")
        return {"rna": rna, "enum": enum, "mechanisms": mech, **res, "decision": decision, "answer": answer}
