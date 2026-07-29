from cost_estimator.estimator import compare_strategies, estimate_request
from cost_estimator.tokenizer import count_tokens


def test_hand_computed_premium_cost():
    # "Please analyze this report." is 5 tokens (cl100k_base); "analyze" forces
    # premium-cloud-large routing. premium-cloud-large is $5.00 / $25.00 per Mtok.
    record = {"id": "r1", "prompt": "Please analyze this report.", "expected_output_tokens": 100}
    result = estimate_request(record, cache_keys=set())

    expected_cost = round(5 * 5.00 / 1_000_000 + 100 * 25.00 / 1_000_000, 6)

    assert result.route == "premium-cloud-large"
    assert result.input_tokens == 5
    assert result.output_tokens == 100
    assert result.cost_usd == expected_cost


def test_cache_hit_has_zero_cost_but_still_counts_tokens():
    record = {"id": "r2", "prompt": "What is your return policy?", "expected_output_tokens": 40}
    cache_keys = {"what is your return policy?"}
    result = estimate_request(record, cache_keys=cache_keys)

    assert result.route == "cache_hit"
    assert result.cost_usd == 0.0
    assert result.input_tokens == count_tokens(record["prompt"])
    assert result.output_tokens == 40


def test_local_slm_defaults_to_zero_cost():
    record = {"id": "r3", "prompt": "Hi there!", "expected_output_tokens": 8}
    result = estimate_request(record, cache_keys=set())

    assert result.route == "local-slm"
    assert result.cost_usd == 0.0


def test_local_slm_uses_infra_cost_when_given():
    record = {"id": "r4", "prompt": "Hi there!", "expected_output_tokens": 8}
    result = estimate_request(record, cache_keys=set(), local_infra_cost_per_request=0.002)

    assert result.route == "local-slm"
    assert result.cost_usd == 0.002


def test_compare_strategies_aggregates_and_forces_baseline_to_premium():
    records = [
        {"id": "a", "prompt": "Hi there!", "expected_output_tokens": 8},
        {"id": "b", "prompt": "Please analyze this report.", "expected_output_tokens": 100},
    ]
    cache_keys = set()
    comparison = compare_strategies(records, cache_keys)

    assert comparison["baseline"]["requests"] == 2
    assert comparison["routed"]["requests"] == 2
    # baseline forces both requests through premium-cloud-large, even the
    # one that the router would send to local-slm.
    assert comparison["baseline"]["cost_usd"] > comparison["routed"]["cost_usd"]
    assert comparison["pricing_date"]


def test_savings_pct_is_positive_when_routing_saves_money():
    records = [{"id": "a", "prompt": "Hi there!", "expected_output_tokens": 8}]
    comparison = compare_strategies(records, cache_keys=set())
    assert comparison["savings_pct"] > 0


def test_savings_pct_is_zero_when_routing_matches_baseline():
    records = [{"id": "a", "prompt": "Please analyze this report.", "expected_output_tokens": 100}]
    comparison = compare_strategies(records, cache_keys=set())
    # this record routes to premium-cloud-large either way, so there is no savings.
    assert comparison["savings_pct"] == 0.0
