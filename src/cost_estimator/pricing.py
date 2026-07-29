"""Dated pricing table for the token-cost estimator.

Prices are sourced from the official Anthropic API pricing page; see
docs/decision_records/sources.md for the exact URL, the model each key
maps to, and the access date. The keys below must match the keys used
in that file exactly.
"""

PRICING_DATE = "2026-07-28"

# USD per 1,000,000 tokens (per Mtok).
MODEL_PRICING = {
    "premium-cloud-large": {"input_per_mtok": 5.00, "output_per_mtok": 25.00},
    "premium-cloud-mini": {"input_per_mtok": 1.00, "output_per_mtok": 5.00},
    "local-slm": {"input_per_mtok": 0.0, "output_per_mtok": 0.0},
}
