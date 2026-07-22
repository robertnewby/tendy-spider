---
type: risk
id: R-004
project: tendy-spider
title: Plugin view drift
status: open
severity: medium
priority: P2
owner_agent: platform_quality_developer
decision_authority: lead_developer
next_action: Run dashboard validation whenever project records or the delivery board change
source_file: DECISIONS.md
source_ref: D-011
created: 2026-07-19
updated: 2026-07-19
review_date:
tags:
  - project-management
  - risk
  - tendy-spider
---

# R-004 — Plugin view drift

## Risk

Kanban card position, note properties, and authoritative project files may drift
when edited independently.

## Mitigation

- [ ] #task Run dashboard validation whenever project records or the delivery board change

Bases reads note properties directly. The validator checks board lanes,
milestone source status, decision coverage, links, and plugin checksums.
