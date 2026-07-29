"""CLI entry point for the token-cost benchmark.

Invocation: this module is run with `src/` on the Python import path (the
package is not pip-installed). From the repository root:

    PYTHONPATH=src python -m cost_estimator.benchmark \\
        --dataset benchmarks/dataset.jsonl \\
        --cache benchmarks/cache_keys.txt \\
        --format markdown

On Windows PowerShell, set the path first: `$env:PYTHONPATH = "src"`.

Deterministic and offline: no network calls, no timestamps in the output.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from cost_estimator.estimator import compare_strategies
from cost_estimator.pricing import PRICING_DATE
from cost_estimator.report import to_json, to_markdown

BANNER = (
    "> Figures below use pricing sourced from the official provider pricing "
    "page (see `docs/decision_records/sources.md` for URLs and access date). "
    f"Pricing date: `{PRICING_DATE}`. Re-run this benchmark after any price "
    "change.\n\n"
)


def load_dataset(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_cache_keys(path: str) -> set[str]:
    with open(path, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Deterministic, offline token-cost benchmark.")
    parser.add_argument("--dataset", required=True, help="Path to a JSONL dataset of prompt records.")
    parser.add_argument("--cache", required=True, help="Path to a newline-separated cache-keys file.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    records = load_dataset(args.dataset)
    cache_keys = load_cache_keys(args.cache)
    comparison = compare_strategies(records, cache_keys)

    if args.format == "markdown":
        output_path = Path("benchmarks/results.md")
        body = BANNER + to_markdown(comparison)
    else:
        output_path = Path("benchmarks/results.json")
        body = to_json(comparison)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")

    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
