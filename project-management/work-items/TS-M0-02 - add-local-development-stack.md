---
type: work-item
id: TS-M0-02
project: tendy-spider
title: Add local development stack
status: done
priority: P0
milestone: M0
owner_agent: platform_quality_developer
reviewer_agent: lead_developer
depends_on:
  - TS-M0-01
approval_required: false
blocked_reason: ""
next_action: Keep pinned container versions and health semantics aligned as Milestone 1 adds adapters
acceptance_evidence: "Exact make dev produced healthy Postgres and Redis containers and HTTP 200 ready API on 2026-07-21"
source_file: TASK.md
source_ref: Milestone 0 item 2
created: 2026-07-19
updated: 2026-07-21
due:
tags:
  - project-management
  - work-item
  - tendy-spider
---

# TS-M0-02 — Add local development stack

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

Docker Compose starts the local API dependencies with plain Postgres and Redis.
TimescaleDB remains deferred until measurements justify it.

## Next action

- [x] #task Add fixture-first Docker Compose for Postgres and Redis

## Acceptance

- [x] One documented command boots the stack.
- [x] Health checks surface failed dependencies.
- [x] No paid provider or live credential is required.

## Evidence

- Colima is running with the Docker runtime.
- `make dev` waited for healthy Postgres and Redis containers before starting
  the application processes.
- `/health/ready` returned HTTP 200 with Postgres, Redis, read-only API, and
  background jobs all `ready`.
