# Why the rules are written this way

`SKILL.md` holds the rules. This file holds the reasons, moved out so that the
rules fit in what survives a context compaction (the re-injected copy of a
skill is cut at about 20,000 characters). Read it when a rule seems to be in
the way, before deciding it does not apply.

## The artifacts

The fix for agents inventing missing details is not more instructions in the
prompt. It is a set of written artifacts that exist on disk before
implementation starts, and that implementation is required to consult.

The files are versioned with the code on purpose: any agent or person who opens
the repository later gets the context without needing this skill installed.
That only works if the documents are self-contained.

A genuinely new requirement written at feature level is scope smuggled in as a
refinement; it goes back to `02-requisitos.md` for approval.

## Working language

A path that changes with the language of the project is a path nothing else can
point at: not `AGENTS.md`, not another artifact, not a reader who has seen one
of these repositories before. That is why file names and mode names are never
translated while everything a person reads as a sentence is.

## Scale

Offering the short path is not skipping the process; a process nobody can
afford is one nobody uses. "Start a new project" for a forty-line script is
still a forty-line script.

## Reconnaissance

Skipping Phase 0.5 is the single most common way to produce a confident, wrong
proposal. Do not re-argue a settled choice because you would have chosen
differently. That is different from correcting a document that no longer
describes reality.

## The gate

An approval that is always granted carries no information. `methodology.md`
says a solo developer running full ceremonies is performing a ritual rather
than managing risk, and that judgement applies to this process as much as to
Scrum. A gate nobody reads is the same ritual with the cost moved onto the
user.

An undocumented skip is the same as no documentation. Naming the assumptions in
a message is not recording them: the message scrolls away and the next session
starts without it, which is the exact failure the artifacts exist to prevent.

If the justification for a methodology is missing, later phases will relitigate
the decision.

## Slicing

If the whole system is one feature, the folder means nothing and the structure
is dead weight. Two small features cost nothing; one oversized feature costs
traceability.

## The validation report

An artifact that has not been checked is a draft.

Half of the checklist is structural and does not need judgement, so the checker
does it. It reads only identifiers and file names, the two things this skill
never translates, so it behaves the same in every working language. It cannot
tell whether a criterion is observable, whether a requirement was invented, or
whether a decision lists an alternative nobody considered. What it can tell is
whether what you wrote points at something real, which is the half that was
never worth taking on trust.

Checking silently is indistinguishable from not checking, hence the line. `N`
is not a number you choose: anyone can count it against the checklist. A count
with nothing named next to it is the half of the line that cannot be checked,
and it is the half someone who never ran the checklist would still be able to
write. `0 fixed` and `0 open` are informative.

A structural change noted in a verification log is a decision filed where no
one will find it.

## Keep the earlier artifacts true

Writing forward is easy; going back is what gets skipped. In seven of ten
real sessions the user had to ask for the documents to be brought up to date,
and promises like "I'll note that for later" lived only in the conversation
until the user reminded the agent of them. A plan that now
describes a sequence nobody followed is not fixed by recording the reason
elsewhere, and an index missing entries is worse than no index.

## AGENTS.md

An existing `AGENTS.md` is the team's: it was there first, and it is usually the
only place the build commands and house conventions are written down. The
template is the shape of a file you are creating, not a shape to impose on one
you found.

An agent decides which skills to load from the text of the request, before
anything has looked at the disk, so this skill is not in context for a request
that carries no signal of what the repository holds ("the app won't start,
check the `.env`"). `AGENTS.md` is read anyway, by tools that open it on their
own. Writing the three rules into it is what puts them in front of an agent
that never loaded this skill.

## Execution contract

A session long enough to build something is long enough to be compacted. Reading
the story and `AGENTS.md` from disk costs one file read, and it is the
difference between a contract that still holds late in a long session and one
that quietly stopped applying while the documents went on looking healthy.

Rule 1: a change nobody wrote down is a change nobody agreed to.

Rule 2: small decisions are the ones that get lost, and their accumulation is
what makes a codebase incomprehensible.

Rule 3: blocked is an honest result, and it reads as a dead end unless you close
it. "Four blocked, all four need read access to the staging database, and they
close in one turn with it" is the same fact as four scattered rows and the only
form of it anyone can act on.

Rule 4: which data is yours is a fact that lives in the conversation unless you
record it, and by cleanup time any pattern that looks like test data also
matches whatever was there before. Deleting is the one step in this contract
that cannot be undone, so not deleting what you cannot separate is the same
answer as `blocked`: what could not be established is not acted on. A cleanup
list that grows for three stories is a list nobody runs. The command you hand
over runs with more permission than you had, and an instruction with a syntax
error is worse than none.

Writing automated tests is a different concern and belongs to a different
skill.

## Delegation

While another skill drives, the work still gets done, no criterion gets
verified, and the decisions taken along the way are never written down. The
stories read as untouched while the code has moved on without them. The other
skill works from what you put in front of it, and a path is something it has to
decide to open. A fix it applied on its own initiative is exactly the kind of
decision rule 2 exists for. The going-in half has been measured not to hold;
see the README, Limitations.

## Secrets

The rule holds even for keys documented as public, because the habit is what
protects the case where the key is not. A shell line is output like any other:
it is read, logged and stored. Rewriting a whole line that holds a secret
reproduces it twice, once in what you matched and once in what you wrote.

## Anti-patterns

- Announcing "I will assume Node, in-memory storage, and these fields" and then
  building is the failure the artifacts exist to prevent, only faster: the
  reasoning is stated where it cannot be found again.
- "The user chose between the alternatives offered" and "the user requested it"
  are different facts, and only one of them is true. This matters when someone
  reads the decision months later and takes it for a real constraint.
- "The interface is intuitive" is not a criterion; "a new user completes a basic
  sale within 15 minutes of first use" is.
- Text that no longer applies after an edit: an explanation of a state nothing
  is in any more, a reference to a section that was removed.
