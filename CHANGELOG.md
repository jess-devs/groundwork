# Changelog

## 0.7.0 - 2026-09-02

The first version whose changes come from a premortem: not from a case that
broke, and not from building the strongest case against the skill, but from
assuming it had already failed in the field and working backwards to what would
have killed it. That is the weakest evidence in this changelog so far, weaker
than 0.6.0's audit, and every entry below is a prediction. None of them has been
measured. The one thing this version can point at that is not a prediction is a
regression it removes, and a script that either exits zero or does not.

**The contract lives in context, and context is the one thing that does not
survive a long session.** Every rule here says it applies for the rest of the
session. A session long enough to build a feature is long enough to be
compacted, and what a summary keeps is `docs/`, because it is on disk, while the
contract governing it is prose in a window that got shorter. The failure is
silent and it looks like success: the documents stay healthy while the rules
behind them quietly stop being applied, somewhere in the middle, and the
verification log starts filling with reasoned passes again.

The two moments that matter now read from disk. Before implementing a story,
open the story. Before verifying a criterion, open the criterion and
`AGENTS.md`, which since 0.6.0 carries the three rules in full. The cost is a
file read. The suite cannot see any of this: every case is one prompt against a
clean fixture, so the entire eval surface sits inside the first handful of turns
and the regime this is aimed at has never been run.

**A gate that is always approved is the ceremony this skill tells other people
not to perform.** Six phases, six stops, and nothing in the skill noticing when
the stops have become a formality. `methodology.md` says a solo developer
running full ceremonies is performing a ritual rather than managing risk, and
that ceremonies consistently skipped are evidence the choice was wrong. Neither
sentence was ever pointed at this process. Three gates in a row approved with
nothing corrected and nothing asked is now a signal to say so and offer to merge
the remaining stops, two phases per approval, both artifacts still written. A
headless eval approves everything by construction, so the suite is the wrong
instrument for this and will not settle it.

**The structural half of the checklist was a promise, and it is now an exit
code.** `validation.md` asks whether every internal reference points at
something that exists, whether every requirement in a feature has a story,
whether every story has a criterion, whether the decision index lists every
decision. Those are facts about a graph of identifiers, and an agent has been
asserting them the same way it asserts everything else: by saying so. Nine
cross-referenced files across a real project drift, and drift of exactly this
kind is invisible to a reader who trusts the document.

`scripts/check_docs.py` walks that graph and reports what is broken. The items
it settles are marked `[checker]` in `validation.md`. It reads identifiers and
file names, the two things this skill never translates, which is the first time
that rule has paid for itself in something other than readability: the checker
behaves identically on a Spanish project and an English one. It cannot tell
whether a criterion is observable or whether a requirement was invented, and
that half is still read by hand. This is the answer 0.6.0 owed the validation
line. Making `N` countable made half the line checkable; computing part of it
ends the argument for that part.

**0.6.0 pointed a mandate at a file that belongs to somebody else.** 0.5.4 said
to offer an `AGENTS.md` when the repository had none. 0.6.0 removed both the
condition and the offer, made writing it part of the contract, and added a
validation check that the file carries the three rules in full, while
`templates.md` went on showing a whole-file template starting at the project
title. A mandate, a full-file template and a check on the file's contents is
enough to make an agent rewrite a two-hundred-line `AGENTS.md` holding a team's
build commands. Nothing anywhere said to merge rather than replace. That is a
regression this version introduces the fix for rather than a prediction: it was
in the diff.

An existing file is now added to and not restructured, everything already in it
kept in the order it was in, and a repository that uses `CLAUDE.md` for the same
purpose gets the rules there instead of a second entry point.

**The rule that forbids the reasoned pass had no way to end.** Most criteria
worth writing cannot be observed from where an agent sits, so a faithful run
produces a log that is mostly `blocked` next to a plain agent reporting done.
Rule 3 was correct and had no closing move. Blocked criteria are now gathered
into one request that names the single resource that would settle them and what
would happen with it, which is the same fact in the form somebody can act on.

