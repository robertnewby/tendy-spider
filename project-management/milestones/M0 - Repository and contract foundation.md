---
type: milestone
id: M0
project: tendy-spider
title: Repository and contract foundation
status: done
priority: P0
owner_agent: lead_developer
progress: 100
source_file: TASK.md
source_status: done
created: 2026-07-19
updated: 2026-07-21
target_date:
acceptance_evidence: "make check passed; exact make dev reached healthy Postgres and Redis plus HTTP 200 ready API on 2026-07-21"
tags:
  - project-management
  - milestone
  - tendy-spider
---

# M0 — Repository and contract foundation

## Source

[[TASK#Milestone 0 — Repository and contract foundation]]

## Outcome

A typed monorepo, local fixture-based stack, provider-neutral contracts, and
offline quality gates provide a safe foundation for the first product slice.

## Acceptance gate

- One documented command boots the local stack.
- One documented command runs all offline checks.
- API health endpoint and web shell work locally.
- Contracts enforce timestamps, source identifiers, and freshness.
- Tests need no live provider credential.

## Work

- [[project-management/work-items/TS-M0-01 - scaffold-typed-monorepo]]
- [[project-management/work-items/TS-M0-02 - add-local-development-stack]]
- [[project-management/work-items/TS-M0-03 - define-provider-neutral-contracts]]
- [[project-management/work-items/TS-M0-04 - add-offline-ci-quality-gates]]
- [[project-management/work-items/TS-M0-05 - add-safe-environment-template]]

## Acceptance evidence

- `make check` passes all locked offline quality gates.
- `make dev-apps` starts the API and web shell; liveness, truthful unready
  readiness, web delivery, and local CORS were smoke-tested.
- Contract fixtures validate source, time, freshness, adjustment, policy, and
  lineage semantics without provider credentials.
- The exact `make dev` command started healthy Postgres and Redis containers,
  then started the API and web shell. `/health/ready` returned HTTP 200 `ready`
  with both dependencies and both capabilities ready.
