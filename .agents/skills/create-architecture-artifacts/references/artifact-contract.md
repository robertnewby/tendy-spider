# Architecture Artifact Contract

## Repository layout

Use these locations unless an accepted repository decision establishes another
structure:

```text
docs/
  ARCHITECTURE.md                 canonical narrative
  ARCHITECTURE_ARTIFACTS.md       toolchain and artifact register
  diagrams/
    <view>-<slug>.mmd             Mermaid source
    <view>-<slug>.dot             Graphviz source when justified
    <view>-<slug>.drawio          manually editable source when required
    rendered/
      <view>-<slug>.svg           preferred vector export
      <view>-<slug>.png           raster review or compatibility export
  decks/
    <deck-slug>/
      deck.mjs                    editable deck-generation source
      notes.md                    narrative, evidence, and speaker-note source
outputs/
  architecture/
    <deck-slug>.pptx              verified import or interchange artifact
```

Do not commit temporary render directories, downloaded provider data, secrets,
or external template assets without recorded rights.

## Artifact register fields

Maintain one row per durable artifact in `docs/ARCHITECTURE_ARTIFACTS.md`.

| Field | Meaning |
|---|---|
| ID | Stable short identifier |
| Title | Human-readable artifact title |
| Type | Context, container, workflow, data flow, sequence, deployment, trust, or deck |
| Audience | Executive, product, architecture, engineering, operations, or external |
| State | Current, target, transition, or mixed |
| Status | Draft, reviewed, accepted, superseded |
| As of | Date or repository revision represented |
| Source | Editable repository source path |
| Rendered or delivery | Reviewed SVG, PNG, PPTX, or Google Slides link |
| Decisions | Related `DECISIONS.md` IDs |
| Verification | Syntax, semantic, visual, and import checks performed |
| Owner | Profile or person responsible for updates |

Use `draft` until semantic and visual checks both pass. Use `accepted` only when
the relevant decision owner has accepted the architecture, not merely because a
diagram rendered successfully.

## Versioning

- Keep stable artifact IDs when content evolves without changing purpose.
- Create a new artifact ID when the audience, scope, or review question changes
  materially.
- Mark old artifacts superseded and link to the replacement instead of silently
  deleting historical decisions.
- Put the represented repository revision or an as-of date on external decks.
- Regenerate derived assets from source after every semantic change.

## Provenance

Architecture claims derived from external facts must point to an entry in
`docs/SOURCES.md` or an authoritative linked source. Product behavior claims
must point to repository contracts, tests, or accepted decisions. Record
assumptions explicitly when evidence is not yet available.
