# Diagram Standards

## Choose the view by question

| View | Primary question | Expected contents |
|---|---|---|
| System context | Who uses the product and what external systems constrain it? | People, Tendy Spider, external systems, high-level relationships |
| Container or stack | What runs, stores data, and communicates at runtime? | Web app, API and analytics service, workers, stores, queues, provider adapters |
| Component | How is one container divided into responsibilities? | Modules, interfaces, ownership, internal dependencies |
| User workflow | What does a person do and where are decisions or confirmations? | User steps, UI states, system responses, approvals, error exits |
| Data flow | Where does data originate, change form, persist, and become stale? | Sources, raw observations, normalized and derived stores, lineage, consumers |
| Integration sequence | What happens over time across a boundary? | Participants, calls or events, payloads, retries, failures, timeouts |
| Deployment | Where do runtime units execute and what infrastructure connects them? | Environments, compute, network boundaries, stores, observability |
| Trust boundary | Where do identities, privileges, secrets, and data classifications change? | Actors, zones, authentication, authorization, sensitive flows |

Use a component view only when it resolves a real implementation or ownership
question. Do not create code-level diagrams by hand when they can be generated
from source.

## C4-compatible semantics

- A person is a role, not an individual.
- A software system provides value independently and has a clear boundary.
- A container is a separately runnable or deployable application or data store,
  not a Docker container by definition.
- A component is a cohesive responsibility inside one container.
- Keep element IDs and display names stable across context, container, and
  component views.
- Show technologies on container and lower-level views, not on the context view.
- Put the diagram type, scope, and current or target state in the title.
- Include a legend whenever status, trust, freshness, or ownership is encoded by
  color or line style.

Use ordinary Mermaid flowcharts with these semantics. Mermaid's C4 syntax has
more rendering and styling constraints and should not be the default.

## Node and relationship labels

Node labels should contain:

1. a stable name;
2. a type or technology where the view permits it;
3. one concise responsibility.

Relationship labels should use an active verb. Add the important payload,
protocol, cadence, or trust transition when known.

Good: `Retrieves point-in-time filings [HTTPS/JSON, on demand]`

Weak: `Uses`

Do not imply bidirectional behavior with a single unlabeled line. Use two
relationships when the requests and events have different meaning.

## Tendy Spider invariants

- Keep provider SDKs outside core domain boundaries.
- Distinguish raw immutable observations, normalized records, and derived
  analytics.
- Show deterministic calculations separately from LLM orchestration.
- Show user confirmation and audit logging around mutations.
- Mark delayed or end-of-day data explicitly.
- When the view covers financial data, represent observation time, knowledge or
  publication time, retrieval time, freshness, source identity, adjustment
  mode, and transformation lineage at the appropriate level.
- Model partial, stale, contradictory, missing, rate-limited, and permissioned
  states instead of implying every request succeeds.
- Do not depict live order execution in the MVP.

## Format selection

Use Mermaid by default for flow, sequence, state, ER, and C4-style views because
plain text is reviewable and versionable. Prefer left-to-right for workflows
and data pipelines and top-to-bottom for layered stacks.

Use Graphviz DOT for dense dependency or integration topology only when a local
renderer is available and its layout is materially clearer.

Use draw.io only when manual editing, specialized stencils, or pixel-level
connector routing is a deliverable requirement. Treat the editable file as
source and commit a reviewed SVG or PNG beside it.

Use native slide shapes for simple diagrams that exist only to explain one deck
message. If that diagram represents durable architecture, create a repository
source as well.

## Density and visual checks

- Aim for no more than roughly 20 to 25 nodes in one view.
- Avoid more than three nested boundaries in a single diagram.
- Split current and target state when overlays create ambiguity.
- Use no more than five semantic colors plus neutrals.
- Do not encode meaning by color alone.
- Keep labels horizontal and short; use notes or a companion table for detail.
- Keep connectors out of nodes and labels.
- Render and inspect at the size used in the document or slide.
- Check light and dark backgrounds when the artifact will appear in both.

## Review checklist

- Does the title state scope and state?
- Can a reviewer name every boundary and external dependency?
- Are direction, payload, protocol, and failure semantics clear?
- Do all views use the same names for the same things?
- Are proposed and implemented elements distinguishable?
- Are hidden provider, licensing, credential, or deployment assumptions absent?
- Is the source editable and the rendered export legible?
