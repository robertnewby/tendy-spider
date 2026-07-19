# Decision Log

## Accepted

### D-001 — Clean-room workflow reproduction

Reproduce useful behaviors and interfaces between our own components. Do not copy TrendSpider's implementation, branding, UI assets, text, prompts, private APIs, or licensed data.

### D-002 — Cloud-native production, local-first development

Codex CLI develops and tests locally. Production ingestion, scheduling, durable storage, alerting, streaming, and long-running research jobs run as cloud services. The system must remain runnable locally with fixtures.

### D-003 — Provider-neutral data layer

Every source is behind a domain interface. Normalized models include provenance, timestamp, latency, adjustment, and license metadata. Provider substitution must not require rewriting agent prompts or domain logic.

### D-004 — Delayed/end-of-day before real-time

The first product slice favors accuracy, provenance, and low licensing cost over real-time breadth. Real-time SIP/OPRA/CME dependencies are deferred.

### D-005 — Deterministic analytics, LLM orchestration

The model selects and composes tools. Code calculates indicators, scans, rankings, and backtests. The model may explain results but must not invent or hand-calculate authoritative metrics.

### D-006 — Evidence is a product primitive

Each fact carries source identity, observation time, retrieval time, and transformation lineage. Answers surface citations and data freshness. Point-in-time datasets are mandatory for historical evaluation.

### D-007 — Read-only MVP

No real-money execution. Mutations such as watchlists and alerts arrive after read-only research and require confirmation plus audit logging.

### D-008 — No license selected

The repository is public but currently unlicensed. The owner must choose a software license before accepting external reuse or contributions.

## Open

### O-001 — Initial live price provider

Evaluate Alpaca, Twelve Data, Alpha Vantage, Polygon/Massive, Tiingo, and other candidates against commercial rights, coverage, latency, corporate actions, history, and price. Do not use an unofficial Yahoo Finance client as a production dependency.

### O-002 — LLM provider and model policy

Use a provider interface and evaluation suite. Select defaults only after measuring tool-call accuracy, latency, cost, context size, and citation fidelity.

### O-003 — Deployment target

Choose AWS, Azure, GCP, or a simpler managed platform after the vertical slice establishes workload shape. Keep Terraform/OpenTofu or equivalent infrastructure separable from application code.

### O-004 — Product identity

`Tendy Spider` is the repository name, not necessarily the launch brand. Conduct trademark and naming review before public release.
