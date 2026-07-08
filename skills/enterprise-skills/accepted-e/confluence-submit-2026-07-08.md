<!-- Synced from Confluence page 6429900841: confluence-submit 2026-07-08 -->

---

## name: confluence-submit description: > Trigger this skill whenever the user says "/submit" — with or without anything else in the message. This skill first checks the IAS space for duplicate or overlapping skills, then audits the skill with a built-in five-factor rubric, works with the user to optimize it based on that audit, asks whether to file it as Enterprise or Team, checks the chosen filing location fits, then publishes it as a new child page in the Internal AI Skills Confluence space (IAS) — under the Enterprise page or the chosen Team subpage (e.g. Biz Ops, Sales, Marketing) — with a companion audit-summary child page showing the skill's strengths and gaps. Every published title includes the submission date. Use this skill immediately when "/submit" appears anywhere in the message. Confirmation is required for any duplicate/overlap found, the optimization pass, and the Enterprise/Team and subpage choices, but not for publishing itself once those choices are made.

# /submit — Publish Skill to Confluence

When the user says `/submit`, screen the skill for duplicates first, audit it, optimize it  
together with the user, ask where it should be filed, double-check that placement, then publish  
it to Confluence under the right page with a dated title.

---

## Step 1: Identify the Skill Content

Look at the current conversation to find the skill. It will be one of:

**A) Pasted content or uploaded file** — the user has shared raw text directly in the chat or uploaded a file. Use that.

**B) A named skill on disk** — the user has referred to a skill by name (e.g. "the cloud vowel counter skill"). Find it under:

* `/mnt/skills/user/[skill-name]/SKILL.md`
* `/mnt/skills/public/[skill-name]/SKILL.md`

Read the file with the `view` tool to get the full content.

**C) A skill just created this session** — a `SKILL.md` was written to `/home/claude/` during this conversation. Use that content.

If it's ambiguous which skill the user means, check the most recent skill mentioned or worked on in the conversation. Only ask for clarification if there are genuinely multiple candidates and no clear most-recent one.

**Check for supplementary content.** Skills often ship with more than just `SKILL.md` — reference files, scripts, templates, examples, etc., typically in a subfolder like `references/`, `scripts/`, or `assets/` next to the `SKILL.md`. List the skill's directory (`view` the folder containing `SKILL.md`) and note every other file found. These will be published as child pages in Step 11 — always, with no need to ask the user first.

---

## Step 2: Extract the Skill Name

Parse the YAML frontmatter at the top of the skill file to get the `name` field. This will form the basis of the Confluence page title (see Step 9 for the dated format).

yaml---
name: my-skill-name ← use this as the base title
description: ...
---

If no `name` field exists, use the filename (minus `.md`) as the base title.

---

## Step 3: Check for Duplicate or Overlapping Skills

Do this before the full audit in Step 4. Auditing is the most token-expensive part of this  
workflow, and there's no point running the full rubric against a skill that's about to be  
merged, rescoped, or rejected as a near-duplicate. Screen for overlap first, while the skill is  
still cheap to redirect.

The goal isn't to block similar-sounding skills — it's to prevent two skills from doing the same  
job with only cosmetic differences, which fragments the library and confuses whoever's picking a  
skill to use.

**3a. Find candidates.** Call `getPagesInConfluenceSpace` (cloudId `20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`, spaceId `6386384916`) to list titles across the whole space — not just a likely destination page, since an overlapping skill could live anywhere (Enterprise or any Team subpage). Also run `searchConfluenceUsingCql` with a couple of keyword variants pulled from the skill's core task (not just its literal name — two skills solving the same problem often have different names). Skip structural pages (space homepage, "Enterprise Skills," "Team Skills," topic subpages like "Sales") — you're looking for actual skill pages.

**3b. Compare on substance, not surface.** For any candidate whose title or summary looks plausibly related, fetch it with `getConfluencePage` and compare against the skill being submitted on:

* **Core task** — what job does each actually do when triggered?
* **Trigger conditions** — do their descriptions fire on the same or heavily overlapping requests?
* **Scope/output** — do they produce the same kind of result for the same audience?

Two skills can share a general theme (e.g. both touch "sales") without being duplicates — that's only a conflict if they'd both fire on the same request and do essentially the same thing once triggered.

