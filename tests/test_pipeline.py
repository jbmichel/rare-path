"""Offline tests: the pipeline is exercised with a fake runner (no API calls)."""
from rarepath.pipeline import Pipeline
from rarepath.render import render
from rarepath.schemas import *


def ev(s="x", kind=EvidenceKind.EVIDENCE):
    return Evidence(statement=s, kind=kind, source="PMID:1")


DEL = DeliveryFeasibility(target_tissue="CNS", target_cell="neurons", expected_access="intrathecal", major_constraint="spread")
MECH = DiseaseMechanism(disease_name="D", causal_defect="LoF of X", molecular_consequence="Y accumulates",
                        key_cell_types=["neurons"], key_pathology=["Y"], evidence_strength="strong", major_unknowns=["rev"])


class Fake:
    def __init__(self, mech=MECH, cands=None):
        self.calls, self.mech = [], mech
        self.cands = cands if cands is not None else [
            CandidateApproach(name="Reduce Y", biological_hypothesis="h", target_or_process="Z", desired_perturbation="down",
                              plausible_modalities=[Modality.SMALL_MOLECULE, Modality.OLIGONUCLEOTIDE],
                              evidence_for=[ev()], evidence_against=[], key_biological_uncertainty="u")]

    def __call__(self, system, task, schema, tool_names=None):
        self.calls.append(schema.__name__)
        if schema is DiseaseMechanism:
            return self.mech
        if schema is StrategistOutput:
            return StrategistOutput(candidates=self.cands)
        if schema is ModalityOutput:
            mod = Modality.SMALL_MOLECULE if "'small_molecule'" in task else Modality.OLIGONUCLEOTIDE
            return ModalityOutput(assessments=[
                ModalityAssessment(hypothesis_name="reduce y", modality=mod, strategy="s", existing_agents=["DrugA"],
                                   disease_relevant_cells=["neurons"], delivery_feasibility=DEL, supporting_evidence=[ev()],
                                   contradictory_evidence=[], biggest_unknown="b", biggest_failure_mode="f"),
                ModalityAssessment(hypothesis_name="ghost", modality=mod, strategy="s", existing_agents=[],
                                   disease_relevant_cells=[], delivery_feasibility=DEL, supporting_evidence=[],
                                   contradictory_evidence=[], biggest_unknown="b", biggest_failure_mode="f")])
        if schema is ExperimentOutput:
            fit = ModelFitness(best_available_model="iPSC neurons", captures_relevant_mechanism="yes", captures_relevant_cell_type="yes",
                               measurable_phenotype="Y level", important_limitations="none", fitness="adequate")
            plan = ExperimentalPlan(critical_question="q", proposed_experiment="e", model="iPSC", primary_readout="Y",
                                    supportive_result="falls", negative_result="no change", decision_enabled="advance")
            return ExperimentOutput(experiments=[ExperimentFor(hypothesis_name="Reduce Y", modality=m, model_fitness=fit, plan=plan)
                                                 for m in Modality if f"'{m.value}'" in task or f'"{m.value}"' in task])
        if schema is Dossier:
            reviews = [ReviewedApproach(hypothesis_name="Reduce Y", modality=m, verdict=Verdict.INVESTIGATE, why_it_could_work="w",
                                        dominant_failure_mode="f", experiment_reduces_uncertainty=True, rationale="r")
                       for m in (Modality.SMALL_MOLECULE, Modality.OLIGONUCLEOTIDE)]
            return Dossier(disease_mechanism_summary="sum", leverage_points=["lp"], reviews=reviews, comparative_judgment="cj",
                           what_is_known=["k"], critical_gaps=["g"], do_not_fund_yet=["trial"],
                           next_actions=[NextAction(action="a", question_answered="q", activity_required="r", supports_if="s", kills_if="k")])
        raise AssertionError(schema)


def test_full_pipeline(tmp_path):
    f = Fake()
    r = Pipeline(f, checkpoint_dir=tmp_path, log=lambda s: None).run("D")
    assert [a.modality for a in r.approaches] == [Modality.OLIGONUCLEOTIDE, Modality.SMALL_MOLECULE]
    assert all(a.verdict == Verdict.INVESTIGATE and a.best_next_experiment for a in r.approaches)
    assert any("ghost" in w for w in r.warnings)  # unknown hypotheses are dropped, not silently kept
    assert "RNA" not in "".join(f.calls) and f.calls.count("ModalityOutput") == 2  # routed only to relevant agents
    md = render(r)
    for h in ["## 1. Disease mechanism", "## 2.", "## 3.", "## 4.", "## 5.", "## 6."]:
        assert h in md


def test_checkpoint_reuse(tmp_path):
    Pipeline(Fake(), checkpoint_dir=tmp_path, log=lambda s: None).run("D")
    f2 = Fake()
    Pipeline(f2, checkpoint_dir=tmp_path, log=lambda s: None).run("D")
    assert f2.calls == []


def test_insufficient_evidence_stops_early():
    mech = MECH.model_copy(update={"conclusion": Conclusion.INSUFFICIENT_EVIDENCE, "conclusion_note": "unknown gene"})
    f_dossier = Dossier(disease_mechanism_summary="s", leverage_points=[], reviews=[], comparative_judgment="",
                        what_is_known=[], critical_gaps=["cause unknown"], next_actions=[], do_not_fund_yet=["everything"],
                        conclusion=Conclusion.INSUFFICIENT_EVIDENCE, conclusion_note="unknown gene")
    class R(Fake):
        def __call__(self, system, task, schema, tool_names=None):
            return f_dossier if schema is Dossier else super().__call__(system, task, schema, tool_names)
    r = R(mech)
    rep = Pipeline(r, log=lambda s: None).run("D")
    assert r.calls == ["DiseaseMechanism"] and rep.approaches == []
    assert "INSUFFICIENT EVIDENCE" in render(rep)


def test_tools_never_raise():
    from rarepath.tools import run_tool
    text, err = run_tool("nope", {})
    assert err
    text, err = run_tool("pubmed_search", {"bogus": 1})
    assert err
