---
name: groundwork
description: "Turns an idea or a feature request into approved, versioned documentation before any code is written, then keeps the implementation tied to that documentation. Use this whenever someone wants to start a new project, add a feature to an existing codebase, plan before coding, write requirements or user stories, pick a methodology, or record an architecture decision. Use it especially when the request is vague enough that writing code immediately would mean guessing, and when someone asks to skip the documentation or wants the code written straight away. Use it whenever the repository already contains a docs/ folder in the format below, including for work that is not documentation at all: fixing a bug, changing configuration, verifying or closing an acceptance criterion, or handing part of the work to another skill and taking it back. Those are the moments the recorded decisions exist to govern, and the moments they are most often bypassed."
license: Apache-2.0
metadata:
  version: 0.7.0
---

# Groundwork

Most agent work fails the same way: the agent starts coding from a one-line
request, invents the missing details, and produces something plausible that
nobody agreed to. The fix is not more instructions in the prompt. It is a set of
written artifacts that exist on disk before implementation starts, and that
implementation is required to consult.

This skill produces those artifacts and then enforces them.

## Working language

Write every artifact **and every message in the conversation** in the language
the user is writing in. If the user writes in Spanish, both the documents and
your replies are in Spanish. This survives context compaction: after a summary,
re-read what language the user is using rather than defaulting to English.

Two things are fixed identifiers and are never translated, because an agent or a
person opening this repository months from now has to find them without being
told where they are:

- File and directory names (`00-contexto.md`, `features/`, `historias.md`). A
  path that changes with the language of the project is a path nothing else can
  point at: not `AGENTS.md`, not another artifact, not a reader who has seen one
  of these repositories before. The feature slug itself is written in the working
  language.
- The mode names `new-project` / `adopt` / `new-feature`, which name the routing
  in Step 0.

Everything else a person reads as a sentence is translated: headings, story
status, verification results, descriptions, evidence, the validation line. Story
status uses the working language (`pendiente`, `en progreso`, `verificada`), and
the verification results `pass` / `fail` / `blocked` are written `pasa` / `falla`
/ `bloqueado`.

## Step 0: establish mode and environment

Do this before anything else. It takes one look at the workspace and, at most,
one question.

**Environment.** If a filesystem is available, artifacts are written to `docs/`.
If not (a plain chat interface), produce exactly the same Markdown in the
conversation instead, one document per message, and tell the user which file
each block corresponds to so they can save it themselves.

**Scale.** Before choosing a mode, judge whether this work needs the process at
all. It does not when the whole change is smaller than the documentation
describing it would be: a script, a one-file utility, a spike meant to be thrown
away, a typo, a rename, a single well-specified function. In those cases say so
in one line, offer the short path, and do the work. Do not open a phase.

The judgement is about the size of the change, not the phrasing of the request.
"Start a new project" applied to a forty-line photo-renaming script is still a
forty-line script. When it is genuinely borderline, ask once, "this looks small
enough to just build; want me to, or should we scope it first?", and take the
answer. Offering the short path is not skipping the process; a process nobody can
afford is one nobody uses.

**Mode.** Inspect the workspace:

| What you find                             | Mode          | Where to start          |
| ----------------------------------------- | ------------- | ----------------------- |
| Empty or near-empty workspace             | `new-project` | Phase 1                 |
| Existing code, no `docs/`                 | `adopt`       | Phase 0.5, then Phase 1 |
| Existing code with `docs/` in this format | `new-feature` | Phase 0.5, then Phase 3 |

Never guess the mode from the wording of the request alone. "Add a login page"
in an empty directory is a new project; the same sentence in a mature repository
is a feature.

## Phase 0.5: reconnaissance (any mode with existing code)

Skipping this is the single most common way to produce a confident, wrong
proposal. Before asking the user anything about the feature:

1. Read `docs/` if it exists, starting with `00-contexto.md`,
   `03-arquitectura.md` and any `features/*/decisiones.md`. These record
   decisions already closed.
   Do not reopen them on preference. Do not re-argue a settled choice because
   you would have chosen differently. That is different from correcting a
   document that no longer describes reality: if the code contradicts what is
   written, report the divergence and ask which one is wrong. Never edit a
   recorded decision without saying what diverged.
2. Read enough of the codebase to state, in three sentences, what the system
   does, how it is layered, and what conventions it follows.
