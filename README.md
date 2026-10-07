# rarepath

Implements the multi-agent system specified in `AGENT.md`: disease → mechanism → therapeutic hypotheses →
modality agents → experiments → reviewed dossier.

```bash
uv venv && uv pip install -e ".[dev]"
claude            # log in once with your Claude subscription (no API key needed)
rarepath "SLC6A1 neurodevelopmental disorder"      # writes runs/<slug>/dossier.md + report.json
pytest                                             # offline, uses a fake runner
```

Layout: `schemas.py` (YAML shapes from the spec as Pydantic models) · `prompts.py` (one prompt per agent) ·
`tools.py` (Monarch, PubMed, ClinicalTrials.gov, Open Targets, ChEMBL, UniProt) · `llm.py` (bounded tool loop + structured output) ·
`pipeline.py` (fixed pipeline, no agent loops) · `render.py` (six-section dossier).

Backends: `--backend subscription` (default) runs agents through the Claude Agent SDK on your Claude Code login (llm_cc.py); `--backend api` uses the Anthropic API directly (llm.py; needs a key or `ant auth login`, model `claude-opus-5-5`, refusal fallbacks on, `--no-fallbacks` to disable). `--effort` defaults to medium.
Other choices:
each stage is checkpointed to `runs/<slug>/stages/` so reruns don't re-spend (`--fresh` to redo);
modality agents only receive hypotheses that name them, and run in parallel. MATRIX / Every Cure has no public API wired in yet.
