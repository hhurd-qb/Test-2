<!-- Synced from Confluence page 6401425413: work-day-sprint-planner -->

---

## name: work-day-sprint-planner description: >- Plan a sprint for the user's team: pull the current sprint, backlog, and last sprint's carryover, take the user's sprint goals, recommend ticket assignments and scope across the board's members, recommend which backlog items to pull in (and, on request, move them into the active / next / a specified sprint), and flag work discussed in Slack/meetings that has no Jira ticket yet (optionally creating those tickets). Use for sprint planning, sprint kickoff, capacity or scope planning, and backlog grooming. All writes are confirmed. Requires the Atlassian connector; Slack and Microsoft 365 improve untracked-work detection.

# Work-Day Sprint Planner

Help the user plan a sprint for their team: assess goals, recommend a balanced  
ticket distribution, flag scope risk, and surface work that's happening but isn't  
ticketed yet.

Read <references/jira-rules.md> first (query-size  
discipline, field ids, write safety).

## Config & identity

Reuse `work-day-config` from memory. The key field for planning is  
`sprint_board` — the board to plan, since sprints belong to boards. It holds:  
`name`, `project` (the board's project key — or `projects` if the board spans  
several), and optional `sprint_name_prefix` (the board's sprint-naming prefix,  
e.g. "SMIT", used to disambiguate when a project has more than one board). If  
it's missing, ask the user which board/project to plan and save it.

**Members are not a fixed roster** — derive them from the **distinct assignees**  
on the board's sprint / backlog / carryover tickets. Plan across EVERYONE who has  
work in the space, not just the user or their direct reports. (A teammate with  
zero current tickets won't appear — that's an accepted limitation of deriving  
members from tickets.)

## Step 1 — Gather the BOARD's sprint state (all assignees)

The Atlassian connector has **no board/sprint API**, so scope a board via JQL by  
its project (+ optional sprint-name prefix). Pull tickets for the WHOLE space —  
every assignee AND unassigned — never filter by a person:

* **Active sprint**: `project = <board project> AND sprint in openSprints() ORDER BY assignee`. If the project has multiple boards, keep only issues whose  
  **Sprint field name starts with** `sprint_name_prefix` (filter the results;  
  the Sprint name is in each issue).
* **Carryover**: `project = <project> AND sprint in closedSprints() AND statusCategory != Done` — the board's most recent closed sprint.
* **Backlog**: `project = <project> AND sprint is EMPTY AND statusCategory != Done ORDER BY Rank ASC` — the top-ranked candidates. Pull a couple of pages so  
  there's a real menu to choose from (still `maxResults` ~8 per page).

Mind the size rules ([jira-rules.md](http://jira-rules.md)): `maxResults` ~8, **paginate** to cover all  
assignees, never request `parent` in bulk. The distinct assignees across these  
results are your **members** for the rest of the plan.

## Step 2 — Sprint goals

Use goals the user provides. If none given, ask for them (or infer 2–3 candidate  
goals from the active sprint's epics and say you're inferring).

## Step 3 — Recommend assignments & scope

Produce a plan:

* **Goal assessment** — for each goal, do tickets map to it? Sized right? Risk?
* **Carryover decisions** — for each unfinished ticket: carry / descope / split /  
  reassign, with a one-line why. Carried-over work consumes capacity first.
* **Recommended backlog pulls** (the core recommendation) — propose the specific  
  backlog tickets to bring INTO the sprint. Work out remaining capacity =  
  team capacity − carried-over load, then pick the **highest-rank backlog items**  
  **that (a) advance the stated goals and (b) fit that remaining capacity**.  
  Present as a ranked table:  
  `| Pull? | Ticket | Summary | Goal it serves | Size | Suggested assignee | Why |`  
  Mark each **Pull / Hold / Stretch** (stretch = include only if capacity frees  
  up). Show the running total against capacity so the cutline is visible, and  
  briefly say what was left out and why.
* **Proposed sprint composition** — the resulting sprint = carryover kept +  
  backlog pulls, with the per-member load and the total vs. capacity.
* **Scope risks** — tickets too large, vague, or missing acceptance criteria  
  (flag these BEFORE recommending a pull; don't pull an unestimable ticket).
* **Capacity check** — rough capacity vs. proposed load; a Go / Caution / Stop call.

This step **recommends**; moving the tickets is Step 6 (only on request, with  
confirmation).

## Step 4 — Flag work without a ticket

Cross-reference recent **Slack, Teams, and email** against existing Jira issues:  
work that's clearly planned or in progress (commitments, "I'll build…", decisions)  
but has **no ticket**. Search by **topic and by people** — the space's members  
from Step 1 — not just ticket keys. For each gap: a one-line description, a suggested ticket  
(project/summary/type/priority/assignee), and the source you inferred it from.

## Step 5 — Optionally create the missing tickets

Only if the user says yes. Create them with `createJiraIssue`, **confirming each**  
**payload first**, and report the new keys. Never bulk-create without confirmation.

## Step 6 — Optionally move the approved pulls into a sprint

Only on request. First ask which **target sprint** (or use what the user already  
said), and resolve its **id** — moving an issue means setting its Sprint field  
(`customfield_10017`) to a sprint id, and the connector has no Agile/board API,  
so ids must come from issues already in the sprint:

* **Active sprint** — use the active sprint's id; you already have it from the  
  Step 1 active-sprint tickets' Sprint field. (No extra lookup.)
* **Next / future sprint** — search `project = <project> AND sprint in futureSprints()` (board-prefix filtered) and take the earliest-starting future  
  sprint's id. If no future sprint has any issues yet, its id isn't discoverable  
  via search — ask the user for the sprint id/name (or to seed/start it in Jira).
* **A sprint the user names** — an id is used directly; a name is resolved by  
  searching `sprint = "<name>"` and reading the id off a returned issue. If the  
  named sprint is empty, ask for its id.

Then **confirm the final ticket list + the resolved target sprint (name + id)**,  
and for each approved ticket call `editJiraIssue` setting `customfield_10017` to  
that id. Report each result.

If a Sprint-field write is rejected (some boards lock it from the issue-edit  
path), say so and tell the user to drag the tickets in Jira — there's no Agile  
"move to sprint" endpoint to fall back on. Never move tickets without confirmation.

## Conventions

* **Tone follows the user** — match their own Claude configuration.
* Honor display-name preferences (e.g. "Kautilya", never "Kumar").
* Don't fabricate tickets, capacity, or PTO — if a source is unavailable, say so.
