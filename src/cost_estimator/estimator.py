"""Per-request and aggregate cost estimation. See docs/architecture.md, Stage 4."""

from __future__ import annotations

from dataclasses import dataclass

from cost_estimator.pricing import MODEL_PRICING, PRICING_DATE
from cost_estimator.router import route_prompt
from cost_estimator.tokenizer import count_tokens


@dataclass
class RequestCost:
    id: str
    route: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def _priced_cost(route: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING[route]
    return (
        input_tokens * pricing["input_per_mtok"] / 1_000_000
        + output_tokens * pricing["output_per_mtok"] / 1_000_000
    )


def estimate_request(
    record: dict,
    cache_keys: set[str],
    local_infra_cost_per_request: float = 0.0,
) -> RequestCost:
    input_tokens = count_tokens(record["prompt"])
    output_tokens = record["expected_output_tokens"]
    decision = route_prompt(record["prompt"], cache_keys=cache_keys)

    if decision.route == "cache_hit":
        cost = 0.0
    elif decision.route == "local-slm":
        cost = local_infra_cost_per_request
    else:
        cost = _priced_cost(decision.route, input_tokens, output_tokens)

    return RequestCost(
        id=record["id"],
        route=decision.route,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=round(cost, 6),
    )


def estimate_dataset(
    records: list[dict],
    cache_keys: set[str],
    local_infra_cost_per_request: float = 0.0,
) -> list[RequestCost]:
    return [estimate_request(r, cache_keys, local_infra_cost_per_request) for r in records]


def _baseline_request(record: dict) -> RequestCost:
    """Force every request through premium-cloud-large, ignoring cache/routing."""
    input_tokens = count_tokens(record["prompt"])
    output_tokens = record["expected_output_tokens"]
    cost = _priced_cost("premium-cloud-large", input_tokens, output_tokens)
    return RequestCost(
        id=record["id"],
        route="premium-cloud-large",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost_usd=round(cost, 6),
    )


def _totals(costs: list[RequestCost]) -> dict:
    return {
        "requests": len(costs),
        "input_tokens": sum(c.input_tokens for c in costs),
        "output_tokens": sum(c.output_tokens for c in costs),
        "cost_usd": round(sum(c.cost_usd for c in costs), 6),
    }


def compare_strategies(
    records: list[dict],
    cache_keys: set[str],
    local_infra_cost_per_request: float = 0.0,
) -> dict:
    baseline_totals = _totals([_baseline_request(r) for r in records])
    routed_totals = _totals(estimate_dataset(records, cache_keys, local_infra_cost_per_request))

    baseline_cost = baseline_totals["cost_usd"]
    routed_cost = routed_totals["cost_usd"]
    if baseline_cost > 0:
        savings_pct = round((baseline_cost - routed_cost) / baseline_cost * 100, 1)
    else:
        savings_pct = 0.0

    return {
        "baseline": baseline_totals,
        "routed": routed_totals,
        "savings_pct": savings_pct,
        "pricing_date": PRICING_DATE,
    }
