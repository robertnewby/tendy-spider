---
name: create-architecture-artifacts
description: Create, review, and maintain rigorous software-architecture artifacts for Tendy Spider, including C4-style context and container views, technology-stack diagrams, user workflows, data-flow diagrams, integration and sequence diagrams, deployment and trust-boundary views, architecture decision visuals, and architecture presentations delivered as editable PowerPoint or native Google Slides. Use when an architecture idea must become a reviewable repository artifact, when diagrams or decks need to stay synchronized with code and decisions, or when an existing architecture visual needs semantic or visual QA.
---

# Create Architecture Artifacts

## Overview

Turn architecture reasoning into source-controlled models, validated visual
exports, and decision-oriented decks without making the main implementation
agent carry the artifact-production context.

## Governing rules

- Read the repository guidance in its required order before changing an
  architecture artifact. Treat `docs/ARCHITECTURE.md` and accepted entries in
  `DECISIONS.md` as architectural truth.
- Reconcile contradictions before drawing. Do not make an architecture change
  merely to simplify a diagram. Record a material conflict or proposed
  resolution in `DECISIONS.md`.
- Keep editable text or code as the source of truth. Treat SVG, PNG, PPTX, and
  Google Slides as derived or delivery artifacts.
- Preserve the clean-room, provider-neutral, read-only MVP boundaries. Never
  invent a provider, protocol, data right, deployment choice, or implementation
  fact that the repository has not established.
- Mark proposed, current, future, external, paid, permissioned, and unverified
  elements explicitly. Put an as-of date or repository revision on every
  externally shared artifact.
- Do not silently upload or overwrite a deck. Obtain or infer authorization from
  the user's request, preserve the local source, and report the resulting link.
- Announce use of this skill to the user and explain any pause caused by its
  quality gates.

## Workflow

### 1. Define the artifact brief

Capture the audience, decision or question, scope, current-versus-target state,
required views, delivery format, and any template or brand constraints. Make a
reasonable documented assumption when the missing choice is reversible. Ask
only when the choice changes the architecture or external deliverable
materially.

### 2. Build an evidence-backed architecture inventory

Inspect the implementation, contracts, decisions, source ledger, and relevant
tests. List actors, systems, containers, components, stores, external
dependencies, trust boundaries, interfaces, protocols, ownership, deployment
assumptions, and important failure paths.

For market-data flows, include observation time, knowledge or publication time,
retrieval time, source identity, freshness, latency, adjustment mode, and
transformation lineage wherever the view discusses those concerns.

### 3. Select the minimum useful views

Read [diagram-standards.md](references/diagram-standards.md) before creating or
reviewing diagrams. Do not produce every possible view. Choose the smallest set
that answers the review question and use stable IDs so the same element keeps
the same name across zoom levels.

### 4. Model semantics before styling

Write a short model inventory before authoring the visual. Every node needs a
clear type and responsibility. Every arrow needs a direction and a verb; add
payload, protocol, cadence, and security classification when relevant. Show
error, stale, partial, and retry paths when they affect the design.

### 5. Author source-first diagrams

Use Mermaid flowcharts, sequences, state diagrams, and ER diagrams as the
default repository format. Apply C4 semantics with ordinary Mermaid flowcharts
instead of depending on experimental C4 syntax. Use Graphviz DOT only for dense
topologies that Mermaid cannot lay out clearly. Use native slide shapes for
simple slide-only diagrams.

Use draw.io only when humans need ongoing drag-and-drop editing or a specialized
stencil library. Preserve both the editable `.drawio` file and a reviewed SVG or
PNG. Use generated raster imagery only for illustrative concepts, never as the
canonical technical model.

Keep sources under `docs/diagrams/` and follow
[artifact-contract.md](references/artifact-contract.md).

### 6. Validate semantics and rendering

Validate syntax with a deterministic local renderer when one is provisioned.
Render every final diagram and inspect it at full size. Fix overlap, clipping,
crossed labels, ambiguous arrow direction, unreadable text, inconsistent
element names, and weak contrast. Split dense diagrams rather than shrinking
them.

If the required renderer is unavailable, keep the artifact in draft status,
report the missing prerequisite, and do not claim visual QA passed. Never send
architecture source to an unapproved remote rendering service.

### 7. Build an architecture deck

Read [deck-standards.md](references/deck-standards.md). For any deck creation or
editing task, load and follow the installed `Presentations` skill completely,
including its content rules and render-and-inspect loop.

For a net-new Google Slides deck:

1. Build and fully verify the editable local PPTX and its source.
2. Import the verified PPTX through the Google Drive connector with
   `upload_mode: native_google_slides`.
3. Read the imported presentation back to verify its identity, title, revision,
   and slide structure.
4. Record the local source, PPTX, Google Slides ID or link, and verification
   status in the artifact register.

For an existing native Google Slides deck, inspect and edit it directly through
the Google Drive connector. When repository deck source exists, update that
source first and apply the corresponding change to Slides. When source does not
exist, reconstruct or backport the changed content into `deck.mjs` and
`notes.md` before marking the deck synchronized or accepted. Preserve revision
control and avoid a PPTX round-trip unless the user explicitly requests one.

After importing or materially editing a native Slides deck, render, screenshot,
or export the Google Slides result and inspect the delivery artifact for font
substitution, text reflow, clipping, diagram movement, and contrast changes. If
the connected surface cannot provide a faithful visual review path, mark native
Slides fidelity unverified instead of treating metadata checks as visual QA.

### 8. Hand off the artifact set

Update `docs/ARCHITECTURE_ARTIFACTS.md`, relevant decision records, and any
architecture narrative affected by the visuals. Report:

- the review question and audience;
- source and rendered artifact paths;
- validation and visual-QA evidence;
- current, proposed, deferred, paid, permissioned, and unverified elements;
- decisions made or still required;
- the Google Slides link when a deck was published.

## Quality gates

An architecture artifact is complete only when:

- its semantics agree with repository evidence and decisions;
- names and boundaries remain consistent across all zoom levels;
- arrows state meaningful interactions rather than generic connectivity;
- external systems, trust boundaries, stores, and failure paths are clear;
- market-data provenance and time semantics are represented when relevant;
- editable source and rendered output are both preserved;
- the rendered result was inspected at final size;
- diagrams and slide images have meaningful alternative text when the delivery
  surface supports it, and slide reading order is verified;
- the artifact register identifies status, as-of date, owner, and decision links;
- a deck has a coherent narrative, readable typography, citations, speaker notes
  when useful, and verified Google Slides delivery when requested.
