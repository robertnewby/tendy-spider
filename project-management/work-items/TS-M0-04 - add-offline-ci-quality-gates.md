---
type: work-item
id: TS-M0-04
project: tendy-spider
title: Add offline CI quality gates
status: done
priority: P0
milestone: M0
owner_agent: platform_quality_developer
reviewer_agent: lead_developer
depends_on:
  - TS-M0-01
approval_required: false
blocked_reason: ""
next_action: Keep CI aligned with root Make targets as the vertical slice grows
acceptance_evidence: "make check passed and CI invokes locked offline checks plus Gitleaks"
source_file: TASK.md
source_ref: Milestone 0 item 4
created: 2026-07-19
updated: 2026-07-19
due:
tags:
  - project-management
  - work-item
  - tendy-spider
---

# TS-M0-04 — Add offline CI quality gates

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

Formatting, linting, type checking, unit tests, fixture integration tests, and
secret scanning run through documented top-level commands aligned with CI.

## Next action

- [x] #task Define top-level formatting lint typing unit integration and secret-scan commands

## Acceptance

- [x] One command runs every offline check.
- [x] Unit and integration tests use fixtures only.
- [x] CI and README commands match.
- [x] Secret scanning covers committed and proposed files.

## Evidence

- `make check`
- `.github/workflows/ci.yml`
- `tests/integration/test_contract_fixture_boundary.py`
