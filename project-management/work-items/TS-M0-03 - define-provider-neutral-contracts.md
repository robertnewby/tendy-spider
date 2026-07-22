---
type: work-item
id: TS-M0-03
project: tendy-spider
title: Define provider-neutral contracts
status: done
priority: P0
milestone: M0
owner_agent: contracts_data_developer
reviewer_agent: lead_developer
depends_on: []
approval_required: false
blocked_reason: ""
next_action: Extend the canonical contracts only when a Milestone 1 adapter requires it
acceptance_evidence: "Contract unit and fixture integration tests passed in make check on 2026-07-19"
source_file: TASK.md
source_ref: Milestone 0 item 3
created: 2026-07-19
updated: 2026-07-19
due:
tags:
  - project-management
  - work-item
  - tendy-spider
---

# TS-M0-03 — Define provider-neutral contracts

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

Define canonical contracts for symbol identity, prices, corporate facts,
filings, macro observations, documents, evidence, and provenance before any
live adapter.

## Next action

- [x] #task Define the provenance and timestamp primitives before domain payloads

## Acceptance

- [x] Observation time, knowledge time, and retrieval time are distinct.
- [x] Source identity and freshness are required.
- [x] Adjustment and license metadata are representable.
- [x] Normalized contracts do not import a vendor SDK.

## Evidence

- Canonical JSON Schema 2020-12 catalog under `packages/contracts/schemas/`
- Strict Pydantic validation and deterministic JSON round trips
- Valid and invalid fixtures for stale, renamed, split, restated, short-volume,
  missing-source, naive-time, and silent-adjustment cases
