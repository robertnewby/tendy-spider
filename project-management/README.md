---
type: project-management-guide
project: tendy-spider
status: active
created: 2026-07-19
updated: 2026-07-19
tags:
  - project-management
  - tendy-spider
---

# Tendy Spider project management

## Authority boundary

This folder is an operational read model, not a competing project database.

| Concern | Authoritative source |
| --- | --- |
| Milestone scope, status, and acceptance | [[TASK]] |
| Architectural and product decisions | [[DECISIONS]] |
| Dataset coverage and licensing posture | [[docs/DATASET_MATRIX]] |
| Technical architecture | [[docs/ARCHITECTURE]] |
| Agent profiles and model assignments | [[docs/DEVELOPMENT_AGENTS]] |
| Operational views and next actions | This folder |

If a dashboard record conflicts with an authoritative source, update the
dashboard record. Do not silently rewrite the source from the dashboard.

No AgentOS vault data is included. The AgentOS vault informed only the
separation between a central view, detailed records, and linked artifacts.

## Workflow

```text
planned -> ready -> in-progress -> review -> done
                \-> blocked ----/
```

- `planned`: accepted work that is not ready to start.
- `ready`: dependencies are satisfied and work can be assigned.
- `in-progress`: one owner is actively executing the work.
- `blocked`: work cannot proceed; `blocked_reason` is required.
- `review`: implementation is complete and awaiting verification.
- `done`: acceptance evidence is recorded.
- `deferred`: explicitly outside the active delivery sequence.

Keep no more than three work items in progress at once. A work item needs one
owner, one next action, a milestone, and a source reference. Moving a Kanban
card requires changing the linked note's `status` property in the same edit.

## Main surfaces

- [[Dashboard]] — primary control surface.
- [[Project Portfolio.base]] — generated views over project records.
- [[Boards/Delivery Board]] — drag-and-drop execution view.
- `work-items/` — one Markdown record per actionable work item.
- `milestones/` — one linked record per `TASK.md` milestone.
- `decisions/` — operational records for open `DECISIONS.md` items.
- `risks/` — active project risks and mitigations.
- `templates/` — QuickAdd-compatible record templates.

## Commands

```bash
./scripts/install_obsidian_plugins.sh
python3 scripts/validate_project_dashboard.py
```

The plugin installer is reproducible and checksum-pinned. Community-plugin
runtime bundles are local-only and ignored by Git.
