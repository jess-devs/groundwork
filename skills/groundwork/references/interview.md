# Interview

The purpose is to extract what only the user knows. Do not ask about anything
already answered in the conversation or already written in `docs/`. That is the
fastest way to make the process feel like paperwork.

## How to ask

Ask in small batches, three to five questions at a time, grouped by theme. A
wall of twenty questions gets a wall of thin answers.

**One question, one rule.** Never join two rules in a single question, even when
they share a shape. "Is there a minimum notice for booking or for cancelling?"
gets one answer and produces two rules, only one of which the user meant, and
the wrong one ends up in the requirements looking exactly as legitimate as the
right one. Ask separately even when it feels repetitive: the extra click is
cheap, the conflated requirement is not. The same applies to "and/or" in any
follow-up.

Propose a default answer whenever you can reasonably infer one, and ask the user
to correct it rather than to produce it from nothing. "I assume this is for
internal use and not public sign-up, correct?" gets a better answer than "who
are the users?".

Stop asking when the remaining unknowns can be recorded as assumptions without
changing the shape of the work. Perfect information is not the goal; recorded
uncertainty is.

## Phase 1: new project

**Problem.** What is happening today that made this worth building? Who feels
that pain? What do they do about it now?

**Users.** Who uses it, and in what role? Is there more than one kind of user
with different permissions or different goals?

**Boundaries.** What is explicitly not part of this? What might someone
reasonably expect it to do that it will not do?

**Constraints.** Is there a deadline? Is a stack already decided, and why?
Anything it must integrate with? Any regulation, privacy or data-residency rule
that applies?

Ask only whether a stack is _already_ decided. Do not offer to propose one and
do not mark proposing as recommended. That is Phase 4 work, and an answer given
here gets recorded as a preference the user never expressed. If nothing is
decided, write "not decided, resolved in Phase 4" and move on.

**Scale and quality.** How many users, roughly? What happens if it is down for
an hour? What data in it would hurt if leaked? Who is allowed to see it, and who
is not? Ask for numbers; if the user has none, record "no stated target" rather
than choosing one.

**Team.** Solo or with others? If others, how is work divided, and is there a
review step?

**Done.** How will you know this was worth building? What has to be true for you
to call the first version finished?

## Phase 3: new feature on an existing system

Ask these only after reconnaissance, and lead with your summary of the codebase
so the user is correcting rather than explaining.

**Fit.** What part of the current system does this touch? Is there an existing
flow it extends, or is it genuinely new territory?

**Trigger.** Why now? A user complaint, a business need, a technical debt
payment? The reason usually reveals the real acceptance criteria.

**Compatibility.** Does this change existing behaviour anyone depends on? Is
there data already stored that needs migrating?

**Boundaries.** What is the smallest version of this that would be worth
shipping? Anything adjacent that is tempting but out of scope?

**Constraints.** Does it have to follow the conventions already in the codebase,
or is this an opportunity to change them? If the latter, that is an architecture
decision and needs recording.

## Phase 4: architecture

Ask only what the code and the requirements cannot answer:

- Is there an existing pattern in this codebase you want followed, or one you
  want moved away from?
- Are there dependencies you will not accept for licence, size or maintenance
  risk?
- Is anything here expected to be replaced or extracted later? Anticipated
  change is the main reason to draw a boundary.

## Recording the answers

Distinguish what the user stated from what they picked off a list you wrote.
Both are valid inputs, but only the first is a constraint of theirs; the second
is your proposal that they did not reject. Write it as such, "chose among the
alternatives offered", so that a reader months later does not mistake a default
for a requirement.

## What not to ask

- Anything answerable by reading the repository. Read it.
- Preferences that do not change the artifact. Do not ask about tone, colour or
  naming style when writing requirements.
- The same question in different words to confirm an answer already given. It
  reads as not having listened.