3. Report that summary back and ask the user to correct it.

In `adopt` mode, offer to reconstruct `00-contexto.md` through
`04-calidad.md` from the code by reverse engineering, and mark every
reconstructed statement as inferred rather than confirmed. Do not proceed to
feature work until the user has reviewed it.

## The gate

Each phase ends with a written artifact and an explicit approval from the user.

Present the artifact, state what the next phase will do, and stop. Do not chain
phases in one response. Approval means the user says so; silence, a thumbs-up
emoji, or a question about something else is not approval.

An approval that is always granted carries no information. When three gates in a
row come back approved with nothing corrected and nothing asked, say so and
offer to merge the remaining stops: Phase 1 with 2, Phase 3 with 4, each still
producing both artifacts and still ending in one approval. `methodology.md` says
a solo developer running full ceremonies is performing a ritual rather than
managing risk, and that judgement applies to this process as much as to Scrum.
The artifacts are the point. The number of stops is not, and a gate nobody reads
is the same ritual with the cost moved onto the user.

If the user asks to skip a phase, comply, but write the skipped artifact as a
stub recording that it was skipped and what assumptions were therefore adopted.
An undocumented skip is the same as no documentation.

Write the stub in the same turn as the work, not after it. Naming the
assumptions in a message is not recording them: the message scrolls away and the
next session starts without it, which is the exact failure the artifacts exist to
prevent. If the whole process was skipped and there is no `docs/` yet, one file
is enough: `docs/00-contexto.md`, holding what was asked for, what was skipped,
and every assumption adopted in its place. Three of those assumptions are almost
always the same three: the stack, where data is stored, and the shape of the
main entity. If you had to pick them to write the code, they belong in the
file.

## Phases

Read `references/interview.md` before Phase 1 or 3 for the question banks. Read
`references/templates.md` before writing any artifact for the exact structure.

**Phase 1: Context and scope.** Interview the user about the problem, the
users, the constraints, and the boundaries. Choose a methodology using
`references/methodology.md` and record the choice _with its justification_. If
the justification is missing, later phases will relitigate the decision.
Produces `00-contexto.md` and `01-alcance.md`.

**Phase 2: Requirements.** Derive functional and non-functional requirements
from the scope. Every non-functional requirement must trace to a constraint the
user actually stated; if it does not, ask instead of inventing one.
Produces `02-requisitos.md`.

**Phase 3: Feature definition.** Slice the work into a feature (see below),
convert its requirements into user stories with verifiable acceptance criteria,
and order them. Produces `features/<slug>/requisitos.md`, `historias.md` and
`plan.md`.

**Phase 4: Architecture.** Only after requirements are approved. Decide
structure, boundaries and dependencies, and record each decision with its
alternatives and consequences. Produces or updates `03-arquitectura.md` and
`features/<slug>/decisiones.md`.

**Phase 5: Implementation.** Governed by the execution contract below.

**Phase 6: Verification.** Check each acceptance criterion against what was
built and record the result. Produces or updates `04-calidad.md`.

### How to slice a feature

A feature is a set of stories that deliver value to one kind of user and can be
finished and verified together. Cut along user roles and along coherent flows,
not along technical layers.

If the whole system is one feature, the folder means nothing and the structure
is dead weight. When in doubt, split: two small features cost nothing, one
oversized feature costs traceability. Practical ceilings: more than about six
stories, or stories serving two different user roles, means split. Name the
slice for what the user gets (`solicitud-de-reserva`), not for the release
(`v1`).

Propose the slicing to the user before writing the artifacts, with the reason
for each cut, and stop for approval. Only the first slice gets full artifacts;
the rest are named and left for later.

### The validation report

Before presenting any artifact, check it against `references/validation.md`.
Fix what fails, then present. An artifact that has not been checked is a draft.

Half of that checklist is structural and does not need your judgement, so do not
spend it there. Run the checker, which sits next to this file in the skill
directory and takes the path to `docs/` in the project:

```sh
python .claude/skills/groundwork/scripts/check_docs.py docs/
```

That is where the skill is installed for one project. Globally it is under the
agent's own skills directory instead, so use the path this file was read from
rather than the one printed here.

