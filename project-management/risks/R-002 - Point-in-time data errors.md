---
type: risk
id: R-002
project: tendy-spider
title: Point-in-time data errors
status: open
severity: critical
priority: P0
owner_agent: contracts_data_developer
decision_authority: lead_developer
next_action: Encode observation knowledge retrieval and transformation times in contracts
source_file: docs/ARCHITECTURE.md
source_ref: Backtesting requirements
created: 2026-07-19
updated: 2026-07-19
review_date:
tags:
  - project-management
  - risk
  - tendy-spider
---

# R-002 — Point-in-time data errors

## Risk

Restatements, revisions, ticker changes, universe drift, or corporate-action
handling could introduce look-ahead or survivorship bias.

## Mitigation

- [ ] #task Encode observation knowledge retrieval and transformation times in contracts

Golden tests must cover stale, missing, renamed, split-adjusted, revised, and
rate-limited cases before parity claims.
