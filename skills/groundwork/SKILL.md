---
name: groundwork
description: "Turns an idea or a feature request into approved, versioned documentation before any code is written, then keeps the implementation tied to that documentation. Use this whenever someone wants to start a new project, add a feature to an existing codebase, plan before coding, write requirements or user stories, pick a methodology, or record an architecture decision. Use it especially when the request is vague enough that writing code immediately would mean guessing, and when someone asks to skip the documentation or wants the code written straight away. Use it whenever the repository already contains a docs/ folder in the format below, including for work that is not documentation at all: fixing a bug, changing configuration, verifying or closing an acceptance criterion, or handing part of the work to another skill and taking it back. Those are the moments the recorded decisions exist to govern, and the moments they are most often bypassed."
license: Apache-2.0
metadata:
  version: 0.7.0
---

# Groundwork

Agents invent the details a request leaves out. This skill writes them down in
`docs/` before implementation, then holds implementation to them. Why each rule
is there is in `references/rationale.md`.

**This file ends with the section "Reference files". If the text you have ends
before it, it was cut when the context was compacted: read this file from disk
before the next change.**

## Working language

Write every artifact **and every message** in the language the user writes in.
After a summary, re-read which language that is rather than defaulting to
English.

Never translated: file and
directory names (`00-contexto.md`, `features/`, `historias.md`; the feature slug
itself is in the working language), and the mode names `new-project` / `adopt`
/ `new-feature`. Everything else is translated, including story status
(`pendiente`, `en progreso`, `verificada`) and results (`pasa` / `falla` /
`bloqueado`).

## Execution contract

These rules apply for the rest of the session. What survives a compaction is
`docs/`, not this text, so read from disk at the two moments that matter:
before implementing a story, open the story; before verifying a criterion, open
the criterion and `AGENTS.md`. If `AGENTS.md` does not carry the three rules,
fix that before continuing.

1. **No code without a story.** Before implementing, read the story and its
   acceptance criteria in `features/<slug>/historias.md`. If no story covers the
   change, stop and ask whether to write one.

2. **Record any decision someone could later want to reverse.** Consult
   `03-arquitectura.md` first; if the change contradicts it, stop. Otherwise
   the test is whether a developer arriving in six months could wonder why it
   is like that and be unable to tell. That includes migrating to a replacement
   API, changing a shared type, adding a config flag and choosing where a new
   concern lives, not only new modules and dependencies. It costs six lines in
   `decisiones.md`.

3. **Verify by observation, never by argument.** Each criterion gets one of
   three results:
   - `pass`: observed working, with what was observed written down.
   - `fail`: observed not working.
   - `blocked`: could not be observed, with the missing resource named. The
     story stays open.

   There is no fourth result. Evidence from a stand-in (a mock, a self-check,
   an offscreen render, the client instead of the server) leaves the criterion
   `blocked`; if part of it was observed, split it. What the user says they saw
   is recorded as theirs ("observed by the user: …"), not as your `pass`.
   Changing code a `pass` covers reopens it as `blocked` until observed again.

   Never `pass` because the design implies it, a library guarantees it, or the
   code looks right. Sound reasoning with nothing observed is `blocked`. This
   is most tempting in security criteria, so when the argument feels
   conclusive, mark it blocked and say what would settle it.

   A criterion nobody could ever observe ("the interface is intuitive") was
   written badly and is rewritten. One you cannot observe from where you are is
   not rewritten: it is `blocked`, with the resource named. Shrinking criteria
   to fit the tools of this session makes them describe the agent instead of
   the system.

   When you finish verifying, gather the blocked criteria into one request:
   which ones, the single resource that unblocks them, and what you would do
   with it. Do not repeat that request in later closings until the resource
   appears or the user asks.