It walks the identifier graph and reports what is broken: a reference to an
`RF`, `HU`, `CA` or `AD` that nothing defines, a requirement no story covers, a
story with no criterion, a decision missing from the index in
`03-arquitectura.md`, a pointer to a file that is not there. It reads only
identifiers and file names, the two things this skill never translates, so it
behaves the same in every working language. What it reports is fixed before
presenting, exactly like a checklist failure.

A clean run is not a validated artifact. The checker cannot tell whether a
criterion is observable, whether a requirement was invented, or whether a
decision lists an alternative nobody considered, and that half is still read by
hand. What it can tell you is whether what you wrote points at something real,
which is the half that was never worth taking on trust.

Checking silently is indistinguishable from not checking, so end every artifact
presentation with this line, filled in. The structure is fixed: the label, then
three counts in this order, each naming what it refers to. The wording is in the
working language, like everything else the user reads:

> Validation: N checks passed, M fixed (<what>), K open (<what>).
>
> In Spanish: Validación: N comprobaciones pasan, M corregidas (<qué>), K abiertas (<qué>).

`N` is not a number you choose. It is the count of checklist items that apply to
this artifact, the `Every artifact` block in `references/validation.md` plus the
block for this file. It is fixed before you start, and anyone can count it
against the checklist and see whether it matches. `M` and `K` name what was fixed
and what is open, always: a count with nothing named next to it is the half of
the line that cannot be checked, and it is the half someone who never ran the
checklist would still be able to write.

If nothing was fixed and nothing is open, say so. `0 fixed` and `0 open` are
informative, and are the two counts that need no name after them because there is
nothing to name. Never write the checklist results _into_ the artifact; the
artifact holds the work, the report holds the evidence that the work was
checked.

This applies to implementation and verification too, not only to the document
phases. Closing a story updates `04-calidad.md` and `historias.md`, so it ends
with the same line.

Each artifact holds one kind of content, and mixing them buries things where
nobody looks: `04-calidad.md` holds criteria and their results, `decisiones.md`
holds decisions, `plan.md` holds order and dependencies. A structural change
noted in a verification log is a decision filed where no one will find it. The
diagnosis of an environment problem (a wrong variable, a migration not yet run)
belongs in the conversation and in no artifact at all.

## The artifact contract

```
docs/
├── 00-contexto.md          problem, users, team shape, methodology + why
├── 01-alcance.md           in scope, out of scope, assumptions
├── 02-requisitos.md        functional and non-functional, whole system
├── 03-arquitectura.md      structural decisions and their reasons
├── 04-calidad.md           quality attributes, verification results
└── features/
    └── <slug>/
        ├── requisitos.md   requirements for this feature only
        ├── historias.md    user stories + acceptance criteria
        ├── plan.md         ordering, dependencies, assignment
        └── decisiones.md   decisions made while building this feature
```

These files are versioned with the code, on purpose. Any agent or person who
opens the repository later gets the context without needing this skill
installed. That only works if the documents are self-contained, so never write
an artifact that depends on knowledge held only in the skill or in the current
conversation.

A feature-level requirement refines a system-level one; it never adds scope. If
writing it reveals a genuinely new requirement, stop and take it back to
`02-requisitos.md` for approval instead of smuggling it in as a refinement.

### Keep the earlier artifacts true

Writing forward is easy; going back is what gets skipped, and a document that
describes something that did not happen is worse than no document, because it is
read with the same trust as an accurate one.

Whenever reality diverges from what an earlier artifact says, fix that artifact
in the same turn, not only record the new decision:

- A later phase discovers scope the scope document does not have → add it to
  `01-alcance.md` and resolve or restate the affected open questions.
- Implementation departs from the order or dependencies in `plan.md` → correct
  `plan.md`. Recording the reason in `decisiones.md` does not fix a plan that
  now describes a sequence nobody followed.
- A new decision is written in a feature's `decisiones.md` → add it to the index
  in `03-arquitectura.md`. An index missing entries is worse than no index.
- A decision is superseded → mark the old one, never delete it.

Say what you updated when you present. Two artifacts that contradict each other
are a defect, and the older one is usually the wrong one.

### AGENTS.md is part of the contract

Write it in the same turn as the first artifacts that create `docs/`, and update
it whenever what it points at changes. Its shape is in `references/templates.md`.
A repository with `docs/` and no `AGENTS.md` is a defect in the same way an
incomplete decision index is.