The same rule also said a criterion that can never be observed with the
available means was written badly. Read literally, "available means" is this
session's means, and following it degrades good criteria until they describe the
agent rather than the system. Unobservable by anyone and unobservable by you are
now different findings: the first is rewritten, the second is `blocked` with the
missing resource named.

**The filenames are in Spanish, and the README now says so on purpose.** The
argument for freezing paths is that a path which changes with the language of
the project is a path nothing else can point at, and it holds whichever language
they are frozen in. This one was written in Spanish first. Renaming now would
invalidate every fixture and every repository already carrying a `docs/`, which
is a worse trade than the one a reader makes on their first morning, and the
`AGENTS.md` table already names every file in the reader's own language. Stating
the boundary is the whole change; nothing was renamed.

**Not addressed.** Nothing runs the checker: it is still the agent deciding to
run it, and a hook or a CI step would take that decision away, but this
repository has no `docs/` of its own to test one against. Several skills loaded
at once, each declaring a persistent contract, is a commoner case than the
delegated handoff already recorded and has no fix here beyond being named. The
suite still lives outside this repository, so every number in this changelog can
be read and not re-run by anyone else, which is the weakest joint in a project
whose claim is that its rules came from measurements. And the two carried
forward from 0.6.0 both still stand: there is no way to measure which rules are
followed rather than which cases pass, and the escape hatch in Step 0 still asks
for the size of the change before anything has looked at the repository.

This version adds five rules and a script and removes nothing, which is the
seventh version in a row that can be said of.

## 0.6.0 - 2026-08-26

The first version whose changes come from an attack rather than from a failed
run. Every rule below 0.5.0 came out of a case that broke; these came out of
building the strongest case against the skill and keeping what survived. That is
a weaker kind of evidence than a measurement and is marked as such: three of
these six are predictions, not observations.

**The validation line asked to be trusted for the one reason it forbids.** Rule 3
bans the reasoned pass: a criterion is never `pass` because the design implies
it, and when the argument feels conclusive that is the signal to mark it
`blocked`. Four paragraphs earlier, the skill requires ending every artifact with
`Validation: N checks passed, M fixed, K open`, on the grounds that checking
silently is indistinguishable from not checking. It is, and so is emitting the
line. 0.4.0 recorded this as unfalsifiable and left it there, as a measurement
nobody had. It is worse than a missing measurement: an artifact with the line is
read as checked, so a line that can be written without checking transfers
confidence without transferring evidence, and it was made mandatory everywhere.

`N` is no longer a number anyone chooses. It is the count of checklist items that
apply to the artifact, the shared block plus the block named after the file, so
it is fixed before the check starts and can be counted back against
`validation.md`. `M` and `K` must name what they refer to. That does not make the
line true, but it makes part of it wrong in a way someone can see, which is more
than it had.

**Activation and presence were the same problem, and only one of them was
unsolvable.** The README concluded that the skill cannot fire on repository state
and that widening the description to catch it would be worse. Both hold. What did
not follow is that the rules must therefore be absent: `AGENTS.md` is read by
tools on their own, whether or not any skill loaded, and `templates.md` already
had it carrying the three execution rules in full. It was offered rather than
written, at the end of a section, and the Limitations entry describing the gap
never mentioned it.

It is now part of the contract, written in the same turn as the artifacts that
create `docs/`, checked by `validation.md`, and a repository with `docs/` and no
`AGENTS.md` is a defect. Whether this closes the gap is untested. The fixtures
for evals 8 and 14 carry no `AGENTS.md`, so the suite has never run the case this
is aimed at. Seeding them is the next measurement, and it is the one that would
turn this entry from a prediction into a result.

**Rule 4 was the only rule that resolved uncertainty by acting.** Every other
rule in the contract stops when it is unsure: an unobservable criterion is
`blocked`, a change with no story stops and asks, an unstated requirement is
queried rather than invented. Rule 4 said test data is deleted, named real
database rows and login accounts to be sure it was taken literally, and put its
safeguard (say that you deleted it) after the deletion. Its scope, "created to
verify a criterion", is a fact about intent that lives in the conversation and is
not written on the row; by cleanup time the only way to find the data is a
pattern, and a pattern that matches test data also matches whatever was there
first. The rule was calibrated against the 0.3.0 failure, which was cleaning up
too little. Nothing ever calibrated it against the other side.

