# Execution Plan

## Objective

Deliver a usable, read-only vertical slice of an evidence-backed US-equity research assistant, then expand it without coupling the product to one LLM or market-data provider.

## Milestone 0 — Repository and contract foundation

Status: **next**

1. Scaffold a monorepo with:
   - `apps/web` — TypeScript web client
   - `services/api` — Python API and agent orchestration
   - `packages/contracts` — generated/shared schemas
   - `infra` — local containers and deployment templates
   - `tests/fixtures` — small, redistributable test fixtures
2. Add local development with Docker Compose for Postgres and Redis. TimescaleDB is optional; prefer plain Postgres until measurements justify an extension.
3. Define provider-neutral contracts for:
   - symbol identity and mapping
   - OHLCV bars and quotes
   - corporate facts and filings
   - macro observations
   - news/documents
   - tool evidence and provenance
4. Add CI for formatting, linting, typing, unit tests, and secret scanning.
5. Add `.env.example` containing names only, never working secrets.

Acceptance criteria:

- One documented command boots the local stack.
- One documented command runs all offline checks.
- API health endpoint and web shell work locally.
- Contracts validate timestamps, source identifiers, and freshness.
- No live provider credential is required by tests.

## Milestone 1 — Free-data vertical slice

Status: **planned**

Implement read-only adapters for:

- SEC EDGAR submissions and Company Facts/XBRL
- FRED observations
- FINRA daily short-sale volume
- a configurable delayed/end-of-day US-equity price provider

Price-provider rule: implement the interface and fixture adapter first. Before selecting a live provider, document its personal/commercial terms, rate limits, redistribution rights, corporate-action behavior, and coverage. Do not silently rely on an unofficial scraper.

Agent tools:

- `resolve_symbol`
- `get_price_bars`
- `compute_indicators`
- `get_company_facts`
- `search_filings`
- `get_macro_series`
- `get_short_volume`
- `compare_symbols`

Acceptance criteria:

- A user can ask for a two-symbol comparison and receive deterministic calculations plus citations.
- Answers label delayed/end-of-day data and show observation/retrieval timestamps.
- Missing or stale data produces an explicit partial result, not fabricated values.
- Tool traces are stored without exposing chain-of-thought.
- Golden tests cover at least one normal, stale, missing, renamed, split-adjusted, and rate-limited case.

## Milestone 2 — Chart context and research workspace

Status: **planned**

- Candlestick/line chart with symbol, timeframe, visible range, indicators, drawings, and selected points represented as a structured `ChartContext` object.
- Conversation threads linked to a workspace and watchlist.
- Evidence drawer showing exact source documents and timestamps.
- Saved research artifacts and reproducible comparison tables.

Acceptance criteria:

- The agent receives chart state as structured values, not a screenshot when structured state exists.
- Changing the visible range changes tool inputs and is visible in the audit trail.
- Every chart series identifies adjustment mode and data provider.

## Milestone 3 — Scanner, alerts, and backtest explanation

Status: **planned**

- Typed scan DSL compiled to deterministic query/execution code.
- Scheduled alerts with confirmation, throttling, deduplication, and audit history.
- Event-driven backtest engine with costs, slippage, benchmark, trade log, and point-in-time controls.
- LLM explains results but never computes performance metrics itself.

Acceptance criteria:

- Scanner and backtest results are reproducible from stored inputs and code version.
- Tests demonstrate no future-data leakage.
- Alert delivery is idempotent and can be disabled globally.

## Milestone 4 — Multi-symbol deep research

Status: **planned**

- Parent research job decomposes a bounded universe into symbol-level jobs.
- Concurrency, token, provider-call, and dollar budgets are enforced.
- Sub-results retain independent evidence; the synthesis cites them.
- Cancellation, retry, partial completion, and resume are supported.

## Deferred paid-parity work

Do not implement until the owner approves vendor spend and licensing:

- full consolidated real-time US equities/NBBO
- OPRA options chains and historical options trades
- real-time CME/NYMEX/COMEX/CBOT futures
- broad analyst estimates and ratings history
- unusual-options-flow classification
- Nasdaq retail trading activity
- Nasdaq Global Index universe
- production StockTwits firehose/derived sentiment

## Product decisions required before public launch

- commercial vs personal/internal use
- supported countries and investor classifications
- chosen data licenses and redistribution rights
- model/provider budget and retention policy
- financial-content disclaimers and legal review
- repository software license
- whether paper trading is in scope
