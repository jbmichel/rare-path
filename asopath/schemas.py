from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Goal = Literal["skip_exon", "include_exon", "skip_multiple_exons", "block_cryptic_splice", "degrade_transcript",
               "stabilize_transcript", "suppress_mutant_allele", "alter_polyadenylation", "other"]


class RNADefect(BaseModel):
    gene: str
    transcript: str = Field(description="Canonical/MANE transcript id if known, else ''")
    defect: str = Field(description="What the lesion does to RNA and protein, <=2 sentences")
    desired_rna_product: str
    goal: Goal
    target_exons: list[int] = Field(description="Canonical exon number(s) carrying the lesion; [] if not exon-based")
    tissues: list[str] = Field(description="Tissues and cell types that must be reached")


class Mechanism(BaseModel):
    name: str = Field(description="Short name of the ASO mechanism, e.g. 'skip exon 55', 'suppress a non-productive splicing event'")
    how_it_works: str = Field(description="One sentence: what the oligo binds and what it changes in the RNA")
    rna_product: str = Field(description="The RNA/protein outcome this mechanism would produce for this lesion")
    requires: str = Field(description="What must already be true or exist for this to work (e.g. a splice site, an event, an element)")
    alleles: Literal["both", "mutant only", "normal only", "depends"] = Field(description="Which allele(s) the oligo acts on")
    discovery_burden: Literal["target known", "target must be located", "unknown whether a target exists"]
    fit: Literal["strong", "possible", "poor", "not applicable"]
    why: str = Field(description="One sentence on the fit for this lesion")


class MechanismSet(BaseModel):
    mechanisms: list[Mechanism] = Field(min_length=2)
    exon_skipping_applies: bool = Field(description="True if exon skipping or inclusion is a candidate mechanism for this lesion")


class Finding(BaseModel):
    claim: str = Field(description="One specific sourced statement, <=30 words")
    source: str = Field(description="URL, PMID or NCT id actually retrieved")


class ProductEval(BaseModel):
    candidate: str = Field(description="The exon block or mechanism being evaluated")
    natural_human_equivalent: str = Field(description="Real deletions/carriers of this product and what is known of their phenotype; 'none found' if none")
    domain_consequence: str = Field(description="Which protein domains/repeats/binding sites are lost or fused, using the deleted amino-acid range; 'n/a' if the product is the unaltered protein")
    rescue_evidence: str = Field(description="Patient-cell, animal or clinical rescue of this product; 'none found' if none")
    judgment: Literal["likely functional", "plausible", "uncertain", "likely poor"]
    why: str = Field(description="One sentence")
    findings: list[Finding]


class ProductReport(BaseModel):
    products: list[ProductEval]
    ranking_rationale: str = Field(description="Which product is best and why, <=60 words")


class ASOEvidence(BaseModel):
    candidate: str = Field(description="The exon block or mechanism being evaluated")
    target_evidence: str = Field(description="For mechanisms that need a pre-existing event or element: whether it has been demonstrated, how much of the transcript uses it, and the source; "
                                             "if not found, the searches tried. 'n/a' for exon skipping of a known exon")
    published_asos: str = Field(description="ASOs/PMOs published against these exons, with names/sequences/ids; 'none found' if none")
    coordinated_skipping: str = Field(description="Exon-skipping blocks only: direct evidence that ONE oligo yields skipping of >1 exon in this block, with the source; "
                                                  "state which searches returned nothing if none found. 'not applicable' for other mechanisms")
    linked_or_multitarget: str = Field(description="Precedent for linked/dual-arm or multi-target oligos relevant to this block; 'none found' if none")
    amenability: str = Field(description="Target-specific amenability, e.g. endogenous skipping, splice-site strength, enhancer/silencer, exon definition, accessibility of the element")
    findings: list[Finding]


class ASODesignReport(BaseModel):
    per_skip: list[ASOEvidence]
    benchmarks_not_transferable: str = Field(
        description="Efficacy results from OTHER splice targets that a reader might wrongly use as expectations here, and why they do not transfer; '' if none")
    proposed_designs: list[str] = Field(description="Concrete ASO designs (mechanism, target region, architecture, oligo count), <=25 words each")