When the file already exists, add the documentation section and the three rules
to it and change nothing else. Do not reorder it, do not restructure it, and
never replace it: what is there is the team's, it was there first, and it is
usually the only place the build commands and the house conventions are written
down. The template is the shape of a file you are creating, not a shape to
impose on one you found. If the repository keeps its agent instructions in
`CLAUDE.md` or in another file that tools read the same way, add them there
rather than creating a second entry point, and say which file you used.

It carries more than its index. An agent decides which skills to load from the
text of the request, before anything has looked at the disk, so this skill is not
in context for a request that carries no signal of what the repository holds.
"The app won't start, check the `.env`" is the shape of it. `AGENTS.md` is read
anyway, by tools that open it on their own. Writing the three execution rules
into it is what puts them in front of an agent that never loaded this skill,
which is the one case where they are needed and absent.

## Execution contract

These rules apply for the rest of the session, not only at the moment they are
read.

A session long enough to build something is long enough to be compacted, and
what survives a summary is `docs/`, not this contract. So read from disk rather
than from memory at the two moments that matter: before implementing a story,
open the story; before verifying a criterion, open the criterion and
`AGENTS.md`. It costs one file read, and it is the difference between a contract
that still holds late in a long session and one that quietly stopped applying
somewhere in the middle, while the documents went on looking healthy. If
`AGENTS.md` turns out not to carry the three rules, that is the defect to fix
before continuing.

1. **No code without a story.** Before implementing, read the relevant story and
   its acceptance criteria in `features/<slug>/historias.md`. If no story covers
   the change, stop and ask whether to write one. A change nobody wrote down is
   a change nobody agreed to.

2. **Record any decision someone could later want to reverse.** Consult
   `03-arquitectura.md` first; if the change contradicts what is recorded, stop.
   Otherwise the test is not what category the change falls into but whether a
   developer arriving in six months could look at it, wonder why it is like
   that, and be unable to tell. That includes migrating to a replacement API,
   changing the shape of a shared type, adding a config flag, and choosing where
   a new concern lives, not only new modules and dependencies. These small
   decisions are the ones that get lost, and their accumulation is what makes a
   codebase incomprehensible. Recording one costs six lines in `decisiones.md`.

3. **Verify by observation, never by argument.** Each criterion gets one of
   three results:
   - `pass`: observed working, with what was observed written down.
   - `fail`: observed not working.
   - `blocked`: could not be observed, with the missing resource named. The
     story stays open.

   A criterion is never marked `pass` because the design implies it should
   work, because a library guarantees it, or because the code was reviewed and
   looks right. If the reasoning is sound but nothing was observed, the result
   is `blocked`, not `pass`. This is most tempting exactly where it matters
   most, in security criteria, so when the argument feels conclusive, that is
   the signal to mark it blocked and say what would settle it.

   A criterion nobody could ever observe was written badly. "The interface is
   intuitive" has no reading under which two people would have to agree, so it
   is rewritten rather than approved. A criterion you cannot observe from where
   you are sitting is a different finding and is not rewritten: it is `blocked`,
   and the resource that would settle it gets named. Shrinking criteria until
   they fit the tools available in this session is how a set of criteria stops
   describing the system and starts describing the agent.

   Blocked is an honest result, and it reads as a dead end unless you close it.
   When you finish verifying, gather the blocked criteria into one request:
   which ones, the single resource that unblocks them, and what you would do
   with it. "Four blocked, all four need read access to the staging database,
   and they close in one turn with it" is the same fact as four scattered rows
   and the only form of it anyone can act on.

4. **Leave the environment as you found it.** Test data created to verify a
   criterion is deleted once observed, including rows in real databases and
   accounts created for a login test. Say what you are about to delete, then say
   that you deleted it.

   Only what you created in this session, and only what you wrote down as you
   created it: the identifier, the row, the account name. Which data is yours is
   a fact that lives in the conversation unless you record it, and by the time
   you clean up, any pattern that looks like test data (`test%`, today's rows,
   the resource you happened to use) also matches whatever was there before you
   arrived. Deleting is the one step in this contract that cannot be undone, so
   when you cannot tell your data from the data that was already there, you do
   not delete: hand over the identifying criterion and say what you could not
   separate. That is the same answer as `blocked`: what could not be
   established is not acted on.

   When you lack the permissions to delete it, hand the user the exact command
   at the end of that story rather than accumulating it across several. A list
   that grows for three stories is a list nobody runs. That command runs with
   more permission than you had, so it names the rows it removes rather than a
   pattern that matches them. Check it before giving it; an instruction with a
   syntax error is worse than none. Say which data you deliberately kept, and
   why.

