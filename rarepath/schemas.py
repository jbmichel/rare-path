"""Pydantic models mirroring the YAML shapes in AGENT.md.

Kept deliberately small: the smallest representation that preserves the
therapeutic decision (AGENT.md section 3).
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EvidenceKind(str, Enum):
    EVIDENCE = "EVIDENCE"      # directly supported by a source
    INFERENCE = "INFERENCE"    # derived from available evidence
    HYPOTHESIS = "HYPOTHESIS"  # requires experimental validation


class Stance(str, Enum):
    SUPPORTIVE = "supportive"
    CONTRADICTORY = "contradictory"
    INCONCLUSIVE = "inconclusive"
    NOT_STUDIED = "not_studied"


class Evidence(BaseModel):
    statement: str
    kind: EvidenceKind
    stance: Stance = Stance.SUPPORTIVE
    source: str = Field(default="", description="PMID, NCT id, database record, URL; empty only for pure inference")


class Conclusion(str, Enum):
    """Useful failure outcomes (AGENT.md section 21)."""
    OK = "OK"
    MECHANISM_UNCERTAIN = "MECHANISM UNCERTAIN"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT EVIDENCE"
    NO_ADEQUATE_MODEL = "NO ADEQUATE MODEL"
    NO_PLAUSIBLE_DELIVERY_PATH = "NO PLAUSIBLE DELIVERY PATH"
    NO_EXISTING_AGENT = "NO EXISTING AGENT IDENTIFIED"
    NOT_TESTABLE_YET = "THERAPEUTIC HYPOTHESIS NOT TESTABLE YET"


class Verdict(str, Enum):
    PURSUE = "PURSUE"
    INVESTIGATE = "INVESTIGATE"
    LOW_PRIORITY = "LOW PRIORITY"
    REJECT = "REJECT"


class Modality(str, Enum):
    SMALL_MOLECULE = "small_molecule"   # includes repurposing
    OLIGONUCLEOTIDE = "oligonucleotide"
    RNA = "rna"                         # siRNA, mRNA, ...
    PROTEIN = "protein"                 # biologics


# --- Mechanism agent -------------------------------------------------------

class DiseaseMechanism(BaseModel):
    disease_name: str
    identifiers: list[str] = Field(default_factory=list, description="MONDO/OMIM/Orphanet ids")
    causal_defect: str
    molecular_consequence: str
    key_cell_types: list[str]
    key_pathology: list[str]
    evidence_strength: str = Field(description="strong | moderate | weak, with one-line justification")
    major_unknowns: list[str]
    key_evidence: list[Evidence] = Field(default_factory=list)
    conclusion: Conclusion = Conclusion.OK
    conclusion_note: str = ""


# --- Therapeutic strategist ------------------------------------------------

class CandidateApproach(BaseModel):
    name: str
    biological_hypothesis: str
    target_or_process: str
    desired_perturbation: str
    plausible_modalities: list[Modality]
    evidence_for: list[Evidence]
    evidence_against: list[Evidence]
    key_biological_uncertainty: str


class StrategistOutput(BaseModel):
    candidates: list[CandidateApproach]
    conclusion: Conclusion = Conclusion.OK
    conclusion_note: str = ""


# --- Modality agents -------------------------------------------------------

class DeliveryFeasibility(BaseModel):
    target_tissue: str
    target_cell: str
    expected_access: str
    major_constraint: str


class ModalityAssessment(BaseModel):
    """One modality's take on one hypothesis. Becomes a TherapeuticApproach."""
    hypothesis_name: str = Field(description="Must equal the CandidateApproach.name it addresses")
    modality: Modality
    strategy: str
    existing_agents: list[str] = Field(description="approved -> clinical -> tool compound; empty if none")
    disease_relevant_cells: list[str]
    delivery_feasibility: DeliveryFeasibility
    supporting_evidence: list[Evidence]
    contradictory_evidence: list[Evidence]
    biggest_unknown: str
    biggest_failure_mode: str
    conclusion: Conclusion = Conclusion.OK
    conclusion_note: str = ""


class ModalityOutput(BaseModel):
    assessments: list[ModalityAssessment]


# --- Experimental strategist -----------------------------------------------

class ModelFitness(BaseModel):
    best_available_model: str
    captures_relevant_mechanism: str
    captures_relevant_cell_type: str
    measurable_phenotype: str
    important_limitations: str
    fitness: str = Field(description="adequate | partial | inadequate | unknown")


class ExperimentalPlan(BaseModel):
    critical_question: str
    proposed_experiment: str
    model: str
    primary_readout: str
    supportive_result: str
    negative_result: str
    decision_enabled: str


class ExperimentFor(BaseModel):
    hypothesis_name: str
    modality: Modality
    model_fitness: ModelFitness
    plan: ExperimentalPlan
    conclusion: Conclusion = Conclusion.OK


class ExperimentOutput(BaseModel):
    experiments: list[ExperimentFor]


# --- Final object ----------------------------------------------------------

class TherapeuticApproach(BaseModel):
    """The main decision object (AGENT.md section 8)."""
    name: str
    biological_hypothesis: str
    target_or_process: str
    desired_perturbation: str
    modality: Modality
    strategy: str
    existing_agents: list[str]
    disease_relevant_cells: list[str]
    delivery_feasibility: DeliveryFeasibility
    supporting_evidence: list[Evidence]
    contradictory_evidence: list[Evidence]
    biggest_unknown: str
    biggest_failure_mode: str
    model_fitness: Optional[ModelFitness] = None
    best_next_experiment: Optional[ExperimentalPlan] = None
    conclusion: Conclusion = Conclusion.OK
    verdict: Optional[Verdict] = None
    verdict_rationale: str = ""


# --- Reviewer / synthesizer ------------------------------------------------

class ReviewedApproach(BaseModel):
    hypothesis_name: str
    modality: Modality
    verdict: Verdict
    why_it_could_work: str
    dominant_failure_mode: str
    experiment_reduces_uncertainty: bool
    rationale: str


class NextAction(BaseModel):
    action: str
    question_answered: str
    activity_required: str
    supports_if: str
    kills_if: str


class Dossier(BaseModel):
    """Six-section final dossier (AGENT.md section 19)."""
    disease_mechanism_summary: str
    leverage_points: list[str]
    reviews: list[ReviewedApproach]
    comparative_judgment: str
    what_is_known: list[str]
    critical_gaps: list[str]
    next_actions: list[NextAction]
    do_not_fund_yet: list[str]
    conclusion: Conclusion = Conclusion.OK
    conclusion_note: str = ""
