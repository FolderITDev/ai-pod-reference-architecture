# Project Status

**Status: Reference — static, unsupported.**

This repository is a reference architecture, not a maintained product. Read the boundary below before depending on anything here.

## What that means

- **Static.** It is versioned and published as a reference point. It is not under active feature development.
- **Unsupported.** There is no support commitment and no SLA. Issues may remain open as a reference template rather than a work queue.
- **Not production software.** The one runnable module (the token-cost estimator) is a deterministic, offline model intended to be read and reproduced, not deployed as a dependency.
- **No security guarantees.** Do not send real credentials, internal URLs, hostnames, or production data through anything in this repo. All examples use `example.com` and anonymized data on purpose.

## What it is for

- Documenting how a Managed AI Pod structures LLM request routing and cost control.
- Letting anyone reproduce the cost figures in the benchmark for themselves.
- Serving as a blueprint to read and adapt.

## Versioning

Changes, if any, are recorded per release. The pricing table used by the estimator is a dated snapshot; see [`docs/decision_records/sources.md`](docs/decision_records/sources.md) for the date and sources. Re-running the benchmark against current prices is expected and encouraged.

## Contact

Maintained by [Folder IT](https://example.com) as a reference. For questions about Managed AI Pods, use the contact channels on the website rather than repository issues.
