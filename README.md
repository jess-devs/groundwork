# Groundwork

An [Agent Skill](https://github.com/anthropics/skills) that turns an idea or a
feature request into approved, versioned documentation before any code is
written and then keeps the implementation tied to it.

## The problem

Agents fail the same way over and over: they start coding from a one-line
request, invent the missing details, and produce something plausible that nobody
agreed to. More instructions in the prompt do not fix it, because the missing
piece is not instruction it is a record. Groundwork produces that record as
files on disk, and makes implementation consult it.

## What it produces

```
docs/
├── 00-contexto.md          -> problem, users, team shape, methodology + why
├── 01-alcance.md           -> in scope, out of scope, assumptions
├── 02-requisitos.md        -> functional and non-functional requirements
├── 03-arquitectura.md      -> structural decisions and their reasons
├── 04-calidad.md           -> quality attributes, verification log
└── features/<slug>/
    ├── requisitos.md       -> requirements for this feature only
    ├── historias.md        -> user stories + acceptance criteria
    ├── plan.md             -> ordering, dependencies, assignment
    └── decisiones.md       -> decisions made while building this feature
```

These live in the repository on purpose. Anyone or any agent who opens it
later gets the context without having this skill installed.

Three rules govern implementation once the documents exist: no code without a
story, record any decision someone could later want to reverse, and verify by
observation rather than by argument. A criterion that could not be observed is
recorded as `blocked`, not waved through.

Work that is smaller than the documentation describing it takes the short path
instead. The process is not the point; the record is.

Nine cross-referenced files rot quietly, so one part of keeping them true is not
left to an agent's promise that it looked:

```sh
python .claude/skills/groundwork/scripts/check_docs.py docs/
```

It walks the identifier graph and exits nonzero on a reference to an `RF`, `HU`,
`CA` or `AD` that nothing defines, a requirement no story covers, a story with
no criterion, a decision missing from the index, a pointer to a file that is not
there, a missing header block. It reads identifiers and file names only, which
is why those are the two things the skill never translates, and it works the
same on a Spanish project and an English one. It cannot tell you whether a
criterion is observable or whether a requirement was invented. That half is
still read by hand, and it is the half that was always worth reading.

## What it is for, and what it is not

Software with users, stories and criteria that can be observed. That is the shape
the nine files are cut for, and the shape they earn their cost on.

They are not cut for a single-author project that grows by revision rather than
by feature: a skill, a library of prose, a repository whose unit of change is a
rule and not a story. This repository is one of those, and it does not use
groundwork on itself: its `CHANGELOG.md` does the work `decisiones.md` would do,
in one file, chronologically, and does it better for this case. That is not an
oversight to be embarrassed about, it is the boundary. `SKILL.md` already says
that when the whole system is one feature the folder structure is dead weight;
this is what that looks like from outside.

The part of groundwork that generalises past the boundary is the smallest part:
write the decision down where the next person will find it, with what it cost.

## Install

```sh
npx skills add jess-devs/groundwork
```

That is the [`skills` CLI](https://github.com/vercel-labs/skills). It reads this
repository, finds the skill, and installs it into the agents you have on the
machine. Nothing is published to npm the repository is the registry.

By default it installs into the current project, at `.claude/skills/groundwork`.
Add `-g` to install it globally instead, for every project:

```sh
npx skills add jess-devs/groundwork -g
```

Without `--agent` it installs into every agent it detects. Name one to narrow it:

```sh
npx skills add jess-devs/groundwork --agent claude-code
```

The CLI keeps one canonical copy under `.agents/skills/` and links every agent's
skills directory to it, so a single `npx skills update` moves all of them at
once. Installing for one agent alone copies instead, because there is nothing to
share. `--copy` forces copies everywhere, and `npx skills remove groundwork`
uninstalls.

### Without the CLI

The skill is a directory of Markdown files, so copying it works just as well:

```sh
git clone https://github.com/jess-devs/groundwork.git
cp -r groundwork/skills/groundwork ~/.claude/skills/groundwork
```

Use `.claude/skills/groundwork` for the current project only, or your own agent's
skills directory. It follows the open Agent Skills standard and uses only
standard frontmatter fields, so the same directory works in other agent CLIs
copy it to their skills directory instead.

## Working language

Documents are written in whatever language you write in. Two things are fixed
identifiers and are never translated, because whoever opens the repository months
from now has to find them without being told where they are: file and directory
names, and the mode names `new-project` / `adopt` / `new-feature`. Everything
else is prose and gets translated including the
verification results, written `pasa` / `falla` / `bloqueado` in a Spanish
project.

Those fixed names are in Spanish, and that is a cost this repository is choosing
to keep paying. The argument for freezing them is that a path which changes with
the language of the project is a path nothing else can point at; the argument
holds whichever language they are frozen in, and this one was written in
Spanish first. Renaming them now would invalidate every eval fixture and every
repository already carrying a `docs/`, which is a worse trade than the one an
English-speaking reader makes on their first morning. The `AGENTS.md` table is
the map: it names every file and what it holds, in the language of whoever is
reading.

## Repository layout

```
skills/groundwork/  -> the skill itself this is what you install
  SKILL.md          -> body: routing, gates, contract, execution rules
  references/       -> interview banks, templates, methodology, checklist
  scripts/          -> check_docs.py, the structural checker for docs/
CHANGELOG.md        -> every rule, and the failure that produced it
```

## On the changelog

Every rule in this skill exists because something went wrong without it. The
changelog records which failure produced which rule, so that anyone editing it
knows what a line is holding up before removing it. That history is worth more
than the skill.

## Evals

The skill is developed against a suite of 17 cases, each a prompt run headless
against a clean copy of a fixture repository with the skill installed. Five carry
a mechanical check; the rest are read by hand against what the case says should
happen.

The suite is not part of this repository. Its fixtures include a file holding a
deliberately fake connection string, which is the shape that secret scanners
match on, and a case that has not been read yet is closer to a note than to a
test. What the runs produce ends up here instead, as the reasons in the
changelog: every rule below 0.5.0 came out of a case that failed.

Some of what the current suite has measured, on Claude Sonnet:

- The skill loads in 15 of 17 cases. The two it misses are the two whose trigger
  would depend on having looked at the repository first see Limitations.
- Most cases stop at a gate and wait for an approval that never comes in a
  headless run, so the suite sends scripted replies that approve and ask to
  continue, and nothing else. A reply that supplied content would be grading the
  fixture rather than the skill.
- A case where the skill did not load is not evidence about the skill. It is the
  model without it, and its result is recorded that way.

## Limitations

- Twelve of the seventeen eval cases still need a human to read the transcript;
  only five have a mechanical check.
- **The skill cannot reliably fire on repository state.** Its `description` says
  to use it whenever the repository already contains `docs/`, but an agent
  decides which skill to load from the text of the request, before anything has
  looked at the disk. A request like "the app won't start, check the `.env`"
  carries no signal that the repository is documented, so the skill does not
  load and none of its rules are in context. Measured: in the 0.5.1 run it
  activated in 15 of 17 cases, and the two it missed 8 and 14 are exactly
  the two whose trigger would depend on seeing the repository first. Widening
  the description to catch them would mean firing on every debugging request in
  every repository, which is worse. The verdicts on those two cases describe the
  model without the skill.

  0.6.0 stops trying to fix this from the description and moves the weight to
  `AGENTS.md`, which tools read on their own whether or not any skill loaded, and
  which now carries the three execution rules in full instead of pointing at
  them. That separates two things this project had been treating as one: whether
  the skill activates, and whether its rules are in context. The second no longer
  depends on the first. **Untested.** The fixtures for 8 and 14 carry no
  `AGENTS.md`, so the suite has never measured the case this change is aimed at;
  seeding them and re-running is the open experiment.
- Eval 14 fails by design it encodes a behaviour the skill does not yet
  guarantee. Softening it would hide the gap. It currently reports `pass` for
  the wrong reason: the skill never loads, so nothing could have dragged the
  process in.
- Handing work to another skill does not reliably carry the acceptance criteria
  with it. The rule says to write each identifier, its text and its threshold
  into the handoff; measured twice, the skill answered "I'm going to use another
  skill for this" with a recommendation and a wait instead. Two attempts at
  rewording it did not change the behaviour, so it is recorded here rather than
  patched again.

  0.6.0 does not attempt a third rewording either. It cuts the section in
  `SKILL.md` roughly in half, because a rule that two measurements say is not
  followed was still spending context arguing for itself next to rules that are
  followed. What was cut is the argument, not the instruction: the going-in rule
  still stands in one sentence, and the coming-back half is the part that was
  always observed to work and is now the bulk of what the section says: verify,
  record the decisions, name the gaps, point at the artifacts. The likeliest
  reading of the two failures is that the going-in half asks for a turn the skill
  does not have: when the user says "I'm going to use another skill for this",
  answering with twelve numbered criteria is a move the model avoids for
  conversational reasons, and no wording changes that. If it is ever fixed, it
  will be fixed by writing the criteria to a file the other skill is handed, not
  by a better sentence.
- Language persistence across context compaction is not covered by any eval.
- Two situations have no eval at all: a feature with no parent requirement, and
  a plan whose stated dependency is the one that should be pushed back on.
- **The suite measures the first few turns, and the field is the fiftieth.**
  Every case is one prompt run headless against a clean fixture, so no case
  reaches the point where the session is compacted and the contract stops being
  in context while `docs/` goes on looking healthy. 0.7.0 answers it by making
  the two moments that matter read from disk instead of from memory, the story
  before implementing and the story plus `AGENTS.md` before verifying, on the
  grounds that a summary keeps the documents and drops the rules. Nothing has
  measured that. A case that runs long enough to be compacted is the missing
  fixture, and it would also settle the language bullet above.
- **Nothing runs the checker.** `check_docs.py` turns the structural half of
  `validation.md` into an exit code, which is more than a promise, but it is
  still the agent deciding to run it. A pre-commit hook or a CI step would take
  that decision away, and neither ships here: this repository has no `docs/` of
  its own to hook it to, so it would be shipping an untested convenience.
- **A gate nobody reads is not measured either.** 0.7.0 asks the skill to notice
  three consecutive approvals with nothing corrected and offer to merge the
  remaining stops. It comes from the same argument `methodology.md` makes about
  ceremonies that get skipped, not from a run. Headless evals approve
  everything by construction, so the suite is the wrong instrument for it.
- **Co-resident skills, not just delegated ones.** The handoff limitation above
  is about work handed to another skill. The commoner case is several skills
  loaded at once, each declaring rules for the rest of the session, one of them
  saying stop and wait while the others say ship. There is no handoff moment to
  instrument, and no fix here beyond naming it.
- **The evidence is reproducible only by its author.** The suite is not in this
  repository, so the numbers in the changelog can be read but not re-run, by
  anyone else or by a later model. That is the weakest point of a project whose
  entire claim is that its rules came from measurements. Publishing the case
  descriptions and the scripted-reply protocol, with the fixture's fake
  connection string generated at setup rather than committed, is what would fix
  it, and it is not done.

## License

Apache-2.0
