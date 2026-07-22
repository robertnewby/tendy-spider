---
type: risk
id: R-001
project: tendy-spider
title: Market-data licensing constraints
status: open
severity: critical
priority: P0
owner_agent: contracts_data_developer
decision_authority: owner
next_action: Record rights and retention fields before enabling any live provider
source_file: docs/DATASET_MATRIX.md
source_ref: License checks still required
created: 2026-07-19
updated: 2026-07-19
review_date:
tags:
  - project-management
  - risk
  - tendy-spider
---

# R-001 — Market-data licensing constraints

## Risk

Public availability or a free tier may not permit commercial display, storage,
derived use, model use, or redistribution.

## Mitigation

- [ ] #task Record rights and retention fields before enabling any live provider

Keep provider-specific code behind interfaces and preserve source policy with
every observation.
