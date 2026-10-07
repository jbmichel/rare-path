"""Render a Report as the six-section dossier (AGENT.md section 19)."""
from __future__ import annotations

from .pipeline import Report
from .schemas import Conclusion, Evidence, Stance


def _cell(s: str) -> str:
    return (s or "-").replace("|", "/").replace("\n", " ")


def _ev(e: Evidence) -> str:
    src = f" [{e.source}]" if e.source else ""
    return f"- **{e.kind.value}** ({e.stance.value}): {e.statement}{src}"


def render(r: Report) -> str:
    m, d = r.mechanism, r.dossier
    L: list[str] = [f"# Therapeutic development dossier: {r.disease}", ""]
    if d and d.conclusion != Conclusion.OK:
        L += [f"> **{d.conclusion.value}** - {d.conclusion_note}", ""]
    L += ["*Decision-support output from an automated multi-agent analysis. Claims are labelled EVIDENCE / INFERENCE / "
          "HYPOTHESIS. Not medical advice; replaces no experimental validation.*", ""]

    L += ["## 1. Disease mechanism", ""]
    if m.conclusion != Conclusion.OK:
        L += [f"**{m.conclusion.value}** - {m.conclusion_note}", ""]
    L += [f"**Causal defect:** {m.causal_defect}", "", f"**Molecular consequence:** {m.molecular_consequence}", "",
          f"**Key cell types:** {', '.join(m.key_cell_types)}", "",
          "**Key pathology:**", *[f"- {x}" for x in m.key_pathology], "",
          f"**Evidence strength:** {m.evidence_strength}", "",
          "**Major unknowns:**", *[f"- {x}" for x in m.major_unknowns], ""]
    if d:
        L += [d.disease_mechanism_summary, ""]
    if m.key_evidence:
        L += ["<details><summary>Mechanism evidence</summary>", "", *[_ev(e) for e in m.key_evidence], "", "</details>", ""]

    if not d or not r.approaches:
        if d:
            L += ["## 5. Critical gaps", "", *[f"- {x}" for x in d.critical_gaps], "",
                  "## 6. What should be done next", ""]
            L += _actions(d)
        return "\n".join(L).rstrip() + "\n"

    L += ["## 2. Therapeutic leverage points", "", *[f"- {x}" for x in d.leverage_points], ""]

    L += ["## 3. Therapeutic approaches", "", "| Approach | Verdict | Why it could work | Modality | Existing agent? | Delivery | Main risk |",
          "|---|---|---|---|---|---|---|"]
    rev = {(x.hypothesis_name.casefold(), x.modality): x for x in d.reviews}
    for a in r.approaches:
        x = rev.get((a.name.casefold(), a.modality))
        dl = a.delivery_feasibility
        L.append("| " + " | ".join(_cell(s) for s in [
            a.name, a.verdict.value if a.verdict else "-", x.why_it_could_work if x else a.biological_hypothesis,
            a.modality.value, "; ".join(a.existing_agents) or "none identified",
            f"{dl.target_cell}: {dl.expected_access}", a.biggest_failure_mode]) + " |")
    L += ["", "### Comparative judgment", "", d.comparative_judgment, ""]
    for a in r.approaches:
        L += [f"### {a.name} - {a.modality.value}" + (f" - {a.verdict.value}" if a.verdict else ""), "",
              f"*Hypothesis:* {a.biological_hypothesis}", "",
              f"*Target / process:* {a.target_or_process}; *desired perturbation:* {a.desired_perturbation}", "",
              f"*Strategy:* {a.strategy}", "", f"*Verdict rationale:* {a.verdict_rationale or '-'}", ""]
        if a.conclusion != Conclusion.OK:
            L += [f"**{a.conclusion.value}**", ""]
        dl = a.delivery_feasibility
        L += [f"*Delivery:* tissue {dl.target_tissue}; cell {dl.target_cell}; access {dl.expected_access}; "
              f"constraint: {dl.major_constraint}", "",
              f"*Biggest unknown:* {a.biggest_unknown}", ""]
        if a.model_fitness:
            f = a.model_fitness
            L += [f"*Model fitness ({f.fitness}):* {f.best_available_model}. Mechanism: {f.captures_relevant_mechanism} "
                  f"Cell type: {f.captures_relevant_cell_type} Phenotype: {f.measurable_phenotype} Limits: {f.important_limitations}", ""]
        if a.best_next_experiment:
            e = a.best_next_experiment
            L += [f"*Best next experiment:* {e.proposed_experiment} (model: {e.model}; readout: {e.primary_readout}).", "",
                  f"- Question: {e.critical_question}", f"- Supports if: {e.supportive_result}",
                  f"- Weakens/kills if: {e.negative_result}", f"- Decision enabled: {e.decision_enabled}", ""]
        L += ["<details><summary>Evidence</summary>", "", *[_ev(e) for e in a.supporting_evidence + a.contradictory_evidence], "",
              "</details>", ""]

    L += ["## 4. What is already known", "", *[f"- {x}" for x in d.what_is_known], "",
          "## 5. Critical gaps", "", *[f"- {x}" for x in d.critical_gaps], "",
          "## 6. What should be done next", ""]
    L += _actions(d)
    if r.warnings:
        L += ["", "## Pipeline warnings", "", *[f"- {w}" for w in r.warnings], ""]
    return "\n".join(L).rstrip() + "\n"


def _actions(d) -> list[str]:
    L = []
    for i, a in enumerate(d.next_actions, 1):
        L += [f"{i}. **{a.action}**", f"   - Answers: {a.question_answered}", f"   - Requires: {a.activity_required}",
              f"   - Supports if: {a.supports_if}", f"   - Weakens/kills if: {a.kills_if}"]
    L += ["", "**Do not fund yet:**", *[f"- {x}" for x in d.do_not_fund_yet]]
    return L