Hold onto the webui link from each `getConfluencePage` response for any candidate you flag — it's needed in Step 3c so the user can pull up the existing page directly.

**3c. Judge and act.**

* **No meaningful overlap:** State briefly that no overlapping skill was found, and continue to Step 4.
* **Clear duplicate or near-duplicate** (same core task, same triggers, only superficial differences in wording/format): Do not proceed to the audit yet. Tell the user plainly which existing skill(s) overlap and why, **including a link to each overlapping page** so they can review it themselves, and recommend a path — merge the two, narrow one skill's scope so each has a distinct, non-overlapping use case, or revise the trigger conditions to stop them from colliding. Ask the user how they want to proceed (revise and resubmit, continue to audit anyway, or cancel) before taking any further action.
* **Partial or ambiguous overlap:** Name the related skill(s) **with a link to each**, describe the overlap concisely, and ask the user to confirm whether to proceed to the audit as-is or revise first. Don't guess on their behalf.

Keep this report to a few sentences; this isn't a full audit.

---

## Step 4: Quality Audit

Audit the skill identified in Step 1 using the full rubric below. Produce the complete audit report and show it to the user — this is the quality verdict, independent of where the skill will be filed.

Do not skip or abbreviate this step even if the skill looks similar to one audited previously in this conversation; always run the full rubric fresh.

### 4a. Pre-flight Checks

Before classifying, check for these common failure modes:

**No frontmatter:** If the skill has no YAML frontmatter (no `name` or `description` field), it cannot trigger and will automatically score 1/10 on Triggering Precision regardless of other quality. Flag this immediately at the top of the report.

**Ambiguous classification:** If the skill could plausibly be Team or Enterprise, default to Team and note the ambiguity explicitly in the report. Explain what would need to change for it to qualify as Enterprise. Do not upgrade a skill's classification based on quality — only on scope of usefulness.

**Shared as context:** If the user explicitly indicates the skill is being shared for reference rather than evaluation (e.g. "just use this", "don't audit this", "use this as context"), do not audit. Acknowledge the skill and proceed with whatever the user actually asked for. A silent file drop with no instructions is not a context share — treat it as an audit request. (Note: under `/submit`, a skill being explicitly submitted is always an audit request — this exception mainly matters if the skill arrives ambiguously alongside other asks.)

### 4b. Classify the Skill

**Individual** — Personal or fun, no direct working value. Improves daily life or is creative but brings no benefit to team workflows or the org. Examples: vowel counters, journaling assistants, habit trackers.

**Team** — Useful for a specific team's workflow or productivity. Encodes domain-specific knowledge, automates a team process, or improves consistency within a group. Examples: Jira query rules for engineering, a brand voice guide for marketing, a sales call prep checklist.

**Enterprise** — Broadly useful across the entire org regardless of team or role. Encodes company-wide standards, policies, or processes everyone would benefit from. Examples: company branding requirements, onboarding workflows, compliance checklists, universal writing standards.

**Upgrade check (Team skills only):** After scoring, if a Team skill scores 9–10 on Value Add, add an upgrade note to the report flagging it as a candidate for enterprise-wide rewrite. Do this as a final step — do not reclassify based on score.

Note: this classification is informative only — per Step 6, the user always makes the actual Enterprise/Team filing decision regardless of what's concluded here.

### 4c. Apply the Right Framework

**If INDIVIDUAL → No Scoring**

## Skill Audit Report: [Skill Name]
\*\*Category: Individual\*\*
This skill has been classified as personal/individual. It will not be scored or committed to the company skill library.
\*\*Reason:\*\* [1–2 sentences explaining why.]
\*\*Recommendation:\*\* May be useful as a personal install but is not appropriate for shared company use.

**If TEAM or ENTERPRISE → Score Using the Rubric Below**

Score each factor 1–10. Apply the threshold column that matches the skill's category — ignore the other.

**Factor 1: Instruction Engineering** — *Are the instructions well-crafted, internally consistent, and actionable?*

| Score | Criteria |
| --- | --- |
| 9–10 | Precise, unambiguous, structured. Edge cases handled. Claude would know exactly what to do at every stage with no guesswork. |
| 7–8 | Mostly clear with minor gaps a capable reader could fill. |
| 5–6 | Some vagueness, but core intent is decipherable. |
| 3–4 | Contradictory, confusing, or leaves major gaps. |
| 1–2 | Barely coherent or entirely undefined. |

