# TrendSpider Sidekick Analysis

Last verified: **2026-07-18**

## What Sidekick is

Sidekick is best understood as an agent layer embedded in TrendSpider's market-data and trading-research platform. The differentiator is not a unique foundation model. TrendSpider states that Sidekick uses Anthropic/Claude by default, with Gemini and ChatGPT on higher tiers. Its advantage is tool and context access: charts, data, scanners, watchlists, alerts, backtests, filings, news, and alternative datasets.

Publicly described capabilities include:

- reading the open chart's symbol, price action, indicators, drawings, levels, and timeframe;
- querying fundamentals, SEC filings, earnings transcripts, analyst activity, insider and Congressional transactions, and news;
- comparing and ranking multiple symbols;
- running market scans;
- creating alerts and editing watchlists;
- explaining backtest results;
- generating custom indicators;
- performing multi-symbol “Deep Research” with a symbol-focused sub-agent per name and a parent synthesis.

TrendSpider's Deep Research announcement explicitly says the main chat retains scanning, alerts, watchlists, chart analysis, and backtest explanation. It also describes one background analyst per symbol, followed by a compiled response.

## Functional decomposition

| Layer | What must be recreated | Difficulty |
|---|---|---|
| Conversation | Threads, streaming answers, context limits, citations | Moderate |
| Agent orchestration | Tool selection, planning, confirmation, retries, budgets | Moderate-high |
| Chart context | Symbol, timeframe, visible bars, indicators, drawings, selections | Moderate |
| Deterministic analytics | Indicators, comparisons, rankings, scanners | Moderate |
| Research retrieval | Filings, transcripts, fundamentals, news, macro, alternative data | High because of normalization and licensing |
| Stateful actions | Watchlists, alerts, saved artifacts | Moderate; requires confirmation/audit |
| Backtesting | Point-in-time engine, costs, corporate actions, bias controls | High |
| Deep research | Fan-out jobs, evidence merge, cancellation, cost limits | High |
| Real-time breadth | SIP/NBBO, OPRA, futures, indexes, social/flow feeds | Very high and license-bound |

## Can it be duplicated?

### Yes, functionally

The interaction pattern is reproducible with current LLM tool-calling APIs and conventional cloud components. No model training is required for an MVP. A strong implementation can deliver chart-aware conversation, filings/fundamental research, deterministic indicators, scans, alerts, comparisons, and bounded multi-agent research.

### No, not exactly

Exact output and coverage depend on TrendSpider's private orchestration, normalized history, proprietary/third-party feeds, automated technical-analysis algorithms, platform integrations, and UX. Some feeds carry exchange and vendor rights that cannot be cloned by scraping or copying. TrendSpider also identifies a US patent on its site; feature-level legal review is appropriate before imitating distinctive automated-charting behavior.

The right target is clean-room workflow equivalence with independent product design and legitimately sourced data.

## What is actually hard

1. **Symbol master and temporal identity.** Tickers change, securities delist, share classes differ, and the same token can mean different assets across venues.
2. **Point-in-time correctness.** Restated financials, revised macro data, index membership, earnings calendars, and corporate actions create look-ahead and survivorship traps.
3. **Licensing.** Display, derived-use, storage, redistribution, non-professional status, and real-time rights differ by feed.
4. **Data quality.** Vendor feeds disagree on timestamps, adjustments, estimates, and event classification.
5. **Tool reliability.** A fluent answer is worthless if it silently uses stale, incomplete, or mismatched inputs.
6. **Backtest integrity.** Costs, execution assumptions, bar construction, universe history, and future leakage must be explicit.
7. **Long-running research.** Fan-out work needs budgets, cancellation, retries, partial results, and evidence-preserving synthesis.

## Is it a cloud task?

Production is primarily a cloud task:

- continuous/scheduled ingestion;
- durable time-series and document storage;
- background research queues;
- distributed scanner and alert execution;
- WebSocket/SSE streaming;
- model and provider credential management;
- monitoring, cost controls, and audit logs.

Local development remains valuable for UI work, fixture-driven analytics, contract tests, and small backtests. The proposed architecture keeps both modes.

## Safe competitive-research boundary

Allowed and useful:

- public product pages and documentation;
- ordinary user-visible behavior observed through an authorized account;
- independent benchmarks using the same public facts;
- clean-room implementation from documented behavior;
- legitimate public, user-supplied, or licensed data.

Out of bounds:

- bypassing authentication or technical controls;
- probing private endpoints or extracting proprietary prompts;
- copying code, assets, substantial UI text, or restricted datasets;
- using a personal market-data license for unapproved commercial redistribution;
- presenting approximations as feed parity.

## Primary evidence

- [TrendSpider Market Data Library](https://trendspider.com/marketdata/)
- [TrendSpider Market Data Sources](https://help.trendspider.com/kb/data-feeds/market-data-sources)
- [Introducing Sidekick Deep Research](https://trendspider.com/blog/introducing-sidekick-deep-research/)
- [TrendSpider comparison page describing Sidekick context and model choices](https://trendspider.com/learning-center/tc2000-alternative/)
- [TrendSpider comparison page describing Sidekick research sources and actions](https://trendspider.com/learning-center/tipranks-alternative/)

Vendor marketing pages are evidence of claimed capabilities, not independent proof of quality or completeness.
