<!-- Synced from Confluence page 6430097485: skill-auditor 2026-07-08 -->

---

## name: skill-auditor description: Audit and refine an existing Claude Skill (a [SKILL.md](http://SKILL.md) file, with any bundled scripts/references/assets) against Anthropic's best practices for skill authoring — description quality and triggering strength, progressive disclosure, writing style, structure, and the lack-of-surprise principle. Use this whenever the user wants to review, audit, check, clean up, tighten, or "make sure this skill follows best practices," asks whether a skill is well-written or will trigger reliably, wants a quality pass before packaging or sharing a skill, or has just drafted a new skill and wants it reviewed. Trigger on phrases like "review my skill," "does this [SKILL.md](http://SKILL.md) look right," "audit this skill," "clean this up," or "check this against Anthropic's guidelines" — even if the user just pastes or uploads a [SKILL.md](http://SKILL.md) without further explanation.

# Skill Auditor

A skill for reviewing an existing skill against Anthropic's authoring best practices and refining it — without losing what the original author actually intended.

The temptation with a "best practices checker" is to treat it as a linter: scan the file, flag deviations, rewrite. Resist that. A [SKILL.md](http://SKILL.md) often encodes business-specific judgment calls — an exact template a stakeholder requires, a deliberately narrow trigger condition, a tool call that has to stay exactly as written. Mechanically "fixing" those without understanding why they're there is how a well-meaning audit quietly breaks something that worked. So this skill puts one extra step before any editing: understand what the skill is for and what must not change, from the person who wrote or owns it.

## Step 1: Locate and read the skill

Find the [SKILL.md](http://SKILL.md) the user wants reviewed (uploaded file, a path, or pasted directly into the conversation). Read the full file — frontmatter (`name`, `description`, any `compatibility` field) and the body. If there's a bundled `scripts/`, `references/`, or `assets/` directory alongside it, list what's there and skim how (or whether) the [SKILL.md](http://SKILL.md) body actually points to each one.

If you can't find the file or the user only described the skill verbally, ask for it rather than guessing at content that isn't in front of you.

## Step 2: Understand intent before critiquing

This is the step that separates a useful audit from a destructive one. Before touching anything, get the context that isn't visible in the file itself:

* In one sentence, what should Claude be able to do after this skill triggers that it couldn't do well on its own?
* Who uses this, and in what real conversations should it fire — and just as importantly, where should it *not* fire?
* Are there specific phrasings, business terms, tool names, or file types that real users will actually type, which the description needs to catch?
* Is there anything in here that must not change — an exact template, a required tool call, a compliance or brand requirement, a hard-won fix for a past failure?

Ask these conversationally (the `ask_user_input_v0` tool works well if there's a natural way to turn them into short-option questions — otherwise just ask in plain prose). If the user says "just use your best judgment, I don't have time," that's a valid answer — proceed to Step 3 and flag your assumptions clearly in Step 4 instead of blocking on an answer you won't get.

## Step 3: Run the checklist

Read `references/best-practices-checklist.md` for the full set of criteria — it covers frontmatter/description quality, progressive disclosure, writing style and patterns, structure, and the lack-of-surprise/security principle. Go through the skill against each relevant section and note, with specific line or section references, whether it passes, fails, or is a judgment call.

Don't apply every criterion mechanically if it doesn't fit the skill's actual size or purpose — e.g., a short, single-purpose skill doesn't need bundled reference files just to have them, and a skill with genuinely narrow scope doesn't need a "pushier" description just for the sake of it. Use the checklist to spot real gaps, not to pad findings.

## Step 4: Present findings before editing

Summarize what you found in three buckets, referencing what you learned in Step 2 where relevant:

1. **Clear violations** — things that should just be fixed (e.g., description doesn't state *when* to trigger, body exceeds ~500 lines with no hierarchy, instructions use rigid ALL-CAPS rules with no explanation of why).
2. **Judgment calls** — things that could go either way depending on intent, especially anything that touches what the user flagged in Step 2 as intentional or must-not-change. Ask before touching these.
3. **Nice-to-haves** — small polish items that aren't worth blocking on if the user wants to move fast.

Wait for the user to weigh in on the judgment calls before rewriting anything.

## Step 5: Refine

Once you know what to change, rewrite the [SKILL.md](http://SKILL.md) (and any reference files, if they also need cleanup). Preserve everything the user flagged as intentional. Show the changes as a clear before/after summary organized by the same buckets from Step 4 — not just a wall of the full rewritten file — so the user can review quickly and see exactly what moved and why.

## Step 6: Offer next steps

Once the user is happy with the content, mention that:

* The `skill-creator` skill can run actual test prompts against the refined skill and help package it as a `.skill` file for download/install, if they want more than a content review.
* If the description was a major point of revision, `skill-creator`'s description-optimization loop can test triggering accuracy empirically rather than by inspection alone (Claude Code / Cowork only).

Offer these — don't assume the user wants the full test-and-package loop just because they asked for an audit.
