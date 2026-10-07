"""Agent runner: a bounded research loop followed by one structured-output call.

Each agent is `runner(system, task, schema, tool_names) -> schema instance`.
The pipeline depends only on that callable, so tests can substitute a fake.

Notes on API usage:
- Model is claude-opus-5-5; thinking is always on for it, so `thinking` is omitted
  and depth is controlled with `output_config.effort`.
- Forced tool_choice is not supported on this model, so structure comes from
  `output_format` (structured outputs), not from a "submit" tool.
- Server-side refusal fallbacks are enabled (beta `server-side-fallback-2026-07-01`)
  because life-science content can trip safety classifiers; a refusal that
  survives the fallback chain raises RefusalError.
"""
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Protocol, TypeVar

import anthropic
from pydantic import BaseModel

from . import tools as T

M = TypeVar("M", bound=BaseModel)
DEFAULT_MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class RefusalError(RuntimeError):
    pass


class Runner(Protocol):
    def __call__(self, system: str, task: str, schema: type[M], tool_names: list[str] = ...) -> M: ...


@dataclass
class Usage:
    """Thread-safe usage meter. Logs one line per model call plus a running total, and
    optionally appends each call to a JSONL file for later monitoring.

    cost_usd is as reported by the backend; on the subscription backend it is a notional
    API-equivalent figure (what the calls would cost at API rates), not a bill."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    cost_usd: float = 0.0
    calls: int = 0
    tool_calls: int = 0
    log: Callable[[str], None] = lambda s: None
    path: Path | None = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record(self, agent: str, model: str | None, input_tokens: int = 0, output_tokens: int = 0,
               cache_read: int = 0, cache_write: int = 0, cost_usd: float | None = None, turns: int | None = None) -> None:
        with self._lock:
            self.calls += 1
            self.input_tokens += input_tokens
            self.output_tokens += output_tokens
            self.cache_read_tokens += cache_read
            self.cache_write_tokens += cache_write
            self.cost_usd += cost_usd or 0.0
            row = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"), "agent": agent, "model": model,
                   "input_tokens": input_tokens, "output_tokens": output_tokens, "cache_read_tokens": cache_read,
                   "cache_write_tokens": cache_write, "cost_usd": cost_usd, "turns": turns,
                   "cum_calls": self.calls, "cum_tool_calls": self.tool_calls, "cum_cost_usd": round(self.cost_usd, 4),
                   "cum_input_tokens": self.input_tokens, "cum_output_tokens": self.output_tokens}
            if self.path:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("a") as f:
                    f.write(json.dumps(row) + "\n")
            self.log(f"    usage [{agent}] in={input_tokens:,} (+{cache_read:,} cached) out={output_tokens:,}"
                     + (f" ${cost_usd:.3f}" if cost_usd is not None else "")
                     + f" | total: {self.calls} calls, {self.tool_calls} tools, "
                       f"{self.input_tokens + self.cache_read_tokens:,} in / {self.output_tokens:,} out, ${self.cost_usd:.2f}")

    def count_tool(self) -> None:
        with self._lock:
            self.tool_calls += 1

    def summary(self) -> str:
        return (f"{self.calls} model calls, {self.tool_calls} tool calls, {self.input_tokens:,} input "
                f"(+{self.cache_read_tokens:,} cache-read) / {self.output_tokens:,} output tokens, ${self.cost_usd:.2f}")


class ClaudeRunner:
    def __init__(self, model: str = DEFAULT_MODEL, effort: str = "medium", max_turns: int = 10,
                 fallbacks: bool = True, log: Callable[[str], None] = lambda s: None,
                 client: anthropic.Anthropic | None = None, usage_path: Path | None = None):
        self.client = client or anthropic.Anthropic()
        self.model, self.effort, self.max_turns, self.log = model, effort, max_turns, log
        self.fallbacks = fallbacks
        self.usage = Usage(log=log, path=usage_path)

    # -- low level ---------------------------------------------------------
    def _kwargs(self, system: str, messages: list, tools: list[dict]) -> dict:
        kw: dict = dict(model=self.model, max_tokens=16000, system=system, messages=messages,
                        output_config={"effort": self.effort})
        if tools:
            kw["tools"] = tools
        if self.fallbacks:
            kw["betas"] = [FALLBACK_BETA]
            kw["fallbacks"] = "default"
        return kw

    def _account(self, resp, agent: str) -> None:
        u = resp.usage
        self.usage.record(agent, getattr(resp, "model", self.model), u.input_tokens, u.output_tokens,
                          getattr(u, "cache_read_input_tokens", 0) or 0, getattr(u, "cache_creation_input_tokens", 0) or 0)
        if resp.stop_reason == "refusal":
            cat = getattr(getattr(resp, "stop_details", None), "category", None)
            raise RefusalError(f"Model refused the request (category={cat}) even after fallbacks")
        if resp.stop_reason == "max_tokens":
            raise RuntimeError("Response hit max_tokens; output would be truncated")

    # -- the agent ---------------------------------------------------------
    def __call__(self, system: str, task: str, schema: type[M], tool_names: list[str] | None = None) -> M:
        tools = T.schemas(tool_names or [])
        agent = schema.__name__
        messages: list = [{"role": "user", "content": task}]
        pending: list = []
        for turn in range(self.max_turns if tools else 0):
            resp = self.client.beta.messages.create(**self._kwargs(system, messages, tools))
            self._account(resp, agent)
            messages.append({"role": "assistant", "content": resp.content})  # thinking blocks must be replayed intact
            pending = [b for b in resp.content if b.type == "tool_use"]
            if resp.stop_reason != "tool_use" or not pending:
                pending = []
                break
            if turn == self.max_turns - 1:
                break  # budget exhausted; answer the dangling tool calls below
            results = []
            for b in pending:
                text, err = T.run_tool(b.name, b.input)
                self.usage.count_tool()
                self.log(f"    tool {b.name}({json.dumps(b.input)[:90]})" + (" [error]" if err else ""))
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": text, "is_error": err})
            messages.append({"role": "user", "content": results})
            pending = []

        closing = ("Research is complete. Produce the final structured output now from the evidence gathered. "
                   "Where evidence is thin, say so and use the appropriate conclusion value rather than guessing. "
                   "Mark every claim EVIDENCE, INFERENCE or HYPOTHESIS and cite sources (PMID, NCT, record id).")
        content: list = [{"type": "tool_result", "tool_use_id": b.id, "is_error": True,
                          "content": "Research budget exhausted; tool not run."} for b in pending]
        content.append({"type": "text", "text": closing})
        messages.append({"role": "user", "content": content})

        kw = self._kwargs(system, messages, tools)
        if tools:
            kw["tool_choice"] = {"type": "none"}
        resp = self.client.beta.messages.parse(output_format=schema, **kw)
        self._account(resp, agent + ':final')
        if resp.parsed_output is None:
            raise RuntimeError("Structured output failed to parse")
        return resp.parsed_output
