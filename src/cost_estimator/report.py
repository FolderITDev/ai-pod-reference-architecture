"""Renders a compare_strategies() result as Markdown or JSON."""

from __future__ import annotations

import json

_ASSUMPTIONS_PATH = "docs/decision_records/assumptions.md"
_ASSUMPTIONS_LINK = "../docs/decision_records/assumptions.md"


def to_markdown(comparison: dict) -> str:
    baseline = comparison["baseline"]
    routed = comparison["routed"]
    lines = [
        "| Strategy | Requests | Tokens in | Tokens out | Estimated cost (USD) |",
        "|----------|---------:|----------:|-----------:|---------------------:|",
        f"| Baseline (all premium) | {baseline['requests']} | {baseline['input_tokens']} "
        f"| {baseline['output_tokens']} | ${baseline['cost_usd']:.6f} |",
        f"| Cache + routing        | {routed['requests']} | {routed['input_tokens']} "
        f"| {routed['output_tokens']} | ${routed['cost_usd']:.6f} |",
        "",
        f"Estimated savings: `{comparison['savings_pct']}%` · "
        f"Pricing as of `{comparison['pricing_date']}` · "
        f"Assumptions: [`{_ASSUMPTIONS_PATH}`]({_ASSUMPTIONS_LINK})",
    ]
    return "\n".join(lines) + "\n"


def to_json(comparison: dict) -> str:
    return json.dumps(comparison, indent=2) + "\n"
