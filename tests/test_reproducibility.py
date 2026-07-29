import json
import os
import subprocess
import sys
from pathlib import Path

from cost_estimator.estimator import compare_strategies

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASET = REPO_ROOT / "benchmarks" / "dataset.jsonl"
CACHE_KEYS = REPO_ROOT / "benchmarks" / "cache_keys.txt"


def _load_records():
    with open(DATASET, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _load_cache_keys():
    with open(CACHE_KEYS, encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


def test_compare_strategies_is_deterministic_in_process():
    records = _load_records()
    cache_keys = _load_cache_keys()

    first = compare_strategies(records, cache_keys)
    second = compare_strategies(records, cache_keys)

    assert first == second


def test_benchmark_cli_is_deterministic_across_processes(tmp_path):
    # Run with cwd=tmp_path so the CLI's output file lands outside the repo's
    # own benchmarks/ directory, keeping this test free of side effects.
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    cmd = [
        sys.executable,
        "-m",
        "cost_estimator.benchmark",
        "--dataset",
        str(DATASET),
        "--cache",
        str(CACHE_KEYS),
        "--format",
        "json",
    ]

    subprocess.run(cmd, cwd=tmp_path, env=env, check=True, capture_output=True)
    first_output = (tmp_path / "benchmarks" / "results.json").read_text(encoding="utf-8")

    subprocess.run(cmd, cwd=tmp_path, env=env, check=True, capture_output=True)
    second_output = (tmp_path / "benchmarks" / "results.json").read_text(encoding="utf-8")

    assert first_output == second_output
