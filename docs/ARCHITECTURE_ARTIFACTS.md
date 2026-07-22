# Architecture Artifact System

This document defines the source-first workflow for Tendy Spider architecture
diagrams and presentation decks. `docs/ARCHITECTURE.md` remains the canonical
architecture narrative; this file records the visual toolchain and durable
artifact inventory.

## Adopted toolchain

1. **Architecture semantics:** use C4-style context, container, and component
   boundaries, supplemented by user workflow, data flow, integration sequence,
   deployment, and trust-boundary views.
2. **Repository diagrams:** use Mermaid source by default. Use ordinary
   flowcharts with C4 semantics rather than experimental Mermaid C4 syntax.
   Reserve Graphviz DOT for dense topology and draw.io for an explicit
   drag-and-drop editing requirement.
3. **Diagram validation:** keep editable source and a reviewed SVG or PNG.
   Validate syntax with a deterministic local renderer and inspect the final
   render. A source-only diagram remains draft.
4. **Deck creation:** use the installed Codex Presentations skill for editable
   PPTX generation, slide rendering, and visual QA.
5. **Google Slides delivery:** import a verified PPTX as native Google Slides
   through the Google Drive connector. Edit an existing native Slides deck
   directly, verify its revision before material updates, and backport all
   connector-side changes to repository source.
6. **Ownership:** assign architecture artifacts to `solution_architect`, using
   the project skill at `.agents/skills/create-architecture-artifacts/`.

The local environment does not currently expose `mmdc`, Graphviz `dot`, or the
draw.io desktop CLI. Standalone diagram exports must remain draft until the
canonical source renders successfully with a deterministic renderer. A
slide-native reconstruction is not a substitute for validating the canonical
diagram source. Add any renderer as a pinned project development dependency
when the Milestone 0 toolchain exists; do not depend on an unversioned global
install or an unapproved remote rendering service.

## Capability status

Checked **2026-07-19**:

- the project skill passes the official Codex skill validator;
- all six custom-agent TOML files parse, and Codex strict configuration loading
  succeeds;
- the Google Drive plugin is installed, the Slides search path is authorized,
  and the native Slides import action is exposed;
- no file was created merely to probe Drive write access, so the import write
  path remains unverified until the first real, reviewed deck is delivered;
- standalone Mermaid, Graphviz, and draw.io renderers are not provisioned;
- three Milestone 0 Mermaid sources pass structural text checks and remain
  drafts pending deterministic rendering and visual QA.

## GitHub skill and plugin review

Observation date: **2026-07-19**. Retrieval date: **2026-07-19**. Freshness:
point-in-time GitHub snapshot; recheck the repository, license, dependencies,
and current Codex catalog before any future installation.

| Candidate | Useful capability | Decision |
|---|---|---|
| [Agents365 `mermaid-skill`](https://github.com/Agents365-ai/mermaid-skill) | Text diagrams, syntax validation, export, and visual self-review | Do not install. Adopt the validation loop in the project skill; avoid its optional remote-rendering fallback and wait for a pinned local renderer. |
| [Agents365 `drawio-skill`](https://github.com/Agents365-ai/drawio-skill) | Polished, manually editable diagrams with strong layout repair | Keep optional. Use only when ongoing manual editing or specialized stencils justify XML and a desktop dependency. |
| [`markdown-viewer/skills`](https://github.com/markdown-viewer/skills) | Broad PlantUML, architecture, chart, and infographic catalog | Do not install. Its renderer-specific output and broad scope add context and licensing complexity without improving the Google Slides path. |
| [`wshobson/agents` C4 plugin](https://github.com/wshobson/agents/tree/main/plugins/c4-architecture) | Separate agents for C4 zoom levels | Do not install. One project architect with stable cross-view semantics is easier to govern and avoids duplicate agent context. |
| [`ningzimu/codex-ppt-skill`](https://github.com/ningzimu/codex-ppt-skill) | Strong image-first slide styling and speaker notes | Do not install. Flattened slide images weaken editability and technical-diagram maintenance. |
| [`siril9/presentation-skill`](https://github.com/siril9/presentation-skill) | Editable PPTX sources and render-based QA | Do not install. It overlaps the installed Codex Presentations skill and adds a second deck-generation stack. |
| [OpenAI `google-slides` plugin example](https://github.com/openai/plugins/tree/main/plugins/google-slides) | Native Slides import, inspection, template migration, and visual iteration | Use the installed Google Drive connector for these actions. A second local plugin is unnecessary for the current workflow. |
| Figma connector | Collaborative free-form canvas and design-system tooling | Defer. It is useful if a shared design system or manual whiteboarding becomes a requirement, but it should not replace version-controlled architecture sources. |

## Artifact register

No product architecture diagram or deck has been accepted yet. The following
implementation-aligned sources are registered as drafts.

| ID | Title | Type | Audience | State | Status | As of | Source | Rendered or delivery | Decisions | Verification | Owner |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TS-ARC-001 | Tendy Spider target runtime | Container/trust | Architecture, engineering | Mixed | Draft | 2026-07-19 | `docs/diagrams/container-target-runtime.mmd` | Not rendered | D-001–D-007, D-010, D-012, D-013 | Current M0 and target elements reconciled; source-structure checks passed; visual QA pending | `solution_architect` |
| TS-ARC-002 | Milestone 0 package dependencies and ownership | Component/dependency | Engineering | Mixed | Draft | 2026-07-19 | `docs/diagrams/component-m0-package-dependencies.mmd` | Not rendered | D-003, D-005, D-006, D-009, D-012, D-013 | Implemented ownership/dependencies and deferred research consumption checked; visual QA pending | `solution_architect` |
| TS-ARC-003 | Milestone 0 local startup and health | Integration sequence | Engineering, operations | Current source/partially verified | Draft | 2026-07-19 | `docs/diagrams/sequence-m0-local-startup-health.mmd` | Not rendered | D-002, D-012, D-013 | API/web smoke passed; Docker path unverified; sequence structure checked; visual QA pending | `solution_architect` |
