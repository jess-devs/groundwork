# Choosing a methodology

The point is not to pick the fashionable framework. It is to pick one whose
ceremonies are actually affordable for this team and this project, and to write
down why, so the choice survives the first inconvenient sprint.

Most small projects are over-ceremonied. A solo developer running formal sprint
planning, review and retrospective with themselves is performing a ritual, not
managing risk. Say so plainly if that is the situation.

## Decide on these factors

Ask or infer, in this order. The first two usually settle it.

1. **Team size.** One person, or more than one?
2. **Requirement stability.** Are the requirements likely to change while the
   work is in progress, or are they effectively fixed?
3. **Cadence.** Does work arrive in batches that can be committed to for a
   period, or does it arrive continuously and unpredictably?
4. **External accountability.** Is there a client, a supervisor or a grader who
   expects specific ceremonies and artifacts?
5. **Duration.** Days, weeks, or months?

## Selection

**Kanban.** Continuous flow, work-in-progress limits, no fixed iterations.
Choose it for solo work, for maintenance, for support-driven work, and whenever
requests arrive unpredictably. It is the correct default for a single developer,
and the one most often wrongly passed over in favour of Scrum.

**Scrum.** Fixed iterations, defined roles, planning and review per iteration.
Choose it for a team of roughly three or more, with requirements that will
change, and someone available to act as product owner. Its overhead only pays
for itself when several people need synchronising. If nobody can genuinely fill
the product owner role, do not pretend: record that and adapt.

**XP practices.** Pair programming, test-first, continuous integration, small
releases. These are engineering practices, not a project framework, and can be
layered on top of either of the above. Choose them when the code has to change
frequently and safely. Test-first in particular pays for itself when acceptance
criteria are already written, which is the case here.

**No framework, artifacts only.** The documents in `docs/`, no ceremonies.
Choose it for short solo work, spikes, and prototypes. This is a legitimate
answer and should be offered when the alternative would be theatre.

**Hybrid.** Usually Kanban flow with a subset of Scrum artifacts. Common when
someone external expects a backlog and demos but the team is too small for
sprints. Record explicitly which pieces are adopted and which are dropped.

## Recording the choice

Write the choice into `00-contexto.md` with three things: the name, the reason
tied to the factors above, and the consequences. Example shape:

> Chosen: Kanban with a WIP limit of two.
> Reason: solo developer, requests arrive unpredictably from users, no fixed
> delivery date. Sprint ceremonies would have no counterpart to synchronise.
> Consequences: no iteration commitment, so progress is tracked by cycle time
> per story rather than by velocity. Stories must be small enough to finish
> within a few days.

The consequences line is the one that matters later. It is what tells a future
session which reporting and planning behaviour is appropriate.

## When to revisit

A methodology is a decision like any other, and belongs in `decisiones.md` if it
changes. Revisit it when the team size changes, when the work changes character
from building to maintaining, or when the ceremonies are being skipped in
practice. Ceremonies that are consistently skipped are evidence the choice was
wrong, not evidence of indiscipline.
