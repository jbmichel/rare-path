"""Runner backed by the Claude Agent SDK, i.e. your Claude Code login (subscription) - no API key.

Same contract as llm.ClaudeRunner: runner(system, task, schema, tool_names) -> schema instance.
Built-in Claude Code tools (Bash, Read, ...) and user/project settings are disabled; the agent
sees only our research tools, served in-process over MCP.
"""
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Callable, TypeVar

from claude_agent_sdk import (ClaudeAgentOptions, ResultMessage, create_sdk_mcp_server, query, tool)
from pydantic import BaseModel

from . import tools as T
from .llm import RefusalError, Usage

M = TypeVar("M", bound=BaseModel)
SERVER = "rp"


def _mcp_server(tool_names: list[str], on_call: Callable[[str, dict, bool], None]):
    sdk_tools = []
    for name in tool_names:
        schema = T.REGISTRY[name][0]

        def make(n=name, s=schema):
            @tool(n, s["description"], s["input_schema"])
            async def handler(args):
                text, err = await asyncio.to_thread(T.run_tool, n, args)
                on_call(n, args, err)
                return {"content": [{"type": "text", "text": text}], "is_error": err}
            return handler
        sdk_tools.append(make())
    return create_sdk_mcp_server(SERVER, tools=sdk_tools)


class SubscriptionRunner:
    def __init__(self, model: str | None = None, effort: str = "medium", max_turns: int = 10,
                 log: Callable[[str], None] = lambda s: None, usage_path: Path | None = None):
        # A stale API key would silently override the subscription login.
        if os.environ.pop("ANTHROPIC_API_KEY", None):
            log("  (ignoring ANTHROPIC_API_KEY; using Claude Code subscription login)")
        self.model, self.effort, self.max_turns, self.log = model, effort, max_turns, log
        self.usage = Usage(log=log, path=usage_path)

    def _on_call(self, name: str, args: dict, err: bool) -> None:
        self.usage.count_tool()
        self.log(f"    tool {name}({json.dumps(args)[:90]})" + (" [error]" if err else ""))

    async def _run(self, system: str, task: str, schema: type[M], tool_names: list[str]) -> M:
        out_fmt = {"type": "json_schema", "schema": schema.model_json_schema()}
        tail = ("\n\nWhen research is complete, answer with the final structured output. Mark every claim EVIDENCE / "
                "INFERENCE / HYPOTHESIS and cite sources you actually retrieved. Where evidence is thin, use the "
                "appropriate `conclusion` value rather than guessing.")

        def options(**kw) -> ClaudeAgentOptions:
            base = dict(system_prompt=system, model=self.model, effort=self.effort, output_format=out_fmt,
                        tools=[], setting_sources=[], permission_mode="default")
            if tool_names:
                base["mcp_servers"] = {SERVER: _mcp_server(tool_names, self._on_call)}
                base["allowed_tools"] = [f"mcp__{SERVER}__{n}" for n in tool_names]
            return ClaudeAgentOptions(**{**base, **kw})

        async def go(prompt: str, **kw) -> ResultMessage:
            res = None
            async for m in query(prompt=prompt, options=options(**kw)):
                if isinstance(m, ResultMessage):
                    res = m
            if res is None:
                raise RuntimeError("Agent SDK returned no result")
            u = res.usage or {}
            self.usage.record(schema.__name__ + (":final" if kw.get("resume") else ""), self.model or "subscription-default",
                              u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("cache_read_input_tokens", 0),
                              u.get("cache_creation_input_tokens", 0), res.total_cost_usd, res.num_turns)
            return res

        res = await go(task + tail + f"\n\nResearch budget: at most {self.max_turns} tool-use turns.",
                       max_turns=self.max_turns + 2)
        if res.structured_output is None and res.subtype == "error_max_turns":
            self.log("    research budget hit; asking agent to finalize")
            res = await go("Research budget exhausted. Produce the final structured output now from what you have.",
                           resume=res.session_id, max_turns=3)
        if res.structured_output is None:
            if res.stop_reason == "refusal":
                raise RefusalError("Model refused the request")
            raise RuntimeError(f"No structured output (subtype={res.subtype}, errors={res.errors}, result={str(res.result)[:200]})")
        return schema.model_validate(res.structured_output)

    def __call__(self, system: str, task: str, schema: type[M], tool_names: list[str] | None = None) -> M:
        return asyncio.run(self._run(system, task, schema, tool_names or []))
