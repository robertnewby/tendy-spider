# Tendy Spider

Clean-room implementation of an evidence-backed AI market-research assistant
inspired by the workflow category represented by TrendSpider Sidekick.

The repository contains the Milestone 0 application foundation. It does **not**
contain TrendSpider code, prompts, private APIs, copied UI assets, licensed
market data, or real-money execution.

## Bottom line

- A functionally similar product can be built with an LLM tool orchestrator, chart context, normalized financial data, scanners, alerts, backtests, watchlists, and evidence-backed research.
- Exact duplication is neither realistic nor the goal. Real-time consolidated US equities, OPRA options, CME futures, analyst consensus, unusual-options classification, Nasdaq retail activity, and broad index coverage require licenses or paid vendors.
- TrendSpider's public catalog currently identifies 27 data families, excluding user-supplied data. This audit finds 11 with useful direct public/free substitutes, 8 more that can be approximated for free, and 8 that are not reasonably reproducible at useful parity without paid or permissioned access. See [docs/DATASET_MATRIX.md](docs/DATASET_MATRIX.md).
- The production system is a cloud workload. Codex CLI can build and test it locally, while scheduled ingestion, durable storage, streaming updates, alerts, and agent jobs belong in cloud infrastructure.
- The current implementation provides provider-neutral contracts, a typed Python
  health API, an evidence-first TypeScript web shell, fixture-only checks, CI,
  and a local Postgres/Redis Compose stack.

## Local development

Requirements: Node.js 22+, npm 11+, Python 3.11+, uv, and Docker Compose.

```bash
make bootstrap
make check
make dev
```

`make dev` starts Postgres, Redis, the API, and the web shell. The local
endpoints are:

- web workspace: `http://127.0.0.1:5173`
- API liveness: `http://127.0.0.1:8000/health/live`
- API readiness: `http://127.0.0.1:8000/health/ready`

Postgres is required for API readiness. If only Redis is unavailable, the
read-only API reports `degraded` and background jobs report `unready`.

### Required commands

| Check | Command |
|---|---|
| Install locked dependencies | `make bootstrap` |
| Format | `make format` |
| Verify formatting | `make format-check` |
| Lint | `make lint` |
| Type check | `make typecheck` |
| Unit tests | `make unit` |
| Fixture integration tests | `make integration` |
| All offline checks | `make check` |
| Start the complete local stack | `make dev` |
| Start only API and web processes | `make dev-apps` |
| Stop local infrastructure | `make dev-down` |

Set `API_RELOAD=1` for Uvicorn auto-reload. `.env.example` documents safe
configuration names and intentionally contains no working credentials.

## Repository map

- [AGENTS.md](AGENTS.md) — durable instructions for coding agents
- [TASK.md](TASK.md) — executable milestones and acceptance criteria
- [DECISIONS.md](DECISIONS.md) — architectural decisions and unresolved choices
- [docs/SIDEKICK_ANALYSIS.md](docs/SIDEKICK_ANALYSIS.md) — capability and duplication analysis
- [docs/DATASET_MATRIX.md](docs/DATASET_MATRIX.md) — all 27 data families and replacement options
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — proposed system design and contracts
- [docs/ARCHITECTURE_ARTIFACTS.md](docs/ARCHITECTURE_ARTIFACTS.md) — diagram,
  deck, and Google Slides production standard
- [docs/DEVELOPMENT_AGENTS.md](docs/DEVELOPMENT_AGENTS.md) — Codex developer profiles and coordination rules
- [docs/SOURCES.md](docs/SOURCES.md) — evidence ledger and primary-source links
- `apps/web` — dependency-light TypeScript research-workspace shell
- `services/api` — FastAPI health and future orchestration boundary
- `packages/contracts` — canonical JSON Schema and Pydantic contracts
- `infra` — pinned local Postgres and Redis Compose services
- `tests` — redistributable fixtures and offline integration checks

## Project management dashboard

The repository root is also an Obsidian vault. Open
[project-management/Dashboard.md](project-management/Dashboard.md) for the
project control surface. `TASK.md`, `DECISIONS.md`, and the technical source
documents remain authoritative; the dashboard is a validated operational view.

Install the pinned local Obsidian plugins:

```bash
./scripts/install_obsidian_plugins.sh
```

Validate project-management records, links, board state, and plugin files:

```bash
python3 scripts/validate_project_dashboard.py
```

## Intended first product slice

The first slice is a read-only US-equity research assistant using delayed/end-of-day prices plus free SEC, FRED, FINRA, and issuer data. It should answer with timestamps, source citations, and explicit data-freshness labels. Real-time feeds, order execution, and expensive alternative data come later behind provider interfaces.

## Boundaries

- Clean-room implementation only; reproduce workflows, not proprietary expression.
- Never scrape authenticated TrendSpider pages or bypass access controls.
- Do not ingest or redistribute a feed until its license and retention rights are recorded.
- Treat all generated market commentary as research support, not investment advice.
- No live order placement in the MVP.

No software license has been selected yet. Do not add one without the owner's decision.