class Platform(BaseModel):
    name: str
    architecture: str = Field(description="Cargo/chemistry + targeting ligand or receptor")
    reaches_cell: str = Field(description="Does it reach the required cell type? Include other critical tissues e.g. heart")
    functional_activity: str
    human_pd: str = Field(description="Human pharmacodynamic data incl. numbers; 'none' if none")
    dose_frequency: str
    toxicity: str
    access: str = Field(description="Partnering/licensing/internal-development realism")
    findings: list[Finding]


class DeliveryReport(BaseModel):
    platforms: list[Platform]
    naked_baseline: str = Field(description="What unconjugated oligos achieve here, with doses, frequency and numbers")
    payload_vs_delivery: str = Field(description="Which observed efficacy numbers are driven by target amenability/sequence potency versus delivery; <=60 words")


class Program(BaseModel):
    organization: str
    program: str
    target: str
    delivery: str
    stage: str
    key_result: str
    changes_decision_because: str = Field(description="<=20 words")
    source: str


class ProgramsReport(BaseModel):
    programs: list[Program]
    as_of: str = Field(description="Date of the most recent disclosure found")


class Lead(BaseModel):
    therapeutic_product: str
    aso_design: str
    delivery_strategy: str
    reason_it_wins: str
    dominant_risk: str


class Backup(BaseModel):
    concept: str
    one_sentence: str


class Experiment(BaseModel):
    payload_model: str
    payload_constructs: str
    primary_readout: str
    success: str
    kill: str
    delivery_experiment: str = Field(description="The separate follow-on delivery test, one sentence")


class Precedent(BaseModel):
    entry: str = Field(description="One line, <=30 words, why it changes the decision")
    source: str


class Candidate(BaseModel):
    concept: str
    role: Literal["LEAD", "BACKUP", "WATCH", "REJECT"]
    reason: str


class Decision(BaseModel):
    recommendation_line: str = Field(description="One-line program: product + ASO design + delivery")
    recommendation_text: str = Field(description="2-3 sentences")
    why_this_design: list[str] = Field(max_length=3, description="Max 3 bullets, <=30 words each")
    delivery: str = Field(description="One paragraph, <=5 sentences")
    backups: list[Backup] = Field(max_length=2)
    critical_risk: str = Field(description="One paragraph, <=5 sentences")
    experiment: Experiment
    precedents: list[Precedent] = Field(max_length=5)
    lead: Lead
    all_candidates: list[Candidate] = Field(description="Every candidate considered with LEAD/BACKUP/WATCH/REJECT (goes to the evidence file, not the main answer)")
    verdict: Literal["BUILD", "TEST FIRST", "WAIT FOR PLATFORM", "DO NOT PURSUE"]


# ---- final prose, bullet form (AGENT.md section 12 structure) ----

class AnswerBackup(BaseModel):
    concept: str
    bullets: list[str] = Field(min_length=1, max_length=3, description="Plain bullets: what it is, and when it would become preferable to the lead")


class AnswerExperiment(BaseModel):
    model: list[str] = Field(min_length=1, max_length=3, description="What system, and why")
    constructs: list[str] = Field(min_length=1, max_length=3, description="What is compared")
    primary_readout: list[str] = Field(min_length=1, max_length=3, description="What measurement decides whether the payload works")
    success_criterion: list[str] = Field(min_length=1, max_length=3)
    kill_criterion: list[str] = Field(min_length=1, max_length=3)


class AnswerPrecedent(BaseModel):
    bullet: str = Field(description="What was demonstrated and why it changes this program; one plain sentence, rarely two")
    source: str


class Answer(BaseModel):
    verdict: Literal["BUILD", "TEST FIRST", "WAIT FOR PLATFORM", "DO NOT PURSUE"]
    lead_line: str = Field(description="One plain sentence describing the program")
    recommendation: list[str] = Field(min_length=2, max_length=5, description="Bullets: the product, how the ASO makes it, why it is preferred; background only if needed")
    why_this_design: list[str] = Field(min_length=1, max_length=3, description="Each bullet one argument plus its implication")
    delivery: list[str] = Field(min_length=2, max_length=6, description="Bullets: preferred platform, why, best precedent, main limitation, and the follow-on delivery test")
    backups: list[AnswerBackup] = Field(max_length=2)
    critical_risk: list[str] = Field(min_length=1, max_length=4, description="Bullets: the issue most likely to kill the program and why")
    first_experiment: AnswerExperiment
    key_precedents: list[AnswerPrecedent] = Field(max_length=5)
