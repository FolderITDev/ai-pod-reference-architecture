# Assumptions

The token-cost estimator is a **model**, so its output is only as valid as the assumptions behind it. Every assumption is listed here in plain terms. None of them are hidden inside the code.

## 1. No model is actually called

The estimator runs fully offline. It does not send requests to any LLM. It reasons about which target *would* handle a request and what that *would* cost. All figures are estimates, not measurements from live inference.

## 2. Local SLM is modeled at zero token cost

Requests routed to the local SLM are priced at zero tokens by default, because local inference runs on owned infrastructure and carries no per-token bill.

This is a simplification, not a claim that local inference is free. Real cost is compute, power, and amortization of hardware. To account for it, pass a per-request infrastructure cost to the estimator (`local_infra_cost_per_request`); the default of `0` exists only to keep the baseline comparison simple. Treat the "savings" figure as *token-billing savings*, not total cost of ownership.

## 3. Output tokens are a declared estimate

Because no model is called, the estimator cannot observe how long an answer would be. Each dataset record carries an `expected_output_tokens` value that is **declared, not measured**. These values are set per prompt (or per category) and should be documented when the dataset changes. Input tokens, by contrast, are counted exactly with `tiktoken`.

## 4. Pricing is a dated snapshot

The pricing table is a snapshot of official provider prices on a specific date. Prices change. The date and the source URLs live in [`sources.md`](sources.md). Results should always be read as "estimated cost at pricing date `YYYY-MM-DD`". Re-running the benchmark against current prices is expected.

## 5. The cache is exact-match, not semantic

In this reference, a "cache hit" means the normalized prompt (lowercased, trimmed) exactly matches a stored key. A real semantic cache would also match near-identical phrasings via embeddings, which would raise the hit rate. The reference therefore likely **understates** cache savings relative to a production semantic cache. This is intentional (see ADR-001 in [`architecture.md`](../architecture.md)).

## 6. Routing is rule-based

The router uses a short, explicit set of rules (heavy-reasoning terms and a word-count threshold). It is transparent and testable, but it is not a tuned classifier. Routing quality in a real deployment would depend on rules or a model fitted to the actual workload. The term list and threshold are configurable.

## 7. Latency is not modeled

The estimator reports cost only. It does not estimate or measure latency, because latency can only be measured against real inference. Any latency figure here would be fabricated, so none is reported (see ADR-003).

## 8. The dataset is illustrative

The prompts in `benchmarks/dataset.jsonl` are anonymized examples chosen to demonstrate the routing paths. They are not a representative sample of any real production traffic, and the resulting savings figure is specific to this dataset. Point the benchmark at your own prompts to get a figure relevant to your workload.

---

**Bottom line:** the estimator is useful for reasoning about the *shape* and *direction* of LLM cost under caching and routing, on a reproducible basis. It is not a precise forecast of a production bill.