**Factor 2: Conciseness** — *Is the skill as short as it needs to be — and no shorter?*

| Score | Criteria |
| --- | --- |
| 9–10 | Every sentence earns its place. Dense but readable. No redundancy. |
| 7–8 | Mostly tight. A sentence or two could be cut. |
| 5–6 | Noticeable padding or repeated content, but core is navigable. |
| 3–4 | Significantly bloated or redundant. |
| 1–2 | Extremely verbose or critically terse. |

**Factor 3: Value Add** — *Does this skill meaningfully improve a workflow that Claude couldn't handle well alone?*

| Score | Criteria |
| --- | --- |
| 9–10 | Encodes non-obvious knowledge Claude couldn't reliably replicate alone. Clear ROI. |
| 7–8 | Adds real value — improves consistency or quality in context. |
| 5–6 | Marginal value. Claude could mostly handle this natively. |
| 3–4 | Replicates something Claude already does well. Little added value. |
| 1–2 | No value, or counterproductive. |

**Factor 4: Appropriate Complexity** — *Is the complexity level right for the job?*

| Score | Criteria |
| --- | --- |
| 9–10 | Complexity matches the task perfectly. Nothing superfluous, nothing missing. |
| 7–8 | Slight mismatch but not harmful. |
| 5–6 | Noticeably over- or under-engineered. |
| 3–4 | Major mismatch. |
| 1–2 | Completely inappropriate complexity. |

**Factor 5: Triggering Precision** — *Will this trigger when needed — and only then?*

| Score | Criteria |
| --- | --- |
| 9–10 | Covers formal and informal phrasings. Explicit "when NOT to use" clause. Handles edge cases like silent file drops and context-only shares. No false-positive risk. |
| 7–8 | Good coverage. Minor over/under-trigger risk. |
| 5–6 | Vague or generic. May miss edge cases or misfire. |
| 3–4 | Too broad or too narrow. |
| 1–2 | Absent, nonsensical, or wrong. |

**Pass Thresholds**

| Factor | Team | Enterprise |
| --- | --- | --- |
| Instruction Engineering | ≥ 5 | ≥ 7 |
| Conciseness | ≥ 5 | ≥ 6 |
| Value Add | ≥ 6 | ≥ 7 |
| Appropriate Complexity | ≥ 5 | ≥ 6 |
| Triggering Precision | ≥ 5 | ≥ 7 |
| **Total** | **≥ 32/50** | **≥ 38/50** |

A skill fails if any single factor is below its category threshold — even if the total passes.

### Report Format

Adapt the threshold column to the skill's category. Do not show both columns.

