# Tendy Spider

Clean-room research and implementation plan for an AI market-research assistant inspired by the workflow category represented by TrendSpider Sidekick.

This repository is a handoff package for Codex CLI. It does **not** contain TrendSpider code, prompts, private APIs, copied UI assets, or licensed market data.

## Bottom line

- A functionally similar product can be built with an LLM tool orchestrator, chart context, normalized financial data, scanners, alerts, backtests, watchlists, and evidence-backed research.
- Exact duplication is neither realistic nor the goal. Real-time consolidated US equities, OPRA options, CME futures, analyst consensus, unusual-options classification, Nasdaq retail activity, and broad index coverage require licenses or paid vendors.
- TrendSpider's public catalog currently identifies 27 data families, excluding user-supplied data. This audit finds 11 with useful direct public/free substitutes, 8 more that can be approximated for free, and 8 that are not reasonably reproducible at useful parity without paid or permissioned access. See [docs/DATASET_MATRIX.md](docs/DATASET_MATRIX.md).
- The production system is a cloud workload. Codex CLI can build and test it locally, while scheduled ingestion, durable storage, streaming updates, alerts, and agent jobs belong in cloud infrastructure.

## Start here in Codex CLI

```bash
git clone https://github.com/robertnewby/tendy-spider.git
cd tendy-spider
codex
```

Suggested first prompt:

> Read AGENTS.md, README.md, TASK.md, DECISIONS.md, and every file under docs/. Summarize the constraints and open decisions, then execute Milestone 0 from TASK.md. Do not add a paid data dependency or live-trading capability without explicit approval.

## Repository map

- [AGENTS.md](AGENTS.md) — durable instructions for coding agents
- [TASK.md](TASK.md) — executable milestones and acceptance criteria
- [DECISIONS.md](DECISIONS.md) — architectural decisions and unresolved choices
- [docs/SIDEKICK_ANALYSIS.md](docs/SIDEKICK_ANALYSIS.md) — capability and duplication analysis
- [docs/DATASET_MATRIX.md](docs/DATASET_MATRIX.md) — all 27 data families and replacement options
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — proposed system design and contracts
- [docs/SOURCES.md](docs/SOURCES.md) — evidence ledger and primary-source links

## Intended first product slice

The first slice is a read-only US-equity research assistant using delayed/end-of-day prices plus free SEC, FRED, FINRA, and issuer data. It should answer with timestamps, source citations, and explicit data-freshness labels. Real-time feeds, order execution, and expensive alternative data come later behind provider interfaces.

## Boundaries

- Clean-room implementation only; reproduce workflows, not proprietary expression.
- Never scrape authenticated TrendSpider pages or bypass access controls.
- Do not ingest or redistribute a feed until its license and retention rights are recorded.
- Treat all generated market commentary as research support, not investment advice.
- No live order placement in the MVP.

No software license has been selected yet. Do not add one without the owner's decision.