4. **Leave the environment as you found it.** Test data created to verify a
   criterion is deleted once observed, including rows in real databases and
   accounts created for a login test. Say what you are about to delete, then
   say that you deleted it.

   A check that reaches outside the sandbox (sends a message, calls a webhook,
   writes a user's real files, changes system state) is announced and asked
   for first. Afterwards, confirm the teardown worked, not only that it ran.

   Only what you created in this session and wrote down as you created it: the
   identifier, the row, the account name. A pattern (`test%`, today's rows)
   also matches what was there before you. When you cannot tell your data from
   the data already there, do not delete: hand over the identifying criterion
   and say what you could not separate.

   Without permission to delete, hand the user the exact command at the end of
   that story, not accumulated across several. It names the rows it removes,
   not a pattern, and you check it before giving it. Say which data you
   deliberately kept, and why.

Verifying acceptance criteria is in scope. Designing a test suite, choosing a
testing framework or writing automated tests is not.

### When the user is iterating

A run of small changes to one surface (layout, copy, styling, a prompt) is one
piece of work, not a story per tweak. On the first tweak, name the story it
belongs to, or offer one umbrella story, and set the criteria the tweaks can
change to `blocked` until observed again. Then iterate without ceremony.

When the run ends (the user moves on, asks for a commit or a PR, or about ten
tweaks have piled up), do one sync pass before anything else: record the
decisions taken, rewrite the criteria that changed, observe them, update scope
and plan, and end with the validation line.

For visual work, offer a throwaway prototype before writing stories: approving
a screen says more than approving a document that describes it.

### When another skill writes the code

While another skill drives, this contract stops being applied.

**Going in**, when delegation is first mentioned: write the criteria into the
handoff itself, each identifier with its text and its threshold, plus the
constraints recorded in `03-arquitectura.md`. A path is not a handoff.

**Coming back**, in the same session:

1. Verify each criterion the work covers, by observation, and record the
   results in `04-calidad.md` and the story status in `historias.md`.
2. Record in `decisiones.md` the decisions taken while building, including the
   ones the other skill made on its own.
3. If the work exposed a gap no criterion covers, say so and offer to write the
   story.
4. Point to any artifacts it wrote from `AGENTS.md`, with what they govern. Do
   not rewrite them into this format.

## Keep the earlier artifacts true

A document describing something that did not happen is read with the same
trust as an accurate one. Whenever reality diverges from an earlier artifact,
fix that artifact in the same turn:

- Scope a later phase discovers → add it to `01-alcance.md` and resolve or
  restate the affected open questions.
- Implementation departs from `plan.md` → correct `plan.md`. A reason in
  `decisiones.md` does not fix a plan nobody followed.
- A new decision in a feature's `decisiones.md` → add it to the index in
  `03-arquitectura.md`.
- A decision superseded → mark the old one, never delete it.
- You say you will do something later → write it in `plan.md` or `01-alcance.md`
  now, and name the file.
- The user drops something from scope → move it to out of scope, with the date.

Check this before every commit or pull request that touches governed code,
after a merge, and when the user closes the session: compare what changed since
the last check with `historias.md`, `plan.md` and `04-calidad.md`, and run the
checker. The user should never have to ask for the documents to catch up.

Say what you updated when you present. Two artifacts that contradict each
other are a defect, and the older one is usually the wrong one.

## Secrets

Credentials, tokens and connection strings never appear in your output, in an
artifact or in a commit, even values the user pasted and keys documented as
public.

Refer to a secret by its variable name and never echo its value: not in a diff,
a summary, a confirmation that it was set, or a command you run. Pass the
variable, or run the thing that already reads it.

When editing a file that holds a secret, match the smallest unique fragment
that does not contain the value (the port, the host, the flag), never the
whole line.

Keep an example file with empty values, marking which variables are secret and
which are safe to expose to a client. If a secret has already been printed in
this session, say so plainly and recommend rotating it.

## Step 0: mode and environment

One look at the workspace and, at most, one question.

**Environment.** With a filesystem, artifacts go to `docs/`. Without one,
produce the same Markdown in the conversation, one document per message,
naming the file each block belongs to.

**Scale.** The process is not needed when the change is smaller than its
documentation would be: a script, a one-file utility, a throwaway spike, a
typo, a rename, one well-specified function. Say so in one line, offer the
short path, and do the work. Judge the size of the change, not the phrasing.
When it is
borderline, ask once: "this looks small enough to just build; want me to, or
should we scope it first?"

**Mode.** Inspect the workspace:

| What you find                             | Mode          | Where to start          |
| ----------------------------------------- | ------------- | ----------------------- |
| Empty or near-empty workspace             | `new-project` | Phase 1                 |
| Existing code, no `docs/`                 | `adopt`       | Phase 0.5, then Phase 1 |
| Existing code with `docs/` in this format | `new-feature` | Phase 0.5, then Phase 3 |

Never guess the mode from the wording of the request alone.

## Phase 0.5: reconnaissance (any mode with existing code)

Before asking the user anything about the feature:

1. Read `docs/` if it exists, starting with `00-contexto.md`,
   `03-arquitectura.md` and any `features/*/decisiones.md`. These are closed
   decisions: do not reopen them on preference. If the code contradicts what is
   written, report the divergence and ask which one is wrong. Never edit a
   recorded decision without saying what diverged.
2. Read enough of the code to state, in three sentences, what the system does,
   how it is layered, and what conventions it follows.
3. Report that summary and ask the user to correct it.

In `adopt` mode, offer to reconstruct `00-contexto.md` through `04-calidad.md`
from the code, marking every reconstructed statement as inferred. Do not start
feature work until the user has reviewed it.

## The gate

Each phase ends with a written artifact and an explicit approval. Present the
artifact, state what the next phase will do, and stop. Do not chain phases in
one response. Approval means the user says so; silence, an emoji, or a question
about something else is not approval.

When three gates in a row come back approved with nothing corrected and nothing
asked, say so and offer to merge the remaining stops: Phase 1 with 2, Phase 3
with 4, each still producing both artifacts and ending in one approval. Never
merge them without saying so.

An approval changes the document's status on disk in the same turn. If the user
approves by merging pull requests, ask once whether a merge approves the
documents it carries, record the answer in `00-contexto.md`, and apply it. When
decisions are delegated ("decide yourself", an unattended run), stories and
criteria are still written before the code, and the decisions awaiting the user
are listed in one place for one approval on their return.

If the user asks to skip a phase, comply, but in the same turn write the
skipped artifact as a stub recording that it was skipped and which assumptions
were adopted. If the whole process was skipped and there is no `docs/`,
`docs/00-contexto.md` alone is enough: what was asked, what was skipped, and
every assumption, which are almost always the stack, where data is stored, and
the shape of the main entity.

## Phases

Read `references/interview.md` before Phase 1 or 3, and
`references/templates.md` before writing any artifact.

**Phase 1: Context and scope.** Interview the user about the problem, the
users, the constraints and the boundaries. Choose a methodology with
`references/methodology.md` and record it _with its justification_. Produces
`00-contexto.md` and `01-alcance.md`.

**Phase 2: Requirements.** Functional and non-functional requirements from the
scope. Every non-functional requirement traces to a constraint the user
stated; if it does not, ask instead of inventing one. Produces
`02-requisitos.md`.

**Phase 3: Feature definition.** Slice the work into a feature, turn its
requirements into user stories with verifiable acceptance criteria, and order
them. Produces `features/<slug>/requisitos.md`, `historias.md` and `plan.md`.

**Phase 4: Architecture.** Only after requirements are approved. Decide
structure, boundaries and dependencies, each decision with its alternatives and
consequences. Produces or updates `03-arquitectura.md` and
`features/<slug>/decisiones.md`.

**Phase 5: Implementation.** Governed by the execution contract.

**Phase 6: Verification.** Check each acceptance criterion against what was
built and record the result. Produces or updates `04-calidad.md`.

### How to slice a feature

A feature is a set of stories that deliver value to one kind of user and can be
finished and verified together. Cut along user roles and coherent flows, not
along technical layers. When in doubt, split: more than about six stories, or
stories serving two roles, means split. Name the slice for what the user gets
(`solicitud-de-reserva`), not for the release (`v1`).

Propose the slicing before writing the artifacts, with the reason for each cut,
and stop for approval. Only the first slice gets full artifacts; the rest are
named and left for later.

## The validation report

Before presenting any artifact, check it against `references/validation.md`,
fix what fails, then present. Run the structural checker first. It is in
`scripts/` next to this file; use the path this file was read from:

```sh
python <skill directory>/scripts/check_docs.py docs/
```

It reports identifiers that nothing defines or that are defined twice,
requirements no story covers, stories with no criterion, decisions missing from
the index, and pointers to files that are not there. Fix what it reports before
presenting. A clean run is not a validated artifact: whether a criterion is
observable or a requirement invented is still read by hand. When the user asks
what is left, answer from `check_docs.py --status docs/`, not from memory.

End every artifact presentation with this line, in the working language:

> Validation: N checks passed, M fixed (<what>), K open (<what>).
>
> In Spanish: Validación: N comprobaciones pasan, M corregidas (<qué>), K abiertas (<qué>).

`N` is the count of checklist items that apply to the artifact: run
`check_docs.py --count <file>`. `M` and
`K` always name what they count, unless they are zero. The results go in the
line, never into the artifact. Closing a story updates `04-calidad.md` and
`historias.md`, so it ends with the same line.

## The artifact contract

```
docs/
├── 00-contexto.md          problem, users, team shape, methodology + why
├── 01-alcance.md           in scope, out of scope, assumptions
├── 02-requisitos.md        functional and non-functional, whole system
├── 03-arquitectura.md      structural decisions and their reasons
├── 04-calidad.md           quality attributes, verification results
├── referencias/            material the user supplied (brief, challenge), kept as is
└── features/
    └── <slug>/
        ├── requisitos.md   requirements for this feature only
        ├── historias.md    user stories + acceptance criteria
        ├── plan.md         ordering, dependencies, assignment
        └── decisiones.md   decisions made while building this feature
```

These files are versioned with the code and must be self-contained: never
write an artifact that depends on knowledge held only in this skill or in the
current conversation.

A feature-level requirement refines a system-level one and never adds scope. If
writing it reveals a new requirement, take it back to `02-requisitos.md` for
approval instead.

### AGENTS.md

Write it in the same turn as the first artifacts that create `docs/`, and update
it whenever what it points at changes. Its shape is in
`references/templates.md`. A repository with `docs/` and no `AGENTS.md` is a
defect.

If it already exists, add the documentation section and the three rules and
change nothing else: do not reorder, restructure or replace it. If the
repository keeps its agent instructions in `CLAUDE.md` or another file tools
read the same way, add them there instead and say which file you used. The
three rules in `AGENTS.md` are what reaches an agent that never loaded this
skill.

## Anti-patterns

- Saying the assumptions instead of writing them. If you had to assume it to
  proceed, it goes in a file in the same turn.
- Handing another skill a path instead of the criteria themselves.
- Proposing architecture, stack or patterns before requirements are approved.
  In early phases, ask whether a stack is already decided; never offer to pick
  one.
- Recording an option the user picked from your list as something they asked
  for.
- Inventing non-functional requirements as filler. Performance, availability
  and security targets are numbers the user gives you.
- Writing acceptance criteria that cannot be checked.
- Overwriting root-level artifacts when working on a feature. Feature work goes
  under `features/<slug>/`.
- Reopening a decision already recorded in `decisiones.md` because it did not
  come up in the current conversation.
- Producing all phases in one response because the request sounded simple.
- Asking the user to confirm something already answered in the conversation or
  written in `docs/`.
- Leaving text in an artifact that no longer applies after an edit.

## Reference files

- `references/interview.md`: question banks per phase and per mode
- `references/templates.md`: exact structure of every artifact
- `references/methodology.md`: how to choose and justify a methodology
- `references/validation.md`: checklist to run before presenting an artifact
- `references/rationale.md`: why the rules above are written the way they are
- `scripts/check_docs.py`: structural checker for `docs/`, run before presenting
