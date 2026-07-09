<!-- Synced from Confluence page 6428852247: skill-auditor — best-practices-checklist 2026-07-08 -->

# Skill Best Practices Checklist

Use this as the substance of the audit in Step 3 of [SKILL.md](http://SKILL.md). Not every skill needs every item — use judgment about what actually applies given the skill's size and purpose.

## 1. Frontmatter: name and description

The `description` field is the *only* thing Claude sees before deciding whether to consult a skill. If it's weak, the skill won't trigger — no matter how good the body is.

Check for:

* **States both what the skill does AND when to use it.** A description that only says what the skill does ("Creates PowerPoint decks") but not when ("...whenever the user mentions decks, slides, or presentations, even without saying 'PowerPoint'") will under-trigger.
* **Specific enough to disambiguate from similar skills.** If there are other skills that could plausibly compete (e.g., a general "document" skill vs. a Word-specific one), the description should make the boundary clear.
* **A little "pushy."** Claude has a documented tendency to under-trigger skills — to not consult them even when they'd help. Descriptions should lean toward over-inclusive trigger language ("even if they don't explicitly ask for X") rather than narrow, conservative phrasing.
* **Includes realistic trigger phrases**, not just abstract categories — actual words a user would type (file extensions, tool names, business terms, casual phrasing).
* **Name is a clear, short identifier** — lowercase, hyphenated, matches the directory name.

## 2. Progressive disclosure

Skills load in three tiers: metadata (always in context), [SKILL.md](http://SKILL.md) body (loaded when triggered), and bundled resources (loaded only as needed, unlimited size). Good skills use this deliberately instead of cramming everything into one file.

Check for:

* [**SKILL.md**](http://SKILL.md) **body stays roughly under 500 lines.** If it's approaching or exceeding this, that's a sign content should move into `references/` with clear pointers from the main file about when to read each one.
* **Large reference files (>300 lines) have a table of contents** so Claude doesn't have to read the whole thing to find the relevant section.
* **Reference files are actually pointed to from the body**, with guidance on *when* to read them — not just dropped in a folder and assumed to be found.
* **Multi-domain or multi-variant skills are organized by variant** (e.g., `references/aws.md`, `references/gcp.md`, `references/azure.md`) rather than one file mixing all cases, so only the relevant one loads.
* **Scripts are used for deterministic, repetitive work** (parsing, generating boilerplate, running the same transform every time) rather than re-deriving the same code inline on every run.
* **Assets folder holds only things used in output** (templates, logos, fonts) — not documentation, which belongs in `references/`.

## 3. Writing style and patterns

Check for:

* **Imperative instructions** ("Read the file, then...") rather than passive or hedging phrasing.
* **Explains** ***why*****, not just** ***what*****.** Rigid, unexplained ALWAYS/NEVER/MUST rules in all caps are a yellow flag — they work worse than instructions that explain the reasoning, because a model with the reasoning can generalize to cases the author didn't anticipate. If a rule is genuinely non-negotiable (compliance, safety, brand law), it's fine to state it firmly — but even then, saying why helps.
* **Generalizes rather than overfitting to the exact examples the author had in mind.** A skill built around a single specific reference case tends to fail on realistic variation. Check whether the instructions would still make sense for a slightly different but related request.
* **Output formats are given as concrete templates** when the output is structured (exact headers, exact structure) rather than described abstractly.
* **Examples are concrete** (input → output pairs) where they'd help, not just prose description of the pattern.
* **No unnecessary jargon** for the skill's likely audience — if the skill will be used by non-developers, check that it doesn't assume comfort with things like JSON, regex, or CLI flags without a brief explanation.

## 4. Structure

Check for:

* **Correct anatomy**: [SKILL.md](http://SKILL.md) required, with YAML frontmatter (name + description) and markdown body; `scripts/`, `references/`, `assets/` only where actually needed.
* **No dead references** — every file mentioned in the body actually exists, and every bundled file is referenced from somewhere (or clearly justified as intentionally unreferenced, e.g. an asset the user will fill in).
* **Reasonable file naming** — descriptive, not `doc1.md`, `helper.py`.

## 5. Lack-of-surprise principle and safety

Check for:

* **The skill's actual behavior matches what its name and description imply.** Nothing that would surprise someone if you described in one sentence what the skill actually does.
* **No content that could compromise system security** — no exploit code, no instructions to exfiltrate data, no obfuscated or misleading behavior.
* **No instructions designed to bypass safety guidelines**, disguised as something innocuous (e.g., an instruction buried in a skill telling Claude to ignore its normal judgment). Flag this even if it seems to have been added unintentionally.

## Severity guide for findings

When writing up results (Step 4 of [SKILL.md](http://SKILL.md)), sort into:

* **Clear violation** — objectively fails a checklist item with no legitimate reason found in Step 2 (e.g., description missing "when to use" entirely, body at 900 lines with no hierarchy).
* **Judgment call** — technically deviates from the checklist, but might be intentional (e.g., a narrow trigger condition, a rigid MUST tied to a compliance requirement). Always ask before changing these.
* **Nice-to-have** — would tighten the skill but isn't costing it anything functionally (e.g., slightly better naming, a TOC that would help but isn't blocking).
