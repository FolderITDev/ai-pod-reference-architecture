import re

from cost_estimator.pricing import MODEL_PRICING, PRICING_DATE
from cost_estimator.router import route_prompt


def test_pricing_date_is_a_dated_string():
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", PRICING_DATE)


def test_pricing_table_has_expected_keys():
    assert set(MODEL_PRICING) == {"premium-cloud-large", "premium-cloud-mini", "local-slm"}


def test_every_entry_has_input_and_output_prices():
    for key, prices in MODEL_PRICING.items():
        assert isinstance(prices["input_per_mtok"], float)
        assert isinstance(prices["output_per_mtok"], float)
        assert prices["input_per_mtok"] >= 0.0
        assert prices["output_per_mtok"] >= 0.0


def test_local_slm_is_priced_at_zero():
    assert MODEL_PRICING["local-slm"] == {"input_per_mtok": 0.0, "output_per_mtok": 0.0}


def test_every_router_emittable_priced_route_is_in_pricing_table():
    # cache_hit is priced at 0 by the estimator directly and never looked up
    # in MODEL_PRICING; every other route the router can emit must resolve.
    sample_decisions = [
        route_prompt("Hi there!", cache_keys=set()),
        route_prompt("Please analyze this report.", cache_keys=set()),
    ]
    priced_routes = {d.route for d in sample_decisions if d.route != "cache_hit"}
    assert priced_routes
    for route in priced_routes:
        assert route in MODEL_PRICING
