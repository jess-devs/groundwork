# Artifact templates

Use these structures exactly. Translate the headings into the user's working
language; keep the file names fixed.

Translate into the working language everything a person reads as prose:
headings, story status, verification results, descriptions, evidence. A status
shown here as `pending` is written `pendiente` in a Spanish project.

Two things are fixed identifiers and are never translated, because an agent or a
person opening the repository months from now has to find them without being told
where they are: file and directory names, and the mode names
`new-project` / `adopt` / `new-feature`. Everything else read as a sentence is
translated, including the verification results `pass` / `fail` / `blocked`,
written `pasa` / `falla` / `bloqueado`.

Every artifact starts with the same header block, no exceptions, including
`decisiones.md`:

```markdown
> Status: draft | approved
> Last updated: YYYY-MM-DD
> Mode: new-project | adopt | new-feature (these three stay in English)
```

Every label and value in this block is prose and is translated: `Estado:
borrador | aprobado`, `Última actualización:`, `Modo:`. The one exception is the
three `Mode:` values themselves, which stay in English because Step 0 routes on
them.

Mark anything inferred rather than confirmed with `[inferred]`, written
`[inferido]` in the working language, at the end of the line. Readers must be
able to tell what was decided from what was guessed.

---

## 00-contexto.md

```markdown
# Context

## Problem

One paragraph. What is broken or missing today, stated without naming a
solution.

## Users

Who uses this, and what each type needs from it. One line each.

## Constraints

Technical, temporal, budgetary, regulatory. Only constraints the user stated.

## Team

Solo or group. If a group, who does what.

## Methodology

Chosen: <name>
Reason: <two or three sentences tying the choice to the constraints above>
Consequences: <what this commits the project to>

## Glossary

Domain terms and their agreed meaning. Prevents the same thing being called
three different names later.
```

The methodology block is load-bearing. Without the reason recorded, every later
phase reopens the argument.

---

## 01-alcance.md

```markdown
# Scope

## In scope

Bulleted. Each item concrete enough to be recognisably done or not done.

## Out of scope

Bulleted. What was considered and deliberately excluded, with a short why.
This section prevents more rework than the previous one.

## Assumptions

Things taken as true without confirmation. Each one is a risk.

## Open questions

Unresolved items, with who needs to answer them.
```

---

## 02-requisitos.md

Requirements are numbered so that stories and tests can reference them. Prefix
`RF` for functional, `RNF` for non-functional.

```markdown
# Requirements

## Functional

### RF-01: <short title>

The system must <capability>.
Source: <where this came from, e.g. user statement, constraint, regulation>

## Non-functional

### RNF-01: <short title>

The system must <quality>, measured as <concrete threshold>.
Source: <the stated constraint this derives from>
```

A non-functional requirement without a measurable threshold and a traceable
source is filler. Ask for the number instead of choosing one.

---

## features/&lt;slug&gt;/requisitos.md

Same structure as `02-requisitos.md`, but scoped to the feature, and each entry
references the system-level requirement it refines:

```markdown
### RF-04.1: <short title>

Refines: RF-04
The system must <capability>.
```

---

## features/&lt;slug&gt;/historias.md

Each requirement becomes one or more stories. Keep the requirement visible so
traceability survives.

```markdown
# User stories

## HU-01: <short title>

Covers: RF-01

**Story.** As a <role>, I want <capability> so that <benefit>.

**Acceptance criteria.**

1. CA-01.1: <observable, checkable statement>
2. CA-01.2: <observable, checkable statement>

**Status.** pending | in progress | verified
(in the working language: `pendiente` | `en progreso` | `verificada`)
```

Criteria are numbered `CA-<story-number>.<n>` (e.g. `CA-01.1`) so that
`04-calidad.md` and the handoff to another skill can reference each one by ID
instead of by quoting its text.

Criteria are written so that a person can look at the running system and say yes
or no without interpretation. Compare:

- Bad: the system is fast.
- Good: searching available time slots returns results in under one second.
- Bad: the interface is pleasant.
- Good: the layout adapts without horizontal scrolling on screens from 320px up.

Non-functional requirements become stories too. They are the ones most often
skipped, and the ones that most often force rework.

---

## features/&lt;slug&gt;/plan.md

