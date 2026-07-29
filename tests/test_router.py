from cost_estimator.router import route_prompt


def test_cache_hit_on_normalized_match():
    cache_keys = {"what is your return policy?"}
    decision = route_prompt("  WHAT IS YOUR RETURN POLICY?  ", cache_keys=cache_keys)
    assert decision.route == "cache_hit"
    assert "cached" in decision.reason


def test_heavy_term_routes_to_premium():
    decision = route_prompt("Please analyze this report.", cache_keys=set())
    assert decision.route == "premium-cloud-large"
    assert "analyze" in decision.reason


def test_word_threshold_routes_to_premium():
    prompt = " ".join(["word"] * 16)
    decision = route_prompt(prompt, cache_keys=set(), word_threshold=15)
    assert decision.route == "premium-cloud-large"
    assert "threshold" in decision.reason


def test_default_routes_to_local_slm():
    decision = route_prompt("Thanks, that works.", cache_keys=set())
    assert decision.route == "local-slm"
    assert decision.reason


def test_cache_checked_before_heavy_term():
    cache_keys = {"please analyze this report."}
    decision = route_prompt("Please analyze this report.", cache_keys=cache_keys)
    assert decision.route == "cache_hit"


def test_no_cache_keys_falls_through_to_routing():
    decision = route_prompt("Thanks, that works.", cache_keys=None)
    assert decision.route == "local-slm"


def test_custom_heavy_terms_and_threshold():
    decision = route_prompt(
        "Summarize this briefly",
        cache_keys=set(),
        heavy_terms=("summarize",),
        word_threshold=15,
    )
    assert decision.route == "premium-cloud-large"
    assert "summarize" in decision.reason
