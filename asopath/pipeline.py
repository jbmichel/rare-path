from __future__ import annotations

import json
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

from . import prompts as P
from .exons import enumerate_skips
from .render import main_answer, words
from .schemas import (ASODesignReport, Decision, DeliveryReport, ProductReport, ProgramsReport, RNADefect)

WORD_LIMIT = 700


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

        for attempt in range(2):   # AGENT.md section 12: 400-700 words, enforced here rather than hoped for
            n = words(main_answer(decision))
            self.log(f"[main answer] {n} words")
            if n <= WORD_LIMIT:
                break
            self.log("  over limit; editor pass")
            decision = self.run("editor", P.EDITOR.format(limit=WORD_LIMIT - 40),
                                f"Current word count: {n}.\n\n{decision.model_dump_json(indent=1)}", Decision)
            (self.out / "stages" / "7_decision_edited.json").write_text(decision.model_dump_json(indent=1))
        return {"rna": rna, "enum": enum, **res, "decision": decision}
