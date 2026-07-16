<!-- Synced from Confluence page 6454542500: ai-use-case-roi — assumptions 2026-07-16 -->

json{
"\_meta": {
"version": "1.0.0",
"owner": "RevOps — <assign a named owner>",
"last\_updated": "2026-06-29",
"note": "These are the HOUSE assumptions. They are the single authority for every ROI estimate. Do not change per-estimate — change here, bump the version, and every future estimate inherits it. Any per-case deviation must be recorded as an explicit override with a reason (the engine flags these). Argue with the owner of this file, not with individual briefs.",
"changelog": [
"1.0.0 (2026-06-29): initial house assumptions extracted from methodology v1"
]
},
"role\_costs\_loaded\_annual": {
"\_comment": "Fully-loaded annual cost (salary + benefits + overhead ≈ base × 1.3). NOT OTE. OTE only enters revenue math, never time-valuation.",
"SDR": 95000,
"AE": 143000,
"CSM": 150000,
"RevOps\_analyst": 120000,
"support\_rep": 85000,
"renewals\_specialist": 100000,
"PMM\_PM": 165000,
"engineer": 190000,
"manager": 210000
},
"hours\_per\_year": 2080,
"working\_days\_per\_year": 260,
"builder\_role": "engineer",
"scenario\_levers": {
"\_comment": "Scenario variance comes from DELIVERY levers only. Business-chain values (at-risk rate, churn lift, ARR) are point estimates with separate sensitivity — they do not swing by scenario.",
"automation\_share": {"conservative": 0.50, "expected": 0.65, "optimistic": 0.80},
"adoption\_steadystate": {"conservative": 0.40, "expected": 0.60, "optimistic": 0.75},
"coverage": {"conservative": 0.70, "expected": 0.85, "optimistic": 0.95},
"attribution": {"conservative": 0.50, "expected": 0.50, "optimistic": 0.80}
},
"adoption\_year1\_ramp": 0.70,
"coverage\_year1\_ramp": 0.80,
"revenue\_chain\_defaults": {
"\_comment": "Defaults for the redeploy/revenue path. Conservative by design. Per-case overrides must be justified.",
"conversion\_to\_productive": 0.50,
"hours\_per\_downstream\_unit": 3,
"at\_risk\_rate": 0.10,
"churn\_reduction": 0.15
},
"run\_cost\_per\_instance": {
"light": 0.06,
"medium": 0.30,
"heavy": 1.00
},
"run\_cost\_platform\_annual\_default": 1000,
"build\_tshirt\_weeks": {"S": 2, "M": 6, "L": 12},
"confidence\_multiplier": {"High": 1.0, "Medium": 0.7, "Low": 0.4},
"near\_zero\_floor\_usd": 15000
}
