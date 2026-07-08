<!-- Synced from Confluence page 6429048971: skill-auditor — Audit Summary 2026-07-08 -->

# Audit Summary: skill-auditor

**Category:** Team · **Verdict:** ✅ APPROVED · **Score:** 38/50 · **Submitted:** 2026-07-08

## Scores at a Glance

| Factor | Score | Status |
| --- | --- | --- |
| Instruction Engineering | 8/10 | ✅ |
| Conciseness | 8/10 | ✅ |
| Value Add | 8/10 | ✅ |
| Appropriate Complexity | 8/10 | ✅ |
| Triggering Precision | 6/10 | ✅ |

## Where It's Strong

* Instruction Engineering: The six-step flow is unambiguous and sequenced logically, with explicit fallback handling for users who don't want to answer intent questions.
* Value Add: Encodes a genuinely non-obvious judgment call — "understand intent before critiquing" — that a generic audit prompt wouldn't reliably produce on its own.

## Where It Falls Short

* Triggering Precision: No explicit "when NOT to use" clause distinguishing this from a production-readiness/scoring audit (e.g. skill-auditor-v2), creating overlap risk on phrases like "audit this skill" or "does this look right."

## Top Recommendations

* Add a one-sentence "when not to use" clause distinguishing this from a submission/production-readiness audit.
* Consider whether this should be reclassified as Enterprise given its org-wide applicability as more people author skills.
* Tighten Step 2's four intent-gathering questions to three by merging overlapping ones.

## Note on Overlap

At submission time, an existing page **skill-auditor-v2** was found with partially overlapping triggers (same "audit this skill" / "does this look right" phrasing, but a different core task — pass/fail scoring for company use vs. this skill's authoring-best-practices review and refine workflow). Flagged to the submitter, who chose to publish as-is.
