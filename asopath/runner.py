"""Agent runner on the Claude Code subscription login (Claude Agent SDK). One call = one agent session."""
from __future__ import annotations

import asyncio
import json
import os
import threading
import time
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, create_sdk_mcp_server, query, tool
from pydantic import BaseModel

from . import tools as T

BUILTIN = ["WebSearch", "WebFetch"]


class Runner:
    def __init__(self, model=None, effort="medium", max_turns=25, usage_path: Path | None = None, log=print):
        os.environ.pop("ANTHROPIC_API_KEY", None)   # a stale key would override the subscription login
        self.model, self.effort, self.max_turns, self.log, self.path = model, effort, max_turns, log, usage_path
        self.lock, self.total = threading.Lock(), {"calls": 0, "tokens": 0, "notional_usd": 0.0, "tool_calls": 0}

    def _record(self, agent, res):
        u = res.usage or {}
        toks = sum(u.get(k, 0) or 0 for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
        rec = {"t": time.strftime("%H:%M:%S"), "agent": agent, "turns": res.num_turns, "tokens": toks,
               "notional_usd": round(res.total_cost_usd or 0, 4)}
        with self.lock:
            self.total["calls"] += 1; self.total["tokens"] += toks; self.total["notional_usd"] += rec["notional_usd"]
            if self.path:
                with open(self.path, "a") as f:
                    f.write(json.dumps(rec) + "\n")
        self.log(f"  [{agent}] {res.num_turns} turns, {toks:,} tok, ~${rec['notional_usd']:.2f} notional")

    async def _run(self, agent, system, task, schema, tool_names, web):
        def mcp():
            def mk(n):
                @tool(n, T.REGISTRY[n][0]["description"], T.REGISTRY[n][0]["input_schema"])
                async def h(args):
                    text, err = await asyncio.to_thread(T.run_tool, n, args)
                    with self.lock: self.total["tool_calls"] += 1
                    self.log(f"    [{agent}] {n}({json.dumps(args)[:80]})")
                    return {"content": [{"type": "text", "text": text}], "is_error": err}
                return h
            return create_sdk_mcp_server("aso", tools=[mk(n) for n in tool_names])

        allowed = (BUILTIN if web else []) + [f"mcp__aso__{n}" for n in tool_names]

        def opts(**kw):
            base = dict(system_prompt=system, model=self.model, effort=self.effort, tools=BUILTIN if web else [],
                        setting_sources=[], allowed_tools=allowed,
                        output_format={"type": "json_schema", "schema": schema.model_json_schema()})
            if tool_names:
                base["mcp_servers"] = {"aso": mcp()}
            return ClaudeAgentOptions(**{**base, **kw})

        async def go(prompt, **kw):
            res = None
            async for m in query(prompt=prompt, options=opts(**kw)):
                if isinstance(m, ResultMessage):
                    res = m
            self._record(agent, res)
            return res

        res = await go(task + f"\n\nResearch budget: at most {self.max_turns} tool turns, then answer in the required structure.",
                       max_turns=self.max_turns + 2)
        if res.structured_output is None and res.subtype == "error_max_turns":
            res = await go("Budget exhausted. Give the final structured answer now from what you have.", resume=res.session_id, max_turns=3)
        if res.structured_output is None:
            raise RuntimeError(f"{agent}: no structured output ({res.subtype})")
        return schema.model_validate(res.structured_output)

    def __call__(self, agent, system, task, schema: type[BaseModel], tool_names=(), web=False):
        return asyncio.run(self._run(agent, system, task, schema, list(tool_names), web))
