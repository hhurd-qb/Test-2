<!-- Synced from Confluence page 6455099437: ai-use-case-roi — Enterprise 2026-07-16 -->

---

## name: ai-use-case-roi description: >- Scope a proposed AI/automation use case into a realistic, defensible ROI estimate and push it to the Confluence ROI register for prioritization. Arithmetic is done by a deterministic engine (references/roi\_engine.py) against a versioned, owned assumptions library (references/assumptions.json), so the same inputs always yield the same number for everyone. Runs a short interview, grounds inputs in system data (Snowflake/Salesforce/Gainsight) instead of trusting memory, records any deviation from house assumptions as an explicit override, runs the engine, and publishes behind a validation gate. Use WHENEVER a user wants to estimate, scope, justify, or prioritize an AI or automation idea - 'ROI of automating X', 'should we build an agent for Y', 'scope this use case', 'add this to the ROI register', 'business case for [AI idea]'. Requires the Atlassian connector and code execution enabled; uses Snowflake/Salesforce/Gainsight for grounding when available.

# AI Use Case ROI (v2)

## What changed from v1, and why it matters

v1 had the LLM do the math in prose. That made every estimate a fresh re-derivation - the same case  
could score differently across sessions (it did: a QBR case came out $49K by hand and $25K from the  
engine because a conversion step was silently skipped one time). For a tool whose entire purpose is  
*ranking*, that non-determinism is disqualifying. So v2 splits the work:

* **You (the LLM) do:** elicitation, classification, **data-grounding**, override capture, narrative,  
  and the Confluence write. You do **not** do arithmetic or invent assumptions.
* **The engine does:** all math, deterministically, from `assumptions.json`. Same inputs -> same  
  output, for everyone, forever. Confidence is *derived from evidence*, not asserted.

Trust in this system comes from four things, in order: inputs grounded in real data, a method nobody  
can quietly bend, a human who owns the assumptions, and a published track record of projected-vs-  
realized. Your job is the first two on every run.

## Workflow

### Step 1 - Read the assumptions and the schema

Read `references/assumptions.json` (the house numbers - never override them ad hoc in your head) and  
`references/schema.md` (the input contract). You will assemble an inputs JSON that conforms to the  
schema and hand it to the engine.

### Step 2 - Classify, then interview (<=7 questions)

Propose the value type (labor / revenue / risk / capability) and delivery model (augmentation vs  
autonomous) from the one-liner, then ask only what you can't infer. Prefer tappable options. The  
must-ask set is unchanged from v1 (use case; who/how many; volume; time per instance; value-type  
confirm; the gate; build-weeks) **plus, for any revenue or redeploy case, two required numbers that**  
**were benchmarks in v1 and are too load-bearing to guess: average ARR/account and the baseline rate**  
**the AI is supposed to move** (churn rate, win rate, conversion, etc.).

### Step 3 - GROUND the inputs in system data (this is the trust win)

Do not accept volume, headcount, or baseline rates from memory when a system knows the real number.  
Before finalizing each of these, check the connected systems and reconcile:

* **Volume / instance counts** -> Snowflake or Salesforce ("you said 200 QBRs/yr; Gainsight shows  
  187 logged last 12 mo - use 187?").
* **Headcount / eligible population** -> the relevant system of record.
* **Baseline rates** (churn, win rate, at-risk %) -> Gainsight (health/churn), Salesforce (win rate).
* **Average ARR** -> Salesforce / Snowflake.

Record provenance for each in the inputs JSON `data_grounding` block with `source: "system"` or  
`source: "user"` and the system value. The engine reads this to derive confidence - a case built on  
system-grounded numbers earns higher confidence automatically; one built on memory scores Low. Tell  
the user what you grounded and what you couldn't. If a connector isn't available, say so and mark the  
input user-supplied - don't silently treat a guess as fact.

### Step 4 - Capture overrides explicitly

Any per-case value that differs from `assumptions.json` (e.g. at-risk rate 20% vs house 10%) goes in  
the `overrides` array with a `reason`. The engine surfaces these in the output and on the page.  
Deviating from the house method is allowed; hiding it is not. If you find yourself wanting to  
override several house numbers to make a case work, that is a signal the case is weak - say so.

### Step 5 - Run the engine

Write the inputs JSON to a file and run:  
`python references/roi_engine.py inputs.json`  
Use the returned numbers verbatim. **Do not recompute, round differently, or "adjust" the engine's**  
**output** - that reintroduces exactly the drift v2 exists to kill. If a number looks wrong, the fix is  
the inputs or the assumptions file, not a manual edit.

### Step 6 - Present the result honestly

Show the headline (conservative -> expected net, payback, 3-yr ROI), the derived confidence *and its*  
*reason*, the capacity figure if any, every override with its reason, and what was/wasn't grounded.  
Lead with the conservative number. If the engine returns a `near_zero` flag, lead with the **verdict**  
("don't build this for the ROI - here's the real reason to, or don't"), not the number. If it returns  
`table: capability`, present it as an option-value bet with $0 hard ROI.

Be explicit about total uncertainty: the displayed range reflects delivery levers only; the business-  
chain inputs (at-risk %, churn lift, ARR) carry their own 2x+ uncertainty, so the true error bar is  
wider than the conservative-expected band. Say this. False precision loses the finance audience.

### Step 7 - Validation gate before publish

An estimate does not go on the register on one person's say-so. Before writing to Confluence:

* If confidence is **Low** OR any load-bearing input is user-supplied (not grounded) OR there are >=2  
  overrides -> the entry is publishable only as **DRAFT / pending validation**, and you must name who  
  should validate it (e.g. "RevOps to confirm at-risk rate from Gainsight before this counts").
* **High/Medium** with grounded inputs -> publishable as PROJECTED.  
  Never publish a number as validated that isn't. State the gate outcome to the user.

### Step 8 - Push to Confluence (confirm first)

Follow `references/confluence.md`. Create the detail page (include the grounding provenance, the  
overrides table, and the validation status), append/sort the register row, and return the link.  
Always preview and get a yes before writing.

## Portfolio integrity (run before any register total)

Every case records a `shared_capacity_pool` (e.g. "CSM-hours", "AE-selling-hours"). Before anyone  
sums the register or reports a portfolio number, run:  
`python references/roi_engine.py --portfolio path/to/cases/*.json`  
It flags when multiple redeploy/headcount cases claim value from the *same* freed hours - which  
cannot all be true at once. Do not sum conflicting cases' hard cash. This is the guard against the  
aggregation error that discredits hand-built portfolio numbers.

## Governance (state these; they are the trust backbone, not optional extras)

* `assumptions.json` has a named owner (RevOps/Finance). Challenges to method go to the owner and  
  a version bump - not to per-entry debates. Assign the owner before opening this to submitters.
* **Lifecycle:** entries are PROJECTED, reviewed on a set cadence, and expire if not validated. A  
  stale register poisons trust in the fresh entries.
* **Track record is the real currency:** publish projected-vs-realized for every shipped case,  
  including misses. Nothing else converts "a clever tool" into "the number the business believes."  
  Capture the baseline + metric now (measurement plan on every page) even though the payoff is months  
  out.

## Honest scope

This tool imposes disciplined, transparent, *reproducible* argument on AI-investment decisions. It is  
not an objective oracle - inputs are still elicited, and the revenue path still depends on judgment.  
Sell it as a structured argument backed by an owned method and a track record, not as truth. For small  
decisions, don't over-model - a coarse cash/capacity/capability x S/M/L triage is often the honest  
right-sized answer; reserve the full engine for cases big enough to justify it.
