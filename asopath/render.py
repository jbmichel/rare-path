"""Main answer (AGENT.md section 12 structure) and a separate evidence appendix."""
import re


def words(text: str) -> int:
    return len(re.findall(r"\S+", re.sub(r"[#*|`>-]", " ", text)))


def main_answer(d) -> str:
    e = d.experiment
    L = [f"**Verdict: {d.verdict}**", "", "## Recommendation", "", f"**LEAD — {d.recommendation_line}**", "", d.recommendation_text, "", "## Why this design", ""]
    L += [f"- {x}" for x in d.why_this_design]
    L += ["", "## Delivery", "", d.delivery, "", "## Backup", ""]
    L += [f"- **{b.concept}.** {b.one_sentence}" for b in d.backups]
    L += ["", "## Critical risk", "", d.critical_risk, "", "## First experiment", "",
          f"- **Model:** {e.payload_model}", f"- **Constructs:** {e.payload_constructs}", f"- **Primary readout:** {e.primary_readout}",
          f"- **Success:** {e.success}", f"- **Kill:** {e.kill}", f"- **Then, delivery:** {e.delivery_experiment}",
          "", "## Key precedents", ""]
    L += [f"- {p.entry}" for p in d.precedents]
    return "\n".join(L) + "\n"


def references(d) -> str:
    return "\n".join(f"- {p.entry} — {p.source}" for p in d.precedents) + "\n"


def evidence(case: str, r: dict) -> str:
    d = r["decision"]
    L = [f"# Evidence — {case}", "", "## Candidates considered", "| Role | Concept | Reason |", "|---|---|---|"]
    L += [f"| {c.role} | {c.concept} | {c.reason} |" for c in d.all_candidates]
    if r["enum"]:
        L += ["", "## Design space (computed)", "| Skip | Exons | bp | Deleted aa | Range |", "|---|---|---|---|---|"]
        L += [f"| {o['skip']} | {o['n_exons']} | {o['bp_removed']} | {o['aa_deleted']} | {o['deleted_aa_range']} |" for o in r["enum"]["viable_in_frame_skips"][:16]]
    L += ["", "## Products"]
    for p in r["3_product"].products:
        L += [f"**{p.skip}** ({p.judgment}) — {p.why}  \nNatural: {p.natural_human_equivalent}  \nDomains: {p.domain_consequence}  \nRescue: {p.rescue_evidence}", ""]
    L += [f"Ranking: {r['3_product'].ranking_rationale}", "", "## ASO design evidence"]
    for s in r["4_aso"].per_skip:
        L += [f"**{s.skip}**  \nPublished: {s.published_asos}  \nCoordinated: {s.coordinated_skipping}  \nLinked: {s.linked_or_multitarget}  \nAmenability: {s.amenability}", ""]
    L += [f"Non-transferable benchmarks: {r['4_aso'].benchmarks_not_transferable}", "", "Proposed designs:"] + [f"- {x}" for x in r["4_aso"].proposed_designs]
    L += ["", "## Delivery platforms"]
    for p in r["5_delivery"].platforms:
        L += [f"**{p.name}** — {p.architecture}  \nReach: {p.reaches_cell}  \nHuman PD: {p.human_pd}  \nDose: {p.dose_frequency}  \nTox: {p.toxicity}  \nAccess: {p.access}", ""]
    L += [f"Unconjugated baseline: {r['5_delivery'].naked_baseline}", "", f"Payload vs delivery: {r['5_delivery'].payload_vs_delivery}", "", "## Programs",
          "| Org | Program | Target | Delivery | Stage | Key result |", "|---|---|---|---|---|---|"]
    L += [f"| {p.organization} | {p.program} | {p.target} | {p.delivery} | {p.stage} | {p.key_result} |" for p in r["6_programs"].programs]
    return "\n".join(L) + "\n"