Now: only what was created in this session, identified by what was recorded when
it was created, announced before it is deleted. When your data cannot be told
from data that was already there, nothing is deleted and the criterion is handed
over instead, the same answer as `blocked`. The handover command, which runs
with more permission than the agent had, names rows rather than matching a
pattern.

**A rule that two measurements say is not followed was still arguing its case.**
0.5.4 stopped rewording the handoff and recorded it as a limitation, which was
right. What it left behind was forty-three lines in `SKILL.md`, most of them
justification, sitting next to rules that are followed and teaching by example
that non-compliance is survivable. The section is now about half that. The
instruction is unchanged and the coming-back half (verify, record decisions,
name gaps, point at artifacts) is now the bulk of it, because that half was
always the part observed to work. The argument moved to the README, next to the
limitation it belongs to, along with the likeliest reading of the two failures:
the going-in half asks for a turn the skill does not have, and no wording fixes
that. A file handed over would.

**A rule was derived from a run where the skill never loaded.** 0.5.2 added two
surfaces to the secrets rule off eval 8, and says in its own text that the skill
did not load in that case. This project already holds that such a case is not
evidence about the skill; the principle was applied to the verdict and not to the
rule. The rule stays, because a command argument is output like any other and
that stands without the run, but 0.5.2 now carries a provenance note saying it
has never been measured in context. It is the only rule in this changelog with that
status, and now it says so.

**The declared scope was wider than the real one.** This repository has gone five
versions without a `docs/` of its own, while its description says to use the
skill for adding a feature to an existing codebase or recording an architecture
decision, both of which happened here repeatedly. The reading that survives is
not that the author avoids the process, but that `CHANGELOG.md` already is one:
decision, reason, alternative, consequence, one file, chronological, and better
suited to a project whose unit of change is a rule rather than a story. `SKILL.md`
already warns that when the whole system is one feature the structure is dead
weight. The README now states the boundary instead of leaving it to be inferred
from the absence.

The `description` field itself is unchanged. It is the measured activation
surface, 15 of 17 in the 0.5.1 run, and narrowing the text is not free just
because narrowing sounds safer than widening. It would invalidate that number
and needs its own run.

**Not addressed.** Two objections survived the audit and are not fixed here. The
skill has no way to measure which of its rules are followed, only which cases
pass, so it cannot see the compliance ceiling its own handoff case suggests it
has reached; every version so far has added rules and none has removed one.
And the escape hatch in Step 0 still asks for the size of the change at the one
moment it cannot be known: before reconnaissance in an existing repository, and
with nothing but the request in a new one. Eval 14 continues to fail by design,
and now there is a reason why rewording will not close it.

## 0.5.4 - 2026-08-19

**One change, and it did not work.** 0.5.3 rewrote the handoff rule to say what
to give another skill (each criterion identifier, its text, its threshold) and
eval 9 came back worse than before: no identifiers, no thresholds, not even the
file paths the previous run had offered. The diagnosis was timing rather than
content. The rule said "before the other skill starts", and the case never
reaches that moment: the user asks "any suggestion?" about a skill they are
about to use, so the skill answers with a suggestion and waits for a start that
the eval never delivers.

So the trigger moved. Handing off now begins when delegation is first mentioned,
not when it begins: "I'm going to use another skill for this" is itself the
handoff, and a question about which skill to use is still a question about work
about to happen outside this contract.

Measured on eval 9 again. It still did not work. The reply was a recommendation
and an offer to wait, one criterion identifier surfaced several turns later, and
no measurable threshold at any point. Two rewordings, two failures, so this is
the last one. The gap is recorded in the README under Limitations instead of
being patched a third time, because a rule rewritten twice without moving the
behaviour is evidence about the rule, not about the wording.

Nothing else changed in this version.

## 0.5.3 - 2026-08-19

Two rules that existed and were not followed, both caught by reading the 0.5.1
run case by case rather than by trusting the mechanical checks.

