"""Orchestration (AGENT.md section 18): a fixed, loop-free pipeline.

Mechanism -> Strategist -> modality agents (only where relevant, in parallel)
-> merge -> Experimental Strategist (per hypothesis, parallel) -> Reviewer -> Dossier.
Every stage runs once; agent research loops are turn-capped in llm.py.
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, TypeVar

from pydantic import BaseModel

from . import prompts as P
from .schemas import (CandidateApproach, Conclusion, Dossier, DiseaseMechanism, ExperimentOutput,
                      Modality, ModalityOutput, StrategistOutput, TherapeuticApproach)

M = TypeVar("M", bound=BaseModel)

MODALITY_AGENTS = {
    Modality.SMALL_MOLECULE: (P.SMALL_MOLECULE, ["chembl_target_drugs", "opentargets_search", "clinicaltrials_search", "pubmed_search", "uniprot_protein"]),
    Modality.OLIGONUCLEOTIDE: (P.OLIGO, ["pubmed_search", "uniprot_protein", "clinicaltrials_search"]),
    Modality.RNA: (P.RNA, ["pubmed_search", "uniprot_protein", "clinicaltrials_search"]),
    Modality.PROTEIN: (P.PROTEIN, ["chembl_target_drugs", "uniprot_protein", "pubmed_search", "clinicaltrials_search"]),
}
BLOCKING = {Conclusion.INSUFFICIENT_EVIDENCE}


class Report(BaseModel):
    disease: str
    mechanism: DiseaseMechanism
    candidates: list[CandidateApproach] = []
    approaches: list[TherapeuticApproach] = []
    dossier: Dossier | None = None
    warnings: list[str] = []


def _dump(obj) -> str:
    if isinstance(obj, list):
        return json.dumps([o.model_dump(mode="json") for o in obj], indent=1)
    return obj.model_dump_json(indent=1)


class Pipeline:
    def __init__(self, runner, *, max_hypotheses: int = 5, workers: int = 4,
                 checkpoint_dir: Path | None = None, log: Callable[[str], None] = print):
        self.run_agent, self.max_h, self.workers, self.ckpt, self.log = runner, max_hypotheses, workers, checkpoint_dir, log

    def _stage(self, name: str, schema: type[M], fn: Callable[[], M]) -> M:
        """Run a stage, or reuse its checkpoint so reruns don't re-spend."""
        path = self.ckpt / f"{name}.json" if self.ckpt else None
        if path and path.exists():
            self.log(f"  (reusing checkpoint {name})")
            return schema.model_validate_json(path.read_text())
        out = fn()
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(out.model_dump_json(indent=2))
        return out

    def run(self, disease: str) -> Report:
        self.log("[1/6] Mechanism agent")
        mech = self._stage("1_mechanism", DiseaseMechanism, lambda: self.run_agent(
            P.MECHANISM, f"Disease: {disease}", DiseaseMechanism,
            ["monarch_search_disease", "monarch_disease_genes", "opentargets_search",
             "opentargets_disease_targets", "pubmed_search", "uniprot_protein"]))
        report = Report(disease=disease, mechanism=mech)
        warnings = report.warnings
        if mech.conclusion in BLOCKING:
            self.log(f"  stopping: {mech.conclusion.value} - {mech.conclusion_note}")
            report.dossier = self._review(report, early=mech.conclusion)
            return report

        self.log("[2/6] Therapeutic strategist")
        note = (f"\nNOTE: the mechanism is flagged {mech.conclusion.value}: {mech.conclusion_note}. Prefer hypotheses that are "
                "robust to this uncertainty or that directly resolve it.") if mech.conclusion != Conclusion.OK else ""
        strat = self._stage("2_strategist", StrategistOutput, lambda: self.run_agent(
            P.STRATEGIST, f"Disease mechanism:\n{_dump(mech)}\n{note}\nGenerate at most {self.max_h} hypotheses.",
            StrategistOutput, ["pubmed_search", "opentargets_disease_targets", "chembl_target_drugs"]))
        report.candidates = strat.candidates[: self.max_h]
        if not report.candidates:
            self.log(f"  no hypotheses: {strat.conclusion.value} - {strat.conclusion_note}")
            report.dossier = self._review(report, early=strat.conclusion if strat.conclusion != Conclusion.OK
                                          else Conclusion.INSUFFICIENT_EVIDENCE, note=strat.conclusion_note)
            return report

        self.log(f"[3/6] Modality agents ({len(report.candidates)} hypotheses)")
        report.approaches = self._modalities(report, warnings)

        self.log("[4/6] Experimental strategist")
        self._experiments(report, warnings)

        self.log("[5/6] Reviewer / synthesizer")
        report.dossier = self._review(report)
        self._apply_verdicts(report, warnings)
        self.log("[6/6] Done")
        return report

    # -- stage 3+4: route hypotheses only to relevant modality agents ---------
    def _modalities(self, report: Report, warnings: list[str]) -> list[TherapeuticApproach]:
        by_name = {c.name.casefold(): c for c in report.candidates}
        jobs = {}
        for mod in MODALITY_AGENTS:
            cands = [c for c in report.candidates if mod in c.plausible_modalities]
            if cands:
                jobs[mod] = cands

        def work(item):
            mod, cands = item
            system, tool_names = MODALITY_AGENTS[mod]
            task = (f"Disease mechanism:\n{_dump(report.mechanism)}\n\nHypotheses to assess for modality "
                    f"'{mod.value}':\n{_dump(cands)}")
            return mod, self._stage(f"3_{mod.value}", ModalityOutput,
                                    lambda: self.run_agent(system, task, ModalityOutput, tool_names))

        with ThreadPoolExecutor(self.workers) as ex:
            results = list(ex.map(work, jobs.items()))

        out: dict[tuple[str, Modality], TherapeuticApproach] = {}
        for mod, res in results:
            for a in res.assessments:
                cand = by_name.get(a.hypothesis_name.casefold())
                if cand is None:
                    warnings.append(f"{mod.value} agent returned unknown hypothesis '{a.hypothesis_name}'; dropped")
                    continue
                out[(cand.name, mod)] = TherapeuticApproach(
                    name=cand.name, biological_hypothesis=cand.biological_hypothesis,
                    target_or_process=cand.target_or_process, desired_perturbation=cand.desired_perturbation,
                    modality=mod, strategy=a.strategy, existing_agents=a.existing_agents,
                    disease_relevant_cells=a.disease_relevant_cells, delivery_feasibility=a.delivery_feasibility,
                    supporting_evidence=cand.evidence_for + a.supporting_evidence,
                    contradictory_evidence=cand.evidence_against + a.contradictory_evidence,
                    biggest_unknown=a.biggest_unknown or cand.key_biological_uncertainty,
                    biggest_failure_mode=a.biggest_failure_mode, conclusion=a.conclusion)
        # keep hypotheses together: order by candidate order, then modality
        order = {c.name: i for i, c in enumerate(report.candidates)}
        return sorted(out.values(), key=lambda t: (order[t.name], t.modality.value))

    def _experiments(self, report: Report, warnings: list[str]) -> None:
        names = list(dict.fromkeys(a.name for a in report.approaches))

        def work(name: str):
            group = [a for a in report.approaches if a.name == name]
            task = (f"Disease mechanism:\n{_dump(report.mechanism)}\n\nApproaches (one hypothesis, possibly several "
                    f"modalities):\n{_dump(group)}")
            slug = "".join(ch if ch.isalnum() else "_" for ch in name)[:40]
            return self._stage(f"4_exp_{slug}", ExperimentOutput,
                               lambda: self.run_agent(P.EXPERIMENTAL, task, ExperimentOutput, ["pubmed_search"]))

        with ThreadPoolExecutor(self.workers) as ex:
            outputs = list(ex.map(work, names))
        idx = {(a.name, a.modality): a for a in report.approaches}
        for res in outputs:
            for e in res.experiments:
                a = idx.get((e.hypothesis_name, e.modality))
                if a is None:
                    warnings.append(f"experiment for unknown approach '{e.hypothesis_name}/{e.modality.value}' dropped")
                    continue
                a.model_fitness, a.best_next_experiment = e.model_fitness, e.plan
                if e.conclusion != Conclusion.OK and a.conclusion == Conclusion.OK:
                    a.conclusion = e.conclusion
        for a in report.approaches:
            if a.best_next_experiment is None:
                warnings.append(f"no experimental plan returned for {a.name} [{a.modality.value}]")

    # -- stage 5 -------------------------------------------------------------
    def _review(self, report: Report, early: Conclusion | None = None, note: str = "") -> Dossier:
        task = f"Disease: {report.disease}\n\nDisease mechanism:\n{_dump(report.mechanism)}\n"
        if early:
            task += (f"\nThe pipeline stopped early with conclusion {early.value}. {note or report.mechanism.conclusion_note}\n"
                     "Return that conclusion, a short honest dossier, and what to learn next (e.g. what minimal "
                     "experiments or data would make planning possible). Do not invent therapeutic approaches.")
        else:
            task += (f"\nHypotheses:\n{_dump(report.candidates)}\n\nApproaches with delivery, models and experiments:\n"
                     f"{_dump(report.approaches)}\n\nReturn one review per approach.")
        return self._stage("5_dossier" if not early else "5_dossier_early", Dossier,
                           lambda: self.run_agent(P.REVIEWER, task, Dossier, ["pubmed_search"] if not early else []))

    def _apply_verdicts(self, report: Report, warnings: list[str]) -> None:
        idx = {(a.name.casefold(), a.modality): a for a in report.approaches}
        for r in report.dossier.reviews:
            a = idx.get((r.hypothesis_name.casefold(), r.modality))
            if a is None:
                warnings.append(f"review for unknown approach '{r.hypothesis_name}/{r.modality.value}'")
                continue
            a.verdict, a.verdict_rationale = r.verdict, r.rationale
        for a in report.approaches:
            if a.verdict is None:
                warnings.append(f"reviewer gave no verdict for {a.name} [{a.modality.value}]")
