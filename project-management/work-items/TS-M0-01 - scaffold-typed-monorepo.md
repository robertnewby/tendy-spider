---
type: work-item
id: TS-M0-01
project: tendy-spider
title: Scaffold typed monorepo
status: done
priority: P0
milestone: M0
owner_agent: lead_developer
reviewer_agent: solution_architect
depends_on: []
approval_required: false
blocked_reason: ""
next_action: Begin the Milestone 1 fixture-adapter slice after the M0 Docker smoke
acceptance_evidence: "make check passed; make dev-apps served API and web locally on 2026-07-19"
source_file: TASK.md
source_ref: Milestone 0 item 1
created: 2026-07-19
updated: 2026-07-19
due:
tags:
  - project-management
  - work-item
  - tendy-spider
---

# TS-M0-01 — Scaffold typed monorepo

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

Create `apps/web`, `services/api`, `packages/contracts`, `infra`, and
`tests/fixtures` with explicit package boundaries and top-level commands.

## Next action

- [x] #task Define package boundaries and scaffold the root workspace

## Acceptance

- [x] Web shell starts locally.
- [x] API health endpoint responds locally.
- [x] Shared contracts have one canonical home.
- [x] Fixture and infrastructure directories are documented.

## Evidence

- `make check`
- `make dev-apps`
- HTTP 200 from `/health/live` and the web root
- HTTP 503 with explicit unavailable dependencies from `/health/ready`

## Ownership

Lead integrates root files. Backend, frontend, contracts/data, and
platform/quality profiles own their bounded package areas after the scaffold.