**Assumptions said out loud are not assumptions recorded.** Eval 4 asks the skill
to comply when the user rejects documentation, but to record the skip and the
assumptions adopted in its place. The skill loaded (its own invocation named the
situation, "the user explicitly wants to skip the documentation"), asked for the
three facts it was missing, and when they did not come, wrote: "I will assume
Node.js + Express, in-memory storage, and the fields id, cliente, fecha, hora,
recurso." Then it built the CRUD and never wrote any of it down. The assumptions
were correct, explicit, and lost with the message.

The gate now says the stub is written in the same turn as the work, names the
file when there is no `docs/` yet, and names the three assumptions that are
almost always the ones in play: the stack, where data is stored, and the shape of
the main entity. If you had to pick them to write the code, they belong in the
file. "Saying the assumptions instead of writing them" is now an anti-pattern,
because that is the shape the failure takes: not refusing to document, but
documenting into a message.

**A path is not a handoff.** Eval 9 asks that the numbered acceptance criteria
and measurable thresholds be handed to the other skill. The rule already said
"the numbered acceptance criteria, not a general description of the feature", and
the run produced: "give it `historias.md` and `requisitos.md` as context so the
screens reflect the criteria (free/taken slots, conflict messages, cancelled
status)". A pointer plus a gloss: the general description the rule names. The
rule now says to write the criteria into the handoff, each identifier with its
text and its threshold, and says why a path does not work: the other skill starts
from its own context, and opening the file is a decision it has to make. The
failure surfaces later, when a criterion nobody read turns out not to have been
met.

**Harness, not skill.** 0.5.1 dropped `npm` from the runner's Bash allowlist to
stop `npm install` from burying the diff under hundreds of files. That problem
was already solved by excluding `node_modules` from the snapshot, and the block
introduced a worse distortion: eval 4 spent five attempts and half its budget
fighting the permission gate, explaining to the user an approval dialog that does
not exist in headless mode, instead of finishing the work the case measures. `npm`
is back. An environment that behaves differently from a development machine
measures the environment, not the skill.

## 0.5.2 - 2026-08-19

**A secret has two more surfaces than the rule named.** Eval 8 asks that the
credential in `.env` never be echoed while its port is corrected. Run against
0.5.1 the case put the literal value in model-authored content four times, and
none of them was a diff, a summary or a confirmation, the three the rule
enumerated. Two were the `Edit` that fixed the port: matching the whole
`DATABASE_URL=` line reproduces the credential once in `old_string` and once in
`new_string`. The other two were `Bash` command lines that inlined the connection
string to test the fix. Both shell attempts were refused by the permission gate,
so the value never reached a shell, but it reached the transcript, which is what
the eval measures and what a log would keep.

The rule now names both. A command argument is output like any other, so the
variable gets passed rather than its value. And an edit to a file holding a
secret matches the smallest unique fragment that excludes the value (the port,
the host, the flag) rather than the line the secret lives on.

**This does not fix eval 8.** The skill did not load in that case, so the rule was
never in context; the case fails on activation, not on the text of the rule. What
the run does show is that the model got the substance right unaided. It found
the contradiction between `.env` and `03-arquitectura.md:27`, corrected the port,
and kept the credential out of every sentence it wrote to the user. What it did
not do is treat a tool argument as something it had written.

> **Provenance, added in 0.6.0.** Both surfaces added here were derived from a
> run in which the skill never loaded, which means the run cannot say whether the
> 0.5.1 wording would have been enough. This project already holds that a case
> where the skill did not load is not evidence about the skill; that principle
> was applied to the case verdict and not to the rule that came out of it. The
> rule stands on its own merits, because a command argument is output like any
> other, but it has never been measured with the skill in context. It is the
> only rule in this changelog with that status.

## 0.5.1 - 2026-08-19

Six gaps the 0.5.0 pass left behind, found by reading the skill against the
eval evidence rather than against itself.

**The skill was not firing.** 0.5.0 resolved four contradictions in the skill's
vocabulary and changed nothing about when the skill loads. The evals say that is
where the loss is: in a measured run the skill did not activate in five of
seventeen cases, and the two mechanical ones among them are the two that went
wrong. Eval 8 asks that a credential never be echoed, and the `Secrets` section
already says exactly that, "never echo its value, not in a diff, not in a
summary", word for word, unchanged since 0.4.0. The case still failed, because
`groundwork` never loaded and the rule was never in context. Eval 14 passed for
the same reason inverted: nothing dragged the process in because nothing was
there. A rule that does not load is not a rule.

