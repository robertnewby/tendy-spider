# Architecture Deck Standards

## Delivery model

Default to an editable native Google Slides deck for shared delivery. Build
net-new decks as verified local PPTX files through the installed Presentations
skill, then import them through the Google Drive connector using
`native_google_slides`. Keep the deck source and the generated PPTX so the deck
is reproducible.

Edit an existing native Google Slides deck in place through the connector.
Require a fresh presentation read and revision before a material batch update.
Update existing repository source first. If the deck has no source, backport the
edited structure, text, notes, and durable diagrams into a reproducible source
workspace before marking the deck synchronized.

## Narrative

Start with the decision the audience must understand, not with a catalog of
components. A typical technical architecture review uses:

1. title, scope, state, and as-of date;
2. decision or problem statement;
3. system context;
4. primary user workflow;
5. logical stack or container view;
6. data provenance and transformation flow;
7. integration sequence and failure behavior;
8. security, trust, operations, and observability;
9. tradeoffs, open decisions, and phased delivery;
10. appendix with contracts, sources, or detailed views.

Change the sequence when the audience or decision requires it. Do not create
empty sections merely to match the outline.

## Slide design

- One conclusion or question per slide.
- Use a message title that states the takeaway.
- Prefer a diagram, evidence-backed chart, or small comparison over prose.
- Keep labels legible at normal presentation zoom; split dense diagrams.
- Use consistent names, colors, and boundary shapes across the deck.
- Include a legend when styling carries architecture meaning.
- Put as-of dates, source identifiers, and decision references near the claim
  they support.
- Put nuance, evidence details, and talk track in speaker notes when useful.
- Mark proposed, future, paid, permissioned, and unverified elements visibly.
- Add meaningful alternative text to diagrams and informative images when the
  delivery surface supports it; verify slide element reading order.
- Preserve text editability. Use rasterized full-slide imagery only for
  illustrative material, never for the core architecture narrative.

If no project template exists, use the Presentations skill's default design
system and establish a restrained technical visual language. Do not invent a
permanent brand palette before the owner chooses one.

## Verification

Follow every verification requirement in the Presentations skill:

- render every slide;
- inspect slides individually at full size;
- check all text, diagrams, and footnotes for overlap and clipping;
- check visual rhythm and density across a contact sheet;
- fix the source and regenerate rather than patching the binary deck;
- import only the fully verified PPTX to Google Slides.

After import, read the Google Slides presentation back and verify the expected
title, revision, page count, and slide order. Then render, screenshot, or export
the native Slides result and visually inspect it for font substitution, text
reflow, clipping, diagram movement, contrast, and reading order. Metadata alone
does not prove visual fidelity. If no faithful visual review path is available,
record native Slides fidelity as unverified. Record the deck ID or link in the
artifact register.

## Update discipline

- Never overwrite a shared deck without an explicit update request.
- Preserve the previous accepted artifact or use deck revision history.
- Update diagrams and deck content from repository source first, then refresh
  the deck. Backport any connector-side polish before closing the task.
- Record which repository revision and architecture decisions the deck reflects.
- Label exported PDF or PPTX copies as snapshots; the native Slides deck is the
  collaboration surface, not the architecture source of truth.