## Skill Audit Report: [Skill Name]
\*\*Category: [Team / Enterprise]\*\*
[If no frontmatter detected: ⚠️ No YAML frontmatter found. Triggering Precision capped at 1/10.]
### Scores
| Factor | Score | Threshold | Status |
|-------------------------|-------|-----------|--------|
| Instruction Engineering | X/10 | ≥ [5/7] | ✅/❌ |
| Conciseness | X/10 | ≥ [5/6] | ✅/❌ |
| Value Add | X/10 | ≥ [6/7] | ✅/❌ |
| Appropriate Complexity | X/10 | ≥ [5/6] | ✅/❌ |
| Triggering Precision | X/10 | ≥ [5/7] | ✅/❌ |
| \*\*TOTAL\*\* | XX/50 | ≥ [32/38] | ✅/❌ |
### Verdict: ✅ APPROVED FOR [TEAM USE / ENTERPRISE] / ❌ NOT APPROVED
[If classification was ambiguous: ⚠️ Classification note: this skill could be Team or Enterprise. Defaulted to [X]. For Enterprise classification, it would need to [specific change].]
[If a single factor caused failure: ❌ Failed on [Factor Name] alone — total score is not sufficient to override a single-factor failure.]
[If Team skill scores 9–10 on Value Add: ⬆️ Upgrade candidate: this skill's value add score suggests it may be worth rewriting for enterprise-wide deployment.]
---
### Factor-by-Factor Feedback
[2–4 sentences per factor. Cite by quoting the exact phrase or naming the section header (e.g., "The line 'cite specific lines' in the report template…" or "The Factor 3 rubric…"). Be direct — this is quality control, not encouragement.]
### Top Recommendations
- [Most impactful fix — specific and actionable]
- [Second most impactful]
- [Third, if applicable]

### Core Rules

* Classify by scope, not quality. A well-written Team skill is still a Team skill. Only promote to Enterprise if the use case is genuinely org-wide.
* Single factor failure = full rejection. A skill that fails any one factor is rejected even if the total passes. State the failing factor explicitly in the verdict.
* Recommendations must be actionable. "Improve the instructions" is bad. "Split step 3 into two steps and define the output format explicitly" is good.
* Do not inflate scores. A 47/50 should be rare. Most real-world skills have real flaws — find them.

---

## Step 5: Optimize the Skill with the User

Before moving on to filing, walk the user through the Step 4 findings and work together to  
improve the skill. This is a collaborative editing pass, not a rubber stamp.

* Start from the **Top Recommendations** and any factor that scored low or failed its threshold. Present them concisely and propose concrete edits (tightened instructions, a narrower trigger description, a trimmed section, a missing edge case handled, etc.).
* Make the edits the user agrees to directly in the skill content, and treat the result as the new working copy for every step that follows (audit summary, publishing, etc.).
* This can take more than one round — keep iterating until the user is satisfied or explicitly says to move on.
* If the user wants to publish as-is with no changes, that's fine — acknowledge it and proceed to Step 6.
* If the edits made are substantive enough that the Step 4 scores no longer reflect the skill (e.g. a failing factor was directly addressed), re-run the Step 4 rubric on the revised version so the score carried into the audit summary (Step 10) is accurate. Minor wording tweaks don't need a rescore — use judgment on materiality.

---

## Step 6: Ask Enterprise or Team

Regardless of what the audit in Step 4 concluded (even if it classified the skill as Individual, or strongly reads as Enterprise- or Team-scoped), always explicitly ask the user whether this skill should be filed as Enterprise or Team. The auditor's classification is informative context to mention, but the filing decision is the user's call, not automatic.

---

## Step 7: Resolve the Filing Location

**If Enterprise:**

The skill is filed directly under the Enterprise page. Look up the Enterprise page dynamically (see "Locating filing pages" below) — do not assume a fixed page ID. Skip to Step 8.

**If Team:**

Team skills live under topic subpages (e.g. Biz Ops, Sales, Marketing) nested under the Team page. Look up the Team page dynamically, then call `getConfluencePageDescendants` on it to list its current subpages. Present the available subpages to the user and ask which one this skill should go under. If none of the existing subpages fit, ask the user whether to create a new one (name it per their answer) before proceeding — don't create it silently.

**Locating filing pages:**

Call `getPagesInConfluenceSpace` (cloudId `20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`, spaceId `6386384916`) or `getConfluencePageDescendants` on the space homepage (`pageId: 6386385580`) to find the current Enterprise page and Team page by title — do not hardcode their page IDs, since the filing structure can change. If either top-level page (Enterprise or Team) can't be found, tell the user and ask how to proceed rather than guessing.

---

## Step 8: Placement Check

Once a specific destination is set (the Enterprise page, or a specific Team subpage like Biz Ops/Sales/Marketing), run a second, different check — not a re-score of quality. This is a content-fit check: does this skill's subject matter actually belong on the chosen page?

* **For Enterprise:** confirm the skill is genuinely org-wide in relevance (consistent with why it's being filed at the top Enterprise level, not under a specific team).
* **For Team subpages:** judge whether the skill's actual content matches the chosen subpage's domain (e.g. a Jira sprint-planning skill fits an Engineering or Biz Ops subpage, not Marketing).

If it's a clear mismatch, say so plainly and recommend the better-fitting subpage, but let the user make the final call before publishing.

Report this placement verdict to the user concisely (a sentence or two is enough) before moving to publish.

---

## Step 9: Publish the Skill as a Child Page

Use the Atlassian MCP to create the page with these values:

* **Cloud ID:** `20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`
* **Space ID:** `6386384916` (Internal AI Skills / IAS)
* **Parent page ID:** the Enterprise page (Enterprise filing) or the chosen Team subpage (Team filing), resolved in Step 7
* **Title:** `[skill name] [YYYY-MM-DD]` — the skill's name from frontmatter followed by today's date. Every published title includes the date, regardless of whether a same-named page already exists.
* **Content format:** `markdown`
* **Body:** the full raw `SKILL.md` content (the optimized version from Step 5, if changes were made), exactly as written — no summarizing, no paraphrasing, no abbreviating

Call `createConfluencePage` with these parameters.

---

## Step 10: Publish an Audit Summary as a Child Page

Always create this — no need to ask the user first. Its purpose is narrow: give someone reviewing the skill later (including via the GitHub sync, where this becomes a plain file sitting next to the skill) a fast, scannable view of where the skill is strong and where it falls short, without having to re-read the full Step 4 report.

Use the scores and feedback already produced in Step 4 (or the rescored version from Step 5, if one was run) — do not re-run or re-score the audit here. Condense it down to:

* **Where it's strong:** the 1–2 highest-scoring factors, one sentence each, drawn from the Step 4 feedback.
* **Where it falls short:** the 1–2 lowest-scoring factors (or any that failed their threshold), one sentence each, drawn from the Step 4 feedback. If every factor passed comfortably, note the weakest-but-passing factor instead so there's always something concrete for a reviewer to check.
* **Recommendations:** carry over the Top Recommendations from Step 4, verbatim or lightly condensed — noting any that were already addressed during the Step 5 optimization pass.

Format:

# Audit Summary: [Skill Name]
\*\*Category:\*\* [Team/Enterprise] · \*\*Verdict:\*\* [✅ APPROVED / ❌ NOT APPROVED] · \*\*Score:\*\* XX/50 · \*\*Submitted:\*\* YYYY-MM-DD
## Scores at a Glance
| Factor | Score | Status |
|--------|-------|--------|
| Instruction Engineering | X/10 | ✅/❌ |
| Conciseness | X/10 | ✅/❌ |
| Value Add | X/10 | ✅/❌ |
| Appropriate Complexity | X/10 | ✅/❌ |
| Triggering Precision | X/10 | ✅/❌ |
## Where It's Strong
- [Factor]: [1 sentence]
## Where It Falls Short
- [Factor]: [1 sentence]
## Top Recommendations
- [carried over from Step 4]

Publish this with:

* **Parent page ID:** the skill page created in Step 9
* **Title:** `[skill name] — zAudit Summary [YYYY-MM-DD]` — the leading `z` is intentional, so this page alphabetically sorts below the skill page's other children (supplementary content, etc.).
* **Content format:** `markdown`

Call `createConfluencePage` with these parameters.

---

## Step 11: Publish Supplementary Content as Child Pages

If Step 1 found any files beyond `SKILL.md` (references, scripts, templates, examples, etc.), publish each one as a child page under the skill page just created in Step 9 — always, automatically, no need to ask the user first.

For each supplementary file:

* **Parent page ID:** the skill page created in Step 9 (not the Enterprise/Team page)
* **Title:** `[skill name] — [filename without extension] [YYYY-MM-DD]` (e.g. `gtm-plays-brainstorm — plays-library 2026-07-01`)
* **Content format:** `markdown` if the file is markdown/plain text; otherwise wrap the raw content in a code block with the appropriate language tag
* **Body:** the full raw file content, exactly as written — no summarizing, no paraphrasing, no abbreviating

Call `createConfluencePage` once per supplementary file. If there are several, publish them all before moving on — don't stop after the first.

After all are published, briefly note in the Step 13 confirmation that supplementary content was included, with links.

---

## Step 12: Handle Duplicate Titles

Since titles already include the date, collisions should be rare. If the API still returns a `409 Conflict` or duplicate title error (e.g. two submissions of the same skill on the same day), append a short time suffix (e.g. `14:32`) to the title and retry once. This applies to the main skill page, the audit summary from Step 10, and any supplementary child pages from Step 11.

---

## Step 13: Confirm with the URL

Once the page is created, respond with:

> ✅ **[skill name]** submitted to Confluence under **[Enterprise / Team → subpage name]**.  
> 🔗 [View it in the Skills space](webui%20link%20from%20API%20response)  
> 📋 **Audit summary** — [link]

If supplementary content was published in Step 11, add one line per file:

> 📎 **[filename]** added as a child page — [link]

Keep it short — just the confirmation and the link(s).