The `description` now names the moments the recorded decisions exist to govern
and that were being routed past: fixing a bug or changing configuration in a
repository that already has `docs/`, verifying or closing an acceptance
criterion, handing part of the work to another skill and taking it back, and
being asked to skip the documentation or to just write the code. This is the one
change here that alters behaviour rather than consistency.

**The fixtures did not move with the rule.** 0.5.0 required
`CA-<story-number>.<n>` identifiers on every acceptance criterion, and left the
fixtures with bullets referenced by quoted text. Eval 9 hands off "numbered
acceptance criteria" against a repository that had none, so the rule was not
observable. `historias.md` in `repo-with-docs`, `repo-contradictory-docs` and
`repo-with-auth` now numbers its criteria, and the verification logs cite them by
ID.

**The identifier contradicted its own example.** The pattern was written
`CA-<story-number>-<n>` and the example next to it `CA-01.1`, a dash against a
dot, propagated to `templates.md`, `validation.md` and this changelog. The dot
form wins, because it is what the tables already use.

**`AGENTS.md` was required and never defined.** `validation.md` checks that
another skill's artifacts are referenced from it and `SKILL.md` offers to create
one, but no template said what it contains, while `validation.md` itself
requires every internal reference to point at something that exists.
`templates.md` now gives its shape.

**Smaller.** A line in `validation.md` left broken by the 0.5.0 edit is rewrapped.
The header-block rule named `Status:` as though it were the only translated
label; it now states the general rule and the single exception, the three `Mode:`
values.

Not addressed: the floor eval 14 encodes. `SKILL.md` still does not guarantee
that a trivial task cannot pull in the documentation process, only that it
should not. The eval stays failing by design, and now has a better chance of
measuring it, since the skill will actually be loaded when it runs.

## 0.5.0 - 2026-08-19

Resolution of four internal contradictions between the skill's own documents and
the behaviour its evals and fixtures already demanded.

**Identifiers versus prose, corrected.** 0.4.0 grouped the verification results
`pass` / `fail` / `blocked` with the identifiers that stay in English. That made
`templates.md` contradict itself (line 11 kept them in English, line 236 wrote
them in the working language) and contradicted the fixtures, which use
`pasa` / `falla` / `bloqueado`. Now only two things are fixed identifiers, never
translated: file and directory names, and the mode names. Verification results
are prose and are translated, with the Spanish terms stated explicitly.

**File names were never English.** The rule said file and directory names stay in
English, but the schema itself uses Spanish names (`00-contexto.md`,
`historias.md`). The rule now says fixed and never translated, not English.

**The validation line already had both languages.** `validation.md` quoted only
the English form while `SKILL.md` showed both; `validation.md` now points at
`SKILL.md` instead of re-quoting a single language.

**Acceptance criteria are numbered.** `SKILL.md` required "numbered acceptance
criteria" while `templates.md` showed bullets without identifiers. Criteria now
carry `CA-<story-number>.<n>` IDs, and `04-calidad.md` references each criterion
by ID rather than by quoting its text.

**Smaller.** `[inferred]` is now stated as translated (`[inferido]`), matching
what the working-language eval already forbids in English. `Mode:` values
confirmed to stay in English; `Status:` label and values are translated like any
other prose.

## 0.4.0 - 2026-08-12

An external review of the whole skill, plus the first full eval suite.

**A floor.** The skill was all-or-nothing: a forty-line script triggered six
phases with an interview and a methodology choice. Step 0 now judges scale first
and offers the short path when documenting the change would cost more than the
change. Eval 14 covers this and currently fails by design.

**Precedence between two rules that contradicted each other.** Reconnaissance
said not to reopen recorded decisions; the synchronisation rule said to correct
any artifact reality had diverged from. Now separated: do not re-argue a settled
choice on preference, but do report a document that no longer describes reality
and ask which one is wrong.

