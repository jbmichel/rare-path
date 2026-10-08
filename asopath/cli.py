import argparse
import re
from pathlib import Path

from .pipeline import Pipeline
from .render import evidence, main_answer, references, words
from .runner import Runner


def main():
    ap = argparse.ArgumentParser(prog="asopath")
    ap.add_argument("--disease", required=True)
    ap.add_argument("--gene", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--transcript")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--model", default=None)
    ap.add_argument("--max-turns", type=int, default=30)
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()
    out = Path("runs") / re.sub(r"[^a-z0-9]+", "-", f"{a.gene}-{a.variant}".lower()).strip("-")[:60]
    out.mkdir(parents=True, exist_ok=True)
    runner = Runner(a.model, a.effort, a.max_turns, usage_path=out / "usage.jsonl", log=lambda s: print(s, flush=True))
    r = Pipeline(runner, out, a.fresh, log=lambda s: print(s, flush=True))(a.disease, a.gene, a.variant, a.transcript)
    case = f"{a.gene} {a.variant}"
    (out / "answer.md").write_text(f"# {case}\n\n" + main_answer(r["answer"]))
    (out / "evidence.md").write_text(evidence(case, r))
    print(f"\nanswer: {words(main_answer(r['answer']))} words\nusage: {runner.total}\nwrote {out}/answer.md, evidence.md", flush=True)


if __name__ == "__main__":
    main()
