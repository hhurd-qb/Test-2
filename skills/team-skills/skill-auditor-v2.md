<!-- Synced from Confluence page 6401622035: skill-auditor-v2 -->

---

## name: skill-auditor-v2 description: > Evaluate and score a skill's quality for company use. Trigger whenever a user shares a skill (as a [SKILL.md](http://SKILL.md) file, .skill file, or pasted content) and asks whether it's "good enough", "ready", "approved", "any good", "does this look right", "would you use this", or wants it reviewed, rated, graded, or audited. Also trigger when the user asks if a skill "passes" or "meets the bar" for their company or team, or drops a skill file without explanation — assume they want it audited unless they explicitly say otherwise (e.g. "just use this as context", "don't audit this"). Do NOT trigger for general questions about what skills are or how they work, and do NOT trigger when a skill is shared purely as reference material for another task.

# Skill Auditor

Evaluate a submitted skill by first classifying it, then applying the appropriate scoring framework. Follow each step in order — do not skip to scoring before classifying.

---

## Step 1: Pre-flight Checks

Before classifying, check for these common failure modes:

**No frontmatter:** If the skill has no YAML frontmatter (no `name` or `description` field), it cannot trigger and will automatically score 1/10 on Triggering Precision regardless of other quality. Flag this immediately at the top of the report.

**Ambiguous classification:** If the skill could plausibly be Team or Enterprise, default to Team and note the ambiguity explicitly in the report. Explain what would need to change for it to qualify as Enterprise. Do not upgrade a skill's classification based on quality — only on scope of usefulness.

**Shared as context:** If the user explicitly indicates the skill is being shared for reference rather than evaluation (e.g. "just use this", "don't audit this", "use this as context"), do not audit. Acknowledge the skill and proceed with whatever the user actually asked for. A silent file drop with no instructions is not a context share — treat it as an audit request.

---

## Step 2: Classify the Skill

**Individual** — Personal or fun, no direct working value. Improves daily life or is creative but brings no benefit to team workflows or the org. Examples: vowel counters, journaling assistants, habit trackers.

**Team** — Useful for a specific team's workflow or productivity. Encodes domain-specific knowledge, automates a team process, or improves consistency within a group. Examples: Jira query rules for engineering, a brand voice guide for marketing, a sales call prep checklist.

**Enterprise** — Broadly useful across the entire org regardless of team or role. Encodes company-wide standards, policies, or processes everyone would benefit from. Examples: company branding requirements, onboarding workflows, compliance checklists, universal writing standards.

**Upgrade check (Team skills only):** After scoring, if a Team skill scores 9–10 on Value Add, add an upgrade note to the report flagging it as a candidate for enterprise-wide rewrite. Do this as a final step — do not reclassify based on score.

---

## Step 3: Apply the Right Framework

### If INDIVIDUAL → No Scoring

## Skill Audit Report: [Skill Name]
\*\*Category: Individual\*\*
This skill has been classified as personal/individual. It will not be scored or committed to the company skill library.
\*\*Reason:\*\* [1–2 sentences explaining why.]
\*\*Recommendation:\*\* May be useful as a personal install but is not appropriate for shared company use.

---

### If TEAM or ENTERPRISE → Score Using the Rubric Below

Score each factor 1–10. Apply the threshold column that matches the skill's category — ignore the other.

#### Factor 1: Instruction Engineering

*Are the instructions well-crafted, internally consistent, and actionable?*

| Score | Criteria |
| --- | --- |
| 9–10 | Precise, unambiguous, structured. Edge cases handled. Claude would know exactly what to do at every stage with no guesswork. |
| 7–8 | Mostly clear with minor gaps a capable reader could fill. |
| 5–6 | Some vagueness, but core intent is decipherable. |
| 3–4 | Contradictory, confusing, or leaves major gaps. |
| 1–2 | Barely coherent or entirely undefined. |

#### Factor 2: Conciseness

*Is the skill as short as it needs to be — and no shorter?*

| Score | Criteria |
| --- | --- |
| 9–10 | Every sentence earns its place. Dense but readable. No redundancy. |
| 7–8 | Mostly tight. A sentence or two could be cut. |
| 5–6 | Noticeable padding or repeated content, but core is navigable. |
| 3–4 | Significantly bloated or redundant. |
| 1–2 | Extremely verbose or critically terse. |

#### Factor 3: Value Add

*Does this skill meaningfully improve a workflow that Claude couldn't handle well alone?*

| Score | Criteria |
| --- | --- |
| 9–10 | Encodes non-obvious knowledge Claude couldn't reliably replicate alone. Clear ROI. |
| 7–8 | Adds real value — improves consistency or quality in context. |
| 5–6 | Marginal value. Claude could mostly handle this natively. |
| 3–4 | Replicates something Claude already does well. Little added value. |
| 1–2 | No value, or counterproductive. |

#### Factor 4: Appropriate Complexity

*Is the complexity level right for the job?*

| Score | Criteria |
| --- | --- |
| 9–10 | Complexity matches the task perfectly. Nothing superfluous, nothing missing. |
| 7–8 | Slight mismatch but not harmful. |
| 5–6 | Noticeably over- or under-engineered. |
| 3–4 | Major mismatch. |
| 1–2 | Completely inappropriate complexity. |

#### Factor 5: Triggering Precision

*Will this trigger when needed — and only then?*

| Score | Criteria |
| --- | --- |
| 9–10 | Covers formal and informal phrasings. Explicit "when NOT to use" clause. Handles edge cases like silent file drops and context-only shares. No false-positive risk. |
| 7–8 | Good coverage. Minor over/under-trigger risk. |
| 5–6 | Vague or generic. May miss edge cases or misfire. |
| 3–4 | Too broad or too narrow. |
| 1–2 | Absent, nonsensical, or wrong. |

---

### Pass Thresholds

| Factor | Team | Enterprise |
| --- | --- | --- |
| Instruction Engineering | ≥ 5 | ≥ 7 |
| Conciseness | ≥ 5 | ≥ 6 |
| Value Add | ≥ 6 | ≥ 7 |
| Appropriate Complexity | ≥ 5 | ≥ 6 |
| Triggering Precision | ≥ 5 | ≥ 7 |
| **Total** | **≥ 32/50** | **≥ 38/50** |

A skill fails if any single factor is below its category threshold — even if the total passes.

---

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

---

## Core Rules

* **Classify by scope, not quality.** A well-written Team skill is still a Team skill. Only promote to Enterprise if the use case is genuinely org-wide.
* **Single factor failure = full rejection.** A skill that fails any one factor is rejected even if the total passes. State the failing factor explicitly in the verdict.
* **Recommendations must be actionable.** "Improve the instructions" is bad. "Split step 3 into two steps and define the output format explicitly" is good.
* **Do not inflate scores.** A 47/50 should be rare. Most real-world skills have real flaws — find them.
