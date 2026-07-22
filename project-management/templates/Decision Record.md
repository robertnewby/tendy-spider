---
type: decision
id: "{{VALUE:ID}}"
project: tendy-spider
title: "{{VALUE:Title}}"
status: open
priority: "{{VALUE:Priority}}"
owner_agent: "{{VALUE:Owner agent}}"
decision_authority: owner
next_action: "{{VALUE:Next action}}"
source_file: DECISIONS.md
source_ref: "{{VALUE:DECISIONS heading}}"
created: "{{DATE:YYYY-MM-DD}}"
updated: "{{DATE:YYYY-MM-DD}}"
tags:
  - project-management
  - decision
  - tendy-spider
---

# {{VALUE:ID}} — {{VALUE:Title}}

> Add or update the authoritative decision in [[DECISIONS]] before closing this
> operational record.

## Question

State the decision to make.

## Evidence required

- [ ] #task {{VALUE:Next action}}

## Outcome

Link the accepted `DECISIONS.md` entry after the owner decides.
