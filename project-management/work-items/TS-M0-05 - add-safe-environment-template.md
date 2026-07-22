---
type: work-item
id: TS-M0-05
project: tendy-spider
title: Add safe environment template
status: done
priority: P1
milestone: M0
owner_agent: platform_quality_developer
reviewer_agent: lead_developer
depends_on:
  - TS-M0-01
approval_required: false
blocked_reason: ""
next_action: Add future provider variable names only after an adapter is approved
acceptance_evidence: ".env.example contains blank local configuration names and no working secrets"
source_file: TASK.md
source_ref: Milestone 0 item 5
created: 2026-07-19
updated: 2026-07-19
due:
tags:
  - project-management
  - work-item
  - tendy-spider
---

# TS-M0-05 — Add safe environment template

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

Provide `.env.example` with configuration names and safe documentation but no
working secrets, account identifiers, or provider credentials.

## Next action

- [x] #task Add an env example containing variable names and safe descriptions only

## Acceptance

- [x] No secret or realistic token value appears.
- [x] Variables map to documented local services and optional adapters.
- [x] Fixture-driven development works without a copied `.env`.