```markdown
# Plan

## Order

1. HU-01: <why first>
2. HU-03: depends on HU-01

## Dependencies

Which stories block which, and why.

## Assignment

Solo: leave this section out entirely.
Group: who takes what, and which stories can proceed in parallel.

## Risks

What could force this plan to change.
```

---

## 03-arquitectura.md

```markdown
# Architecture

## Overview

Three to five sentences. What the pieces are and how they relate.

## Boundaries

What each module owns, and what it is not allowed to know about.

## Conventions

Naming, layering, error handling, where business logic lives.

## Decisions

Index of decisions, newest last, each linking to its entry in a
features/*/decisiones.md file. Every decision recorded anywhere in the project
appears here; this index is how someone finds them without knowing which
feature they were made in, so it is updated in the same turn the decision is
written.
```

---

## features/&lt;slug&gt;/decisiones.md

Header block first, then one entry per decision. This is what stops a later
session from reopening a settled question.

```markdown
## AD-01: <the decision, stated as a sentence>

Date: YYYY-MM-DD
Context: what forced a choice here.
Alternatives considered: A, B, C, and why each was rejected.
Decision: what was chosen.
Consequences: what this now commits us to, including the costs.
Status: active | superseded by AD-NN
```

Never delete a superseded decision. Mark it. The record of what was rejected is
worth as much as the record of what was chosen.

---

## 04-calidad.md

```markdown
# Quality

## Quality attributes

Which attributes matter for this system and why, each tied to an RNF.

## Verification log

| Story | Criterion                                 | Result  | Date       | Evidence               |
| ----- | ----------------------------------------- | ------- | ---------- | ---------------------- |
| HU-01 | CA-01.1: Search returns in under 1s       | pass    | 2026-03-04 | measured locally, 0.4s |
| HU-04 | CA-04.1: Stored password is not readable  | blocked | 2026-03-04 | needs DB access        |
```

Result is `pass`, `fail` or `blocked`, written in the working language (Spanish:
`pasa`, `falla`, `bloqueado`).
Evidence describes what was observed: what was clicked, what was measured, what
was seen. "Guaranteed by the design" is not evidence; it is the reason to write
`blocked`.

A criterion recorded as failed or blocked is a normal outcome and stays in the
log. A log with only passes is a log nobody used.

---

## AGENTS.md

Not part of `docs/`, but part of the contract: it is written in the same turn as
the first artifacts that create `docs/`, not offered afterwards. It sits at the
repository root and is the entry point most tools read on their own, which makes
it the only place the three rules reach an agent that never loaded this skill.
It names the contract and points at everything else rather than restating it,
except those three rules, which it carries in full for exactly that reason.

This is the shape of a file you are creating. When one is already there, take
the two sections below and add them to it, keeping everything it already says
in the order it says it, under whatever title it already has. Most existing
`AGENTS.md` files hold the build commands and the house conventions, which are
the parts a team notices missing. If the repository uses `CLAUDE.md` or another
file the same way, add the sections there rather than creating a second entry
point, and say which file you used.

```markdown
# <project name>

## Documentation

The decisions that govern this repository live in `docs/`. Read them before
changing code.

| File                      | What it holds                                         |
| ------------------------- | ----------------------------------------------------- |
| `docs/00-contexto.md`     | problem, users, methodology                           |
| `docs/01-alcance.md`      | in scope, out of scope, assumptions                   |
| `docs/02-requisitos.md`   | system requirements                                   |
| `docs/03-arquitectura.md` | structural decisions and the decision index           |
| `docs/04-calidad.md`      | quality attributes and the verification log           |
| `docs/features/<slug>/`   | requirements, stories, plan and decisions per feature |

## Rules

- No code without a story in `features/<slug>/historias.md`.
- Any decision someone could later want to reverse goes in `decisiones.md`.
- A criterion is verified by observation. What could not be observed is recorded
  as blocked, not as passed.

## Artifacts from other tools

| Artifact | What it governs                       |
| -------- | ------------------------------------- |
| `<path>` | `<what it decides, and who wrote it>` |
```

Keep the last table only if another skill or tool wrote artifacts of its own.
Every row must point at a file that exists; an entry point with a broken pointer
is worse than no entry point.