Verifying acceptance criteria is in scope. Designing a test suite, choosing a
testing framework, or writing automated tests is not. That is a different
concern and belongs to a different skill.

### When another skill writes the code

While another skill is driving, this contract stops being applied: the work still
gets done, no criterion gets verified, and the decisions taken along the way are
never written down. The stories read as untouched while the code has moved on
without them.

**Going in**, when delegation is first mentioned rather than when it begins:
write the criteria into the handoff itself, each identifier with its text and its
threshold where it has one, plus the constraints already recorded in
`03-arquitectura.md`. Pointing at `historias.md` is not handing anything off; the
other skill works from what you put in front of it, and a path is something it
has to decide to open.

**Coming back**, in the same session:

1. Verify each acceptance criterion the work covers, by observation, and record
   the results in `04-calidad.md` and the story status in `historias.md`.
2. Record in `decisiones.md` the decisions taken while building, including the
   ones the other skill made on its own. A fix it applied on its own initiative
   is exactly the kind of decision rule 2 exists for.
3. If the work exposed a real gap that no criterion covers, say so and offer to
   write the story. Do not silently absorb it.
4. Point to any artifacts it wrote from `AGENTS.md`, with what they govern. Do
   not rewrite them into this format; they have their own shape for a reason.

Measured twice, the going-in half does not hold. What was tried and what it
produced is in the README under Limitations. The coming-back half is the part
this contract can actually close.

## Secrets

Credentials, tokens and connection strings never appear in your output, in an
artifact, or in a commit. This holds even for values the user pasted and even
for keys documented as public: the habit is what protects the case where the
key is not.

When a secret must be handled, refer to it by variable name and never echo its
value. Not in a diff, not in a summary, not to confirm it was set, and not as
an argument to a command you run. A shell line is output like any other: it is
read, logged and stored, and it is the surface most easily reached for when a
value has to be supplied to something. Pass the variable, or run the thing that
already reads it; never inline the value.

Editing a file that holds a secret is the same problem seen from the other side,
because the line you have to change is the line the secret lives on. Match the
smallest fragment that is unique and does not contain the value (the port, the
host, the flag) instead of the whole line. Rewriting the whole line reproduces
the secret twice, once in what you matched and once in what you wrote.

Keep an example file with empty values, and mark in it which variables are
secret and which are safe to expose to a client. If a secret has already been
printed in this session, say so plainly and recommend rotating it.

## Anti-patterns

- Saying the assumptions instead of writing them. Announcing "I will assume
  Node, in-memory storage, and these fields" and then building is the failure
  the artifacts exist to prevent, only faster: the reasoning is stated where it
  cannot be found again. If you had to assume it to proceed, it goes in a file
  in the same turn.
- Handing another skill a path instead of the criteria themselves.
- Proposing architecture, stack or patterns before requirements are approved.
  In early phases, ask whether a stack is already decided; never offer to pick
  one.
- Recording an option the user picked from your list as something they asked
  for. "The user chose between the alternatives offered" and "the user requested
  it" are different facts, and only one of them is true. This matters when
  someone reads the decision months later and takes it for a real constraint.
- Inventing non-functional requirements as filler. Performance, availability and
  security targets are numbers the user gives you, not numbers you make up.
- Writing acceptance criteria that cannot be checked. "The interface is
  intuitive" is not a criterion; "a new user completes a basic sale within 15
  minutes of first use" is.
- Overwriting root-level artifacts when working on a feature. Feature work goes
  under `features/<slug>/`.
- Reopening a decision already recorded in `decisiones.md` because it did not
  come up in the current conversation. Read before proposing.
- Producing all phases in one response because the request sounded simple.
- Asking the user to confirm something already answered earlier in the
  conversation or already written in `docs/`.
- Leaving text in an artifact that no longer applies after an edit: an
  explanation of a state nothing is in any more, a reference to a section that
  was removed.

## Reference files

- `references/interview.md`: question banks per phase and per mode
- `references/templates.md`: exact structure of every artifact
- `references/methodology.md`: how to choose and justify a methodology
- `references/validation.md`: checklist to run before presenting an artifact
- `scripts/check_docs.py`: structural checker for `docs/`, run before presenting
