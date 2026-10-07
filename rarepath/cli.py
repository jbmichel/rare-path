from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from .llm import DEFAULT_MODEL, ClaudeRunner
from .llm_cc import SubscriptionRunner
from .pipeline import Pipeline
from .render import render


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="rarepath", description="Rare-disease therapeutic decision dossier")
    ap.add_argument("disease", help='e.g. "SLC6A1 neurodevelopmental disorder"')
    ap.add_argument("-o", "--out", default="runs", help="output directory (default: runs/)")
    ap.add_argument("--backend", choices=["subscription", "api"], default="subscription",
                    help="subscription: Claude Code login via Agent SDK (default); api: ANTHROPIC_API_KEY / ant profile")
    ap.add_argument("--model", default=None, help="default: your Claude Code model (subscription) or claude-opus-5-5 (api)")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--max-turns", type=int, default=10, help="tool-use turns per agent")
    ap.add_argument("--max-hypotheses", type=int, default=5)
    ap.add_argument("--no-fallbacks", action="store_true", help="api backend only: disable server-side refusal fallbacks")
    ap.add_argument("--fresh", action="store_true", help="ignore existing stage checkpoints")
    a = ap.parse_args(argv)

    slug = re.sub(r"[^a-z0-9]+", "-", a.disease.lower()).strip("-")[:60]
    out = Path(a.out) / slug
    ckpt = out / "stages"
    if a.fresh and ckpt.exists():
        for f in ckpt.glob("*.json"):
            f.unlink()

    log = lambda s: print(s, file=sys.stderr, flush=True)
    if a.backend == "api":
        runner = ClaudeRunner(a.model or DEFAULT_MODEL, a.effort, a.max_turns, fallbacks=not a.no_fallbacks, log=log, usage_path=out / 'usage.jsonl')
    else:
        runner = SubscriptionRunner(a.model, a.effort, a.max_turns, log=log, usage_path=out / 'usage.jsonl')
    report = Pipeline(runner, max_hypotheses=a.max_hypotheses, checkpoint_dir=ckpt, log=log).run(a.disease)

    out.mkdir(parents=True, exist_ok=True)
    (out / "dossier.md").write_text(render(report))
    (out / "report.json").write_text(report.model_dump_json(indent=2))
    log(f"\nWrote {out}/dossier.md, report.json, usage.jsonl\nUsage this run: {runner.usage.summary()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
