"""Main answer (AGENT.md section 12 structure) and a separate evidence appendix."""
def words(text: str) -> int:
    return len(text.split())   # plain whitespace count, same as `wc -w`


def _b(items, ind=""):
    return [f"{ind}- {x}" for x in items]


def main_answer(a) -> str:
    e = a.first_experiment
    L = [f"**Verdict: {a.verdict}**", "", "## Recommendation", "", f"**LEAD — {a.lead_line}**", ""] + _b(a.recommendation)
    L += ["", "## Why this design", ""] + _b(a.why_this_design)
    L += ["", "## Delivery", ""] + _b(a.delivery)
    L += ["", "## Backup", ""]
    for b in a.backups:
        L += [f"- **{b.concept}**"] + _b(b.bullets, "  ")
    L += ["", "## Critical risk", ""] + _b(a.critical_risk) + ["", "## First experiment", ""]
    for name, items in (("Model", e.model), ("Constructs", e.constructs), ("Primary readout", e.primary_readout),
                        ("Success criterion", e.success_criterion), ("Kill criterion", e.kill_criterion)):
        L += [f"- **{name}**"] + _b(items, "  ")
    L += ["", "## Key precedents", ""] + _b([p.bullet for p in a.key_precedents])
    return "\n".join(L) + "\n"


def bullets(a) -> list[str]:
    """Texts of all content bullets (not the bold group labels), for the readability check."""
    e = a.first_experiment
    out = list(a.recommendation) + list(a.why_this_design) + list(a.delivery) + list(a.critical_risk)
    for b in a.backups:
        out += b.bullets
    for items in (e.model, e.constructs, e.primary_readout, e.success_criterion, e.kill_criterion):
        out += items
    return out + [p.bullet for p in a.key_precedents]


def hard_to_read(a, max_words: int = 30) -> list[str]:
    return [b for b in bullets(a) if len(b.split()) > max_words or ";" in b]


def references(a) -> str:
    return "\n".join(f"- {p.source}" for p in a.key_precedents) + "\n"


def evidence(case: str, r: dict) -> str:
    d = r["decision"]
    L = [f"# Evidence — {case}", "", "## References for key precedents", references(r["answer"]), "## Candidates considered", "| Role | Concept | Reason |", "|---|---|---|"]
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
