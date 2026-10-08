"""Grade a run against an eval fixture. The fixture is read ONLY here, never by the agent pipeline.

usage: python evals/run_eval.py evals/dmd_exon55.md runs/<slug>
"""
import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from asopath.render import words  # noqa: E402
from asopath.runner import Runner  # noqa: E402

DIMS = ["A_design_space", "B_product_reasoning", "C_delivery", "D_currentness", "E_program_selection", "F_experiment", "G_concision"]


class Dim(BaseModel):
    dimension: str = Field(description="One of: " + ", ".join(DIMS))
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
evidence appendix. Score each of the seven dimensions 0-2 exactly per the rubric, using ONLY what is in the agent output (the main answer carries the decision;
the appendix shows what was found). Do not give credit for things the agent did not state. Check every item under 'Unacceptable Failures' and mark triggered or not.
Dimension G (concision) is judged on the main answer; the word count is supplied. Use the exact dimension keys: """ + ", ".join(DIMS) + "."


def main(fixture: str, run: str):
    run_dir = Path(run)
    answer = (run_dir / "answer.md").read_text()
    task = (f"=== EVAL FIXTURE ===\n{Path(fixture).read_text()}\n\n=== MAIN ANSWER ({words(answer)} words) ===\n{answer}\n\n"
            f"=== EVIDENCE APPENDIX ===\n{(run_dir / 'evidence.md').read_text()}")
    runner = Runner(effort="high", max_turns=3, usage_path=run_dir / "eval_usage.jsonl")
    g = runner("eval_grader", SYSTEM, task, Grade)
    total = sum(d.score for d in g.dimensions)
    s = {d.dimension: d.score for d in g.dimensions}
    zero = [k for k in ("A_design_space", "C_delivery", "E_program_selection") if s.get(k) == 0]
    passed = total >= 12 and not zero
    (run_dir / "eval.json").write_text(json.dumps({"total": total, "max": 14, "passed": passed, "words": words(answer), **g.model_dump()}, indent=1))
    lines = [f"# Eval result: {total}/14 — {'PASS' if passed else 'FAIL'}", "", "| Dimension | Score | Evidence |", "|---|---|---|"]
    lines += [f"| {d.dimension} | {d.score} | {d.evidence} |" for d in g.dimensions]
    lines += ["", "## Unacceptable failures"] + [f"- [{'TRIGGERED' if f.triggered else 'ok'}] {f.failure} — {f.note}" for f in g.unacceptable_failures]
    lines += ["", "## Required discoveries missed"] + [f"- {x}" for x in g.required_discoveries_missed] + ["", g.summary]
    if zero:
        lines.insert(1, f"Zero in a gated dimension: {', '.join(zero)}")
    (run_dir / "eval.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
