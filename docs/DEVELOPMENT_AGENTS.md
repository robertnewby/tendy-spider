# Project Subagent Profiles

Tendy Spider provides six project-scoped Codex profiles under `.codex/agents/`:
five engineering profiles and one architecture-artifact specialist. They divide
ownership while the main thread or `lead_developer` retains integration
responsibility.

## Profiles

| Profile | Model | Effort | Primary ownership |
|---|---|---|---|
| `lead_developer` | `gpt-5.6-sol` | `high` | Decomposition, integration, shared decisions, acceptance evidence |
| `backend_developer` | `gpt-5.6-terra` | `high` | Python API, orchestration, persistence, provider interfaces |
| `frontend_developer` | `gpt-5.6-terra` | `medium` | TypeScript research workspace and evidence UI |
| `contracts_data_developer` | `gpt-5.6-sol` | `high` | Schemas, canonical data models, provenance, migrations |
| `platform_quality_developer` | `gpt-5.6-terra` | `high` | Local stack, CI, developer commands, security and integrity tests |
| `solution_architect` | `gpt-5.6-sol` | `high` | Architecture reconciliation, diagrams, artifact QA, and Google Slides-ready decks |

The profiles pin their model and reasoning effort while inheriting the parent
session's tools and permission mode. Project settings in `.codex/config.toml`
allow at most four concurrent threads and keep nesting at one level, so
subagents cannot recursively spawn more agents.

## Coordination rules

1. The main thread defines the requirement, assigns file ownership, and remains
   accountable for the integrated result.
2. Delegate only bounded work that can proceed independently. Prefer parallel
   exploration and verification; serialize changes to shared contracts and root
   documentation.
3. Inspect the worktree before assigning or editing. Existing changes belong to
   their current owner until coordinated otherwise.
4. `contracts_data_developer` owns canonical schema changes. Backend and frontend
   agents propose contract needs instead of creating local competing types.
5. `lead_developer` owns `TASK.md`, `DECISIONS.md`, and final cross-package
   acceptance evidence unless it delegates one of those files explicitly.
6. Each subagent reports changed files, checks run, skipped checks, assumptions,
   and unresolved dependencies. The lead verifies the integrated work rather
   than treating subagent summaries as proof.
7. No profile may approve a paid provider, a software license, real-money
   execution, or a new product/deployment commitment.
8. `solution_architect` owns durable architecture visuals and decks when
   assigned. It uses the project-scoped `create-architecture-artifacts` skill,
   keeps editable sources authoritative, and does not implement application code
   unless the lead assigns a bounded change.

## Recommended use by milestone

### Milestone 0

- Lead: scaffold and integrate the monorepo.
- Contracts/data: define provider-neutral schemas first.
- Backend: build the health endpoint and consume shared contracts.
- Frontend: build the web shell and consume shared contracts.
- Platform/quality: add Compose, CI, top-level commands, and offline checks.

Contract work should land before dependent backend and frontend changes.
Infrastructure and web/API shells can otherwise proceed in parallel when file
ownership does not overlap.

### Milestone 1

- Contracts/data defines adapter and evidence payloads.
- Backend implements fixture adapters before live adapters.
- Platform/quality adds golden cases and point-in-time failure tests.
- Frontend exposes citations, freshness, and partial-result states.
- Lead verifies the two-symbol comparison end to end.

### Later milestones

Use the same profiles for chart context, scanner, alerts, backtests, and deep
research. Use `solution_architect` when a milestone needs decision views,
cross-system flows, or an architecture review deck. Create another specialist
profile only after repeated work demonstrates a distinct ownership boundary and
evaluation need.

## Example requests

```text
Use the contracts_data_developer to define the Milestone 0 contracts. In
parallel, use the platform_quality_developer to scaffold offline CI. Keep all
root documentation edits in the main thread. Wait for both agents, integrate
their work, and run the repository checks.
```

```text
Use backend_developer for the fixture price adapter and
platform_quality_developer for an independent point-in-time test review. Assign
non-overlapping files, wait for both, then have lead_developer verify the
integrated acceptance criteria.
```

```text
Use solution_architect with gpt-5.6-sol/high to reconcile the current
architecture, create the minimum context, container, workflow, and data-flow
views, and produce a verified Google Slides review deck. Keep application code
out of scope and return the artifact register, deck link, QA evidence, and open
decisions.
```
