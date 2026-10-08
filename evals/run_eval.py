"""Grade a run against an eval fixture. The fixture is read ONLY here, never by the agent pipeline.

usage: python evals/run_eval.py evals/<fixture>.md runs/<slug> [answer-file, default answer.md]
"""
import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from asopath.render import words  # noqa: E402
from asopath.runner import Runner  # noqa: E402

# Per-fixture rubric: dimension keys, max score, pass threshold, dimensions where a 0 fails the eval.
RUBRICS = {
    "dmd_exon55": dict(
        dims=["A_design_space", "B_product_reasoning", "C_delivery", "D_currentness", "E_program_selection", "F_experiment", "G_concision"],
        pass_at=12, gated=["A_design_space", "C_delivery", "E_program_selection"]),
    "cdkl5_lof": dict(
        dims=["A_framing_product", "B_design_space", "C_existence_risk", "D_transferability", "E_currentness", "F_delivery", "G_experiment", "H_concision_evidence"],
        pass_at=14, gated=["B_design_space", "C_existence_risk", "D_transferability"]),
}


class Dim(BaseModel):
    dimension: str = Field(description="Exact dimension key from the instructions")
    score: int = Field(ge=0, le=2)
    evidence: str = Field(description="Quote or cite the specific text in the output that justifies the score; <=50 words")


class Failure(BaseModel):
    failure: str
    triggered: bool
    note: str = Field(description="<=30 words")


class Grade(BaseModel):
    dimensions: list[Dim]
    unacceptable_failures: list[Failure]
    required_discoveries_missed: list[str]
    summary: str = Field(description="<=80 words, blunt")


SYSTEM = """You are a strict, independent grader of an ASO discovery agent's output. You receive the eval fixture (rubric) and the agent's main answer plus its
evidence appendix. Score each dimension 0-2 exactly per the rubric, using ONLY what is in the agent output (the main answer carries the decision;
the appendix shows what was found). Do not give credit for things the agent did not state. Check every item under 'Unacceptable Failures' and mark triggered or not.
The concision dimension is judged on the main answer; the word count is supplied. Use the exact dimension keys: """


def main(fixture: str, run: str, answer_file: str = "answer.md"):
    rub = RUBRICS[Path(fixture).stem]
    run_dir = Path(run)
    tag = "" if answer_file == "answer.md" else "_" + Path(answer_file).stem
    answer = (run_dir / answer_file).read_text()
    task = (f"=== EVAL FIXTURE ===\n{Path(fixture).read_text()}\n\n=== MAIN ANSWER ({words(answer)} words) ===\n{answer}\n\n"
            f"=== EVIDENCE APPENDIX ===\n{(run_dir / 'evidence.md').read_text()}")
    runner = Runner(effort="high", max_turns=3, usage_path=run_dir / "eval_usage.jsonl")
    g = runner("eval_grader", SYSTEM + ", ".join(rub["dims"]) + ".", task, Grade)
    total = sum(d.score for d in g.dimensions)
    s = {d.dimension: d.score for d in g.dimensions}
    zero = [k for k in rub["gated"] if s.get(k) == 0]
    mx = 2 * len(rub["dims"])
    passed = total >= rub["pass_at"] and not zero
    (run_dir / f"eval{tag}.json").write_text(json.dumps({"total": total, "max": mx, "passed": passed, "words": words(answer), **g.model_dump()}, indent=1))
    lines = [f"# Eval result: {total}/{mx} — {'PASS' if passed else 'FAIL'}", "", "| Dimension | Score | Evidence |", "|---|---|---|"]
    lines += [f"| {d.dimension} | {d.score} | {d.evidence} |" for d in g.dimensions]
    lines += ["", "## Unacceptable failures"] + [f"- [{'TRIGGERED' if f.triggered else 'ok'}] {f.failure} — {f.note}" for f in g.unacceptable_failures]
    lines += ["", "## Required discoveries missed"] + [f"- {x}" for x in g.required_discoveries_missed] + ["", g.summary]
    if zero:
        lines.insert(1, f"Zero in a gated dimension: {', '.join(zero)}")
    (run_dir / f"eval{tag}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:4])