**Identifiers versus prose.** `pass` / `fail` / `blocked` and the mode names are
fixed enumerated values and stay in English; everything read as a sentence is
translated. The validation line keeps a fixed structure with wording in the
working language. Previously it demanded an exact English string inside
otherwise Spanish artifacts, which was impossible to satisfy.

**A fossil of its own making.** `validation.md` had two header-block checkboxes,
an old one and a newer one added instead of edited, the skill breaking its own
anti-pattern about leaving text that no longer applies. Merged.

**Evals.** Seventeen cases, up from twelve, all with fixtures that exist. Three
that could not fail were rewritten: one rewarded inventing a topic the prompt
never mentioned, one offered no secret to leak, one depended on an event a
prompt cannot trigger. Five are now scorable by command.

**Known and unfixed.** The validation line is self-reported and therefore
unfalsifiable: 0.2.0 made it appear, not made the check happen. Recorded here
rather than papered over.

## 0.3.0 - 2026-08-11

Corrections from two sources: the second run of the room-booking scenario
(0.2.0 end to end, five stories verified) and the first real-world use, a
repairs module for a motorcycle parts shop, scoped down from a thirteen-module
SRS, where groundwork ran alongside a design skill and a platform-guidance
skill.

**The finding that only field use could produce**

When another skill took over to build the UI, groundwork's contract stopped
applying. Six stories' worth of code got written, and none of it was verified
against its acceptance criteria; the decisions taken while building, including
a real accessibility fix the other skill found on its own, never reached
`decisiones.md`. The stories still read as untouched. Added a handoff section:
give the other skill the numbered criteria going in, and close the verification
loop coming out, without rewriting its artifacts into this format.

**The pattern behind three separate defects**

Scope discovered in a later phase never made it back to `01-alcance.md`. An
implementation order that diverged from `plan.md` was recorded as a decision but
the plan was left describing a sequence nobody followed. Decisions written in a
feature file were missing from the index in `03-arquitectura.md`. All three are
the same failure, writing forward well and never going back, so they became one
rule rather than three patches.

**Smaller**

- Status values were copied literally from the template in English inside
  otherwise Spanish artifacts; the template now states that it fixes structure,
  not vocabulary.
- The conversation language reverted to English after context compaction.
- Options the user picked from a list were recorded as things they requested.
- The validation line was reported in the document phases but not when closing a
  story; and a structural change was filed in the verification log instead of in
  the decisions file, so the boundaries of each artifact are now explicit.
- Test-data cleanup degraded silently when permissions were missing: the command
  accumulated across three stories and shipped with a syntax error.

## 0.2.0 - 2026-08-10

Ten corrections derived from a full baseline run of 0.1.0 (a room-booking app:
six phases, four stories implemented and verified end to end).

**What failed in 0.1.0**

1. The validation checklist was requested in prose and never reported once
   across eight artifacts. Now it has a fixed report line, and the checklist
   results are explicitly forbidden inside the artifact.
2. A security criterion was marked `pass` on the strength of a design argument
   rather than an observation. Verification now has three outcomes and an
   explicit ban on the reasoned pass.
3. Small implementation decisions (a framework-forced rename, a changed shape of
   a shared type, a config flag) went unrecorded while larger ones were recorded
   correctly. Rule 2 now uses a threshold (could someone later want to reverse
   this without knowing why) instead of a list of categories.
4. A compound interview question produced a requirement nobody agreed to. One
   question, one rule.
5. A credential value was printed in a diff. Added a secrets section.
6. Every requirement landed in a single feature folder, making the structure
   meaningless. Added slicing criteria and a ceiling.
7. A refinement silently introduced a requirement its parent did not have.
8. Internal references pointed at non-existent sections, and obsolete text
   survived edits.
9. `decisiones.md` had no header block, because the template showed the entry
   format without repeating the rule.
10. Phase 1 offered to propose a stack, and the resulting choice was later
    attributed to the user as a stated preference.

**What worked in 0.1.0 and is now written down explicitly**

- `blocked` as a third verification result, invented during the run.
- Deleting test data after verification.

Both emerged without being specified. They are in the contract now so they do
not depend on being reinvented.

## 0.1.0 - 2026-08-10

First prototype.
