"""Rule-based, transparent request router. See docs/architecture.md, Stage 2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RoutingDecision:
    route: str  # "cache_hit" | "local-slm" | "premium-cloud-large"
    reason: str


def route_prompt(
    prompt: str,
    cache_keys: set[str] | None = None,
    heavy_terms: tuple[str, ...] = ("analyze", "optimize"),
    word_threshold: int = 15,
) -> RoutingDecision:
    normalized = prompt.lower().strip()

    if cache_keys and normalized in cache_keys:
        return RoutingDecision(route="cache_hit", reason="normalized prompt matches a cached key")

    matched_terms = [term for term in heavy_terms if term in normalized]
    if matched_terms:
        return RoutingDecision(
            route="premium-cloud-large",
            reason=f"contains heavy-reasoning term(s): {', '.join(matched_terms)}",
        )

    word_count = len(normalized.split())
    if word_count > word_threshold:
        return RoutingDecision(
            route="premium-cloud-large",
            reason=f"word count {word_count} exceeds threshold {word_threshold}",
        )

    return RoutingDecision(route="local-slm", reason="routine request within word threshold")
