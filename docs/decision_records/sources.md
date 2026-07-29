# Pricing Sources

The token-cost estimator uses a pricing table that is a **dated snapshot** of official provider prices. This file records where each price came from and when, so that any result the benchmark produces can be traced and reproduced.

Prices change. Treat every benchmark figure as "estimated cost at the pricing date below," and re-run the benchmark against current prices when needed.

---

## Pricing date

**As of: `2026-07-28`**

Update this date whenever any price below changes, and regenerate `benchmarks/results.md`.

---

## Model pricing

Prices are in USD per 1,000,000 tokens (per Mtok). Fill each row from the provider's official pricing page and record the URL and the date you accessed it. Do not copy prices from third-party summaries — go to the source.

| Model key (in `pricing.py`) | Real model it maps to | Input (USD / Mtok) | Output (USD / Mtok) | Source URL | Accessed |
|---|---|---:|---:|---|---|
| `premium-cloud-large` | Anthropic Claude Opus 4.8 (`claude-opus-4-8`) | `5.00` | `25.00` | <https://platform.claude.com/docs/en/about-claude/pricing> | `2026-07-28` |
| `premium-cloud-mini` | Anthropic Claude Haiku 4.5 (`claude-haiku-4-5`) | `1.00` | `5.00` | <https://platform.claude.com/docs/en/about-claude/pricing> | `2026-07-28` |
| `local-slm` | Self-hosted open-weight model (organization-specific) | `0.00` | `0.00` | N/A — owned infrastructure | `2026-07-28` |

Notes:

- `local-slm` is priced at zero token cost by design; its real cost is compute and amortization, not per-token billing. See assumption 2 in [`assumptions.md`](assumptions.md). If you model infrastructure cost, record the basis for that figure here too.
- The model keys on the left must match the keys used in `src/cost_estimator/pricing.py` exactly. If you add a model, add both a row here and an entry there.

---

## How to update pricing

1. Open each provider's official pricing page.
2. Copy the input and output price per Mtok into the table above.
3. Record the source URL and the date accessed.
4. Update **Pricing date** at the top and `PRICING_DATE` in `src/cost_estimator/pricing.py` to match.
5. Re-run the benchmark and commit the regenerated `benchmarks/results.md`:

   ```bash
   python -m cost_estimator.benchmark \
       --dataset benchmarks/dataset.jsonl \
       --cache benchmarks/cache_keys.txt \
       --format markdown
   ```

6. Confirm the pricing date shown in `results.md` matches this file.

---

## Why this file exists

Reproducibility is the whole point of the estimator. A cost figure with no dated source is not verifiable, and unverifiable numbers are exactly what this project avoids. Anyone should be able to read this file, visit the same sources, and understand how every figure in the benchmark was produced.
