# Agent Instructions

## Mission

Build a clean-room, provider-neutral AI market-research assistant. The target is workflow equivalence to the useful parts of modern agentic trading research—not a pixel, prompt, brand, API, or data copy of TrendSpider Sidekick.

## Read order

Before changing code, read:

1. `README.md`
2. `TASK.md`
3. `DECISIONS.md`
4. `docs/SIDEKICK_ANALYSIS.md`
5. `docs/DATASET_MATRIX.md`
6. `docs/ARCHITECTURE.md`
7. `docs/SOURCES.md`

If implementation and documentation disagree, stop and update `DECISIONS.md` with the conflict and proposed resolution.

## Current state

The repository begins as a research/design handoff. The next agent should execute Milestone 0 in `TASK.md`, then continue through the vertical slice unless blocked by a material product decision or credential.

## Non-negotiable rules

- Use only public documentation, authorized APIs, user-provided data, or licensed providers.
- Do not scrape authenticated services, reverse engineer private endpoints, bypass technical controls, or reproduce proprietary prompts/UI text.
- Keep provider-specific code behind explicit interfaces. Core domain logic must not depend directly on a vendor SDK.
- Never commit credentials, tokens, account IDs, raw proprietary datasets, or generated `.env` files.
- Every externally sourced fact shown to a user must preserve source URL/identifier, observation timestamp, retrieval timestamp, and freshness/latency.
- Financial time series must be point-in-time safe. Avoid look-ahead bias, survivorship bias, silent split/dividend changes, and mixing preliminary with restated facts.
- Use UTC internally. Preserve the source timezone and market session metadata.
- Do not add real-money order execution in the MVP. Alerts and paper-trading adapters are acceptable only after the read-only slice is tested.
- Do not add a repository license without the owner's explicit choice.

## Product priorities

1. Evidence and data provenance
2. Correct tool execution and deterministic calculations
3. Clear uncertainty and freshness labels
4. Provider portability
5. Cost control and observability
6. UI polish

## Engineering defaults

- Prefer a typed monorepo with a Python analytics/API service and TypeScript web client, but record any change in `DECISIONS.md` before scaffolding a different stack.
- Define JSON-schema/Pydantic contracts before implementing a data adapter or agent tool.
- Keep LLM reasoning separate from deterministic calculations. Indicators, scans, rankings, and backtest metrics must be computed in code and returned to the model as structured data.
- Make tools idempotent where possible. Mutating actions such as watchlist changes or alerts require explicit confirmation and audit logging.
- Store raw immutable observations separately from normalized/derived tables.
- Use fixtures and recorded provider responses in tests; unit tests must not require network access or paid credentials.
- Add migrations for schema changes. Do not mutate production data manually.

## Required checks once code exists

Provide one top-level command for each:

- formatting
- linting
- type checking
- unit tests
- integration tests using fixtures
- local development startup

Document the exact commands in `README.md` and keep CI aligned with them.

## Completion discipline

For each milestone:

- update `TASK.md` status and acceptance evidence;
- record architectural choices in `DECISIONS.md`;
- update the data matrix if a source, license, or parity judgment changes;
- include tests for every deterministic tool;
- report what remains stubbed, paid, permissioned, or unverified.

Do not claim parity from a successful demo against a handful of tickers. Validate coverage, timestamps, corporate actions, missing data, and failure behavior.
