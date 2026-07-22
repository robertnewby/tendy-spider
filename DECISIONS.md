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

### D-009 — Bounded developer subagents

Use project-scoped Codex profiles for lead integration, contracts/data, backend,
frontend, and platform/quality work. The main thread owns decomposition and
integrated verification. Parallel writes require non-overlapping file ownership,
shared contracts and root documentation are serialized, and recursive subagent
spawning remains disabled.

### D-010 — Source-first architecture artifacts and Google Slides delivery

Keep editable repository sources authoritative for architecture diagrams and
decks. Use Mermaid with C4 semantics by default, a deterministic validated
render for delivery, and the Codex Presentations workflow for editable PPTX
generation and slide-level visual QA. Import verified net-new decks as native
Google Slides through the Google Drive connector; edit existing native Slides
decks in place while keeping repository source synchronized. Use the
`solution_architect` profile and
`create-architecture-artifacts` project skill for this work.

### D-011 — Repository-native project-management read model

Use the repository root as an Obsidian vault and keep the project-management
dashboard under `project-management/`. `TASK.md` remains authoritative for
milestone scope, status, and acceptance criteria; `DECISIONS.md` remains
authoritative for decisions; technical matrices and architecture documents
remain authoritative for their domains. Dashboard records are linked,
validated operational views and must not override those sources.

Use Obsidian Bases and Properties as the primary data/view layer. Tasks,
QuickAdd, and Kanban are optional interaction plugins installed from pinned
official releases. Keep third-party runtime bundles out of Git, retain
checksums and a reproducible installer, and do not import AgentOS vault data.

### D-012 — Milestone 0 workspace and toolchain baseline

Use npm workspaces with Node.js 22+ for the TypeScript client and uv with
Python 3.11+ for the API and canonical contracts. Use FastAPI for the initial
typed HTTP boundary, strict TypeScript and mypy settings, JSON Schema 2020-12
plus Pydantic for portable contracts, and one root `Makefile` command surface.
Lock application and quality dependencies. Keep tests fixture-only and
independent of Docker, provider credentials, and paid services.

Use plain Postgres and non-authoritative Redis for the local data and
coordination plane. Their Compose images are pinned. A future framework,
database extension, queue, or monorepo-tool change requires evidence that this
baseline is insufficient.

### D-013 — Dependency-aware health and local browser policy

Expose process-only liveness at `GET /health/live` and dependency-aware
readiness at `GET /health/ready`, with `GET /health` as an alias. Postgres loss
makes the API `unready` and returns HTTP 503. Redis loss with Postgres available
returns HTTP 200 `degraded`: read-only research remains degraded while
background jobs remain unready.

Health payloads use UTC timestamps and explicit dependency and capability
states. They are operational DTOs rather than market-data evidence contracts.
Permit browser access only from explicitly configured origins; the default
allowlist contains the two local web origins, does not use a wildcard, and does
not allow credentials.

## Open

### O-001 — Initial live price provider

Evaluate Alpaca, Twelve Data, Alpha Vantage, Polygon/Massive, Tiingo, and other candidates against commercial rights, coverage, latency, corporate actions, history, and price. Do not use an unofficial Yahoo Finance client as a production dependency.

### O-002 — LLM provider and model policy

Use a provider interface and evaluation suite. Select defaults only after measuring tool-call accuracy, latency, cost, context size, and citation fidelity.

### O-003 — Deployment target

Choose AWS, Azure, GCP, or a simpler managed platform after the vertical slice establishes workload shape. Keep Terraform/OpenTofu or equivalent infrastructure separable from application code.

### O-004 — Product identity

`Tendy Spider` is the repository name, not necessarily the launch brand. Conduct trademark and naming review before public release.

### O-005 — Architecture presentation template and visual identity

Use the default Codex presentation design system until the owner selects a
durable Google Slides template, logo, fonts, and brand palette. The first
accepted template should become a rights-cleared project asset and must not
change architecture semantics.
