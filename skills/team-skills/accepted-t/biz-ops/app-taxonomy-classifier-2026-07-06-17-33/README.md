<!-- Synced from Confluence page 6419316833: app-taxonomy-classifier 2026-07-06 17:33 -->

---

## name: app-taxonomy-classifier description: > LLM fallback classifier for the hybrid app taxonomy pipeline. Call this skill when the rule-based step produces zero matches for an app. Given an app name and table names (JSON), returns scored parent label candidates — and optionally scored sub-label candidates under each selected parent. Both passes use the same skill; the caller controls which pass is running by supplying the appropriate candidate list and optional parent context.

# App Taxonomy Classifier — LLM Fallback Skill

## Purpose

This skill is the **LLM fallback step** in a two-stage hybrid classification  
pipeline. The rule-based step runs first; this skill is only invoked for apps  
that produced **zero rule-based matches**.

The pipeline runs classification in **two sequential passes**:

1. **Parent pass** — classify the app into one or more parent labels from the  
   full parent list.
2. **Sub-label pass** — for each selected parent, classify the app into one or  
   more sub-labels from that parent's sub-label list. The selected parent(s) are  
   passed as additional context.

Both passes use this same skill. The caller controls the pass by supplying the  
appropriate candidate list (and, for the sub-label pass, the selected parents).

---

## Input Schema

json{
"app\_name": "string — required",
"table\_names": ["string", "..."],
"candidate\_labels": [
{
"label": "string",
"app\_name\_signals": "string — comma-separated keywords",
"table\_name\_signals": "string — comma-separated keywords",
"sub\_categories": "string — bullet list (parent pass only)",
"description": "string — one-sentence description (optional)"
}
],
"selected\_parents": ["string", "..."],
"pass": "parent | sublabel"
}

**Field notes:**

* `table_names` may be an empty array if no tables are known. The model should  
  weight app name more heavily in that case.
* `candidate_labels` is the full parent list on the parent pass, and the  
  sub-labels of ONE parent on the sub-label pass (called once per selected  
  parent).
* `selected_parents` is omitted on the parent pass; populated on the sub-label  
  pass to give the model context.
* `pass` tells the model which task it is performing (affects prompt framing).

---

## Output Schema

json{
"candidates": [
{
"label": "string",
"confidence": 0.0,
"reasoning": "string — one sentence"
}
],
"fallback\_triggered": false
}

**Field notes:**

* `candidates` is an ordered list, highest confidence first. Include all labels  
  with confidence > 0.10. Cap at 3 candidates.
* `confidence` is a float 0.0–1.0. Scores across all candidates do NOT need to  
  sum to 1.0; they reflect independent signal strength per label.
* `reasoning` is a single sentence explaining why the label fits this specific  
  app. It must reference something concrete from the input (a word in the app  
  name, a table name, etc.). Do not write generic reasoning.
* `fallback_triggered` is `true` when no candidate exceeds a confidence of 0.15,  
  meaning the model is defaulting to `Specialized / Niche Tools` (parent pass)  
  or the most generic sub-label (sub-label pass). The caller should log these  
  for human review.

---

## Taxonomy Reference

### Parent Labels (used in parent pass `candidate_labels`)

| Label | App Name Signals | Table Name Signals | Sub-categories |
| --- | --- | --- | --- |
| Project & Work Tracking | project, pmo, gantt, sprint, milestone, deliverable, workplan | projects, tasks, milestones, gantt dependencies, work orders, deliverables | Gantt & Timeline Management; Agile / Sprint Tracking; Portfolio & Program Management; Work Order Management; Resource & Capacity Planning |
| Contact & Relationship Management | crm, contact, customer, pipeline, prospect, account, broker | contacts, customers, accounts, leads, opportunities, activities, companies | Sales Pipeline & Opportunity Tracking; Customer Account Management; Partner & Broker Management; Interaction & Activity Logging; Lead Nurturing & Marketing Outreach |
| Request & Intake | intake, request, submission, portal, enrollment, service request | requests, applications, intake forms, submissions, referrals, inquiries | IT & Internal Service Requests; HR & Employee Requests; Grant & Program Applications; Patient / Client Intake Forms; External Portal Submissions |
| Reporting & Analytics | report, dashboard, analytics, metrics, kpi, scorecard, performance | reports, metrics, kpi, dashboards, summary table, factors, percentiles | Operational KPI Dashboards; Vendor & Supplier Scorecards; Financial Performance Reporting; Employee Performance Reviews; Data Aggregation / Hub Apps |
| Document & Content Management | document, content, knowledge, library, record manage, file manage | documents, document templates, document library, files, attachments, contracts | Contract Repository & Management; Policy & Procedure Libraries; Marketing & Creative Asset Management; Technical Documentation; Records Retention & Archiving |
| Inventory & Order Management | inventory, order, warehouse, procurement, fulfillment, purchase order | inventory, purchase orders, orders, shipments, line items, suppliers, parts | Warehouse & Stock Management; Purchase Order Tracking; Vendor & Supplier Management; Order Fulfillment & Shipment Tracking; Bill of Materials Management |
| Asset & Resource Tracking | asset, equipment, fleet, device, tool, vehicle, facility | assets, equipment, devices, fleet, vehicles, tools, facilities | IT Hardware & Device Registry; Facilities & Real Estate Inventory; Fleet & Vehicle Management; Tools & Equipment Checkout; Preventive Maintenance Scheduling |
| Case & Issue Management | case, ticket, issue, incident, support, helpdesk, bug, complaint | cases, tickets, issues, incidents, complaints, bugs, support tickets | IT Help Desk / Ticketing; Customer Support & Complaints; Safety Incident Reporting; Legal Case Management; Bug & Defect Tracking |
| Inspection & Audit | inspect, audit, checklist, safety check, assessment, walkthrough | inspections, audits, checklists, findings, corrective actions, defects | Safety & OSHA Compliance Audits; Quality Control Inspections; Field Site Assessments; Corrective Action Tracking (CAPA); Vendor / Supplier Audits |
| Financial Operations | invoice, budget, expense, billing, payroll, accounting, revenue | invoices, budgets, expenses, payments, purchase orders, transactions, payroll | Invoice & Billing Management; Budget Planning & Tracking; Expense Reporting & Reimbursement; Payroll Processing; Grant & Fund Accounting |
| Compliance & Certification Tracking | compliance, certification, license, permit, regulatory, renewal, accreditat | compliance, certifications, licenses, permits, risks, audits, renewals | Professional License & Certification Tracking; Regulatory Permit Management; Vendor Compliance & Pre-Qualification; Employee Training Compliance; Risk Register & Controls Management |
| Scheduling & Dispatch | schedul, dispatch, roster, shift, appointment, booking, crew | schedules, appointments, shifts, bookings, roster, dispatch, crew | Field Crew & Technician Scheduling; Appointment Booking; Shift & On-Call Roster Management; Resource Allocation to Job Sites; Event & Room Scheduling |
| Approval & Review Workflows | approval, review, sign-off, change request, change control, authorization | approvals, reviews, change requests, change orders, approvers, decisions | Change Request & Change Control; Document Sign-Off Routing; Budget & Spend Approvals; Leave & HR Approvals; Regulatory Submission Reviews |
| Onboarding & Lifecycle Management | onboard, lifecycle, enrollment, offboard, provision, registration, orient | onboarding, offboarding, enrollment, registrations, lifecycle, stages | Employee Onboarding & Offboarding; Client / Patient Enrollment; Student Registration & Lifecycle; IT Provisioning & Access Management; Product / Project Lifecycle Gates |
| Tests & Archives | test, testing, sandbox, dev, copy of, backup, archive, restore, dummy, demo, staging, uat, pilot | records, files (minimal tables typical) | Sandbox & Dev Environments; Backup & Restore Copies; UAT / QA Apps; Demos & Pilots; CSV Exports & Data Dumps |
| Specialized / Niche Tools | highly domain-specific names with no shared pattern | unique domain-specific table names with no shared pattern | Personal & Hobbyist Trackers; Highly Specialized Internal Tools; Single-Purpose Lookup Databases; Niche Industry Workflows; Platform Admin & Governance |

### Sub-labels by Parent (used in sub-label pass `candidate_labels`)

**Project & Work Tracking**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Gantt & Timeline Management | gantt, timeline, baseline | gantt, baseline dates, calendar days, gantt dependencies |
| Agile / Sprint Tracking | agile, sprint, scrum, kanban | sprints, backlog, user stories, kanban |
| Portfolio & Program Management | pmo, portfolio, program, initiative | programs, initiatives, portfolio, resource assignments |
| Work Order Management | work order, service order | work orders, job orders, service orders |
| Resource & Capacity Planning | resource, capacity, staffing | resources, resource assignments, capacity, team members, time cards |

**Contact & Relationship Management**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Sales Pipeline & Opportunity Tracking | sales, pipeline, opportunity, lead, prospect, bid | opportunities, leads, prospects, pipeline, quotes |
| Customer Account Management | account, customer, client | accounts, customers, clients, companies |
| Partner & Broker Management | partner, broker, dealer, distributor, affiliate | partners, brokers, dealers, distributors |
| Interaction & Activity Logging | activity, interaction, engagement, communication | activities, interactions, communications, call logs, notes |
| Lead Nurturing & Marketing Outreach | campaign, marketing, outreach, nurture | campaigns, leads, marketing, outreach |

**Request & Intake**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| IT & Internal Service Requests | it request, service request, it portal, help desk | service requests, it requests, help desk |
| HR & Employee Requests | hr request, leave request, employee request, time off | leave requests, hr requests, employee requests, time off |
| Grant & Program Applications | grant, grant portal, program application, application portal | grant applications, grant, program applications |
| Patient / Client Intake Forms | patient intake, client intake, referral | patient intake, referrals, client intake |
| External Portal Submissions | portal, external submission, public form | submissions, portal requests, public forms |

**Reporting & Analytics**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Operational KPI Dashboards | kpi, operational dashboard, ops metrics | kpi, metrics, operational data |
| Vendor & Supplier Scorecards | vendor scorecard, supplier scorecard | scorecards, vendor metrics, supplier ratings |
| Financial Performance Reporting | financial report, revenue report, p&l | financial data, revenue, expenses |
| Employee Performance Reviews | performance review, employee review | reviews, performance ratings, employees |
| Data Aggregation / Hub Apps | hub, aggregator, rollup, summary | summary table, aggregated data, rollups |

**Document & Content Management**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Contract Repository & Management | contract, agreement, msa | contracts, agreements, contract terms |
| Policy & Procedure Libraries | policy, procedure, sop | policies, procedures, sops |
| Marketing & Creative Asset Management | creative asset, marketing asset, brand | assets, creative files, brand materials |
| Technical Documentation | technical doc, documentation, spec | documents, specs, technical files |
| Records Retention & Archiving | records retention, archive, retention | archived records, retention schedules |

**Inventory & Order Management**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Warehouse & Stock Management | warehouse, stock, inventory count | inventory, stock levels, warehouse locations |
| Purchase Order Tracking | purchase order, po tracking | purchase orders, po line items |
| Vendor & Supplier Management | vendor, supplier management | vendors, suppliers, vendor contracts |
| Order Fulfillment & Shipment Tracking | fulfillment, shipment, shipping | shipments, orders, tracking numbers |
| Bill of Materials Management | bom, bill of materials | bom, components, materials |

**Asset & Resource Tracking**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| IT Hardware & Device Registry | hardware, device registry, it asset | devices, hardware, it assets |
| Facilities & Real Estate Inventory | facilities, real estate, building | facilities, buildings, locations |
| Fleet & Vehicle Management | fleet, vehicle | fleet, vehicles, mileage |
| Tools & Equipment Checkout | tool checkout, equipment checkout | tools, equipment, checkout logs |
| Preventive Maintenance Scheduling | preventive maintenance, pm schedule | maintenance schedules, pm tasks |

**Case & Issue Management**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| IT Help Desk / Ticketing | help desk, it ticket | tickets, it requests |
| Customer Support & Complaints | customer support, complaint | complaints, support tickets |
| Safety Incident Reporting | safety incident, incident report | incidents, safety reports |
| Legal Case Management | legal case, litigation | cases, legal matters |
| Bug & Defect Tracking | bug, defect | bugs, defects |

**Inspection & Audit**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Safety & OSHA Compliance Audits | osha, safety audit | audits, safety findings |
| Quality Control Inspections | quality control, qc inspection | inspections, qc findings |
| Field Site Assessments | field assessment, site assessment | assessments, site data |
| Corrective Action Tracking (CAPA) | capa, corrective action | corrective actions, capa records |
| Vendor / Supplier Audits | vendor audit, supplier audit | vendor audits, supplier findings |

**Financial Operations**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Invoice & Billing Management | invoice, billing | invoices, billing records |
| Budget Planning & Tracking | budget, budget planning | budgets, budget lines |
| Expense Reporting & Reimbursement | expense, reimbursement | expenses, reimbursements |
| Payroll Processing | payroll | payroll, pay periods |
| Grant & Fund Accounting | grant accounting, fund accounting | grants, funds |

**Compliance & Certification Tracking**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Professional License & Certification Tracking | license, certification | licenses, certifications |
| Regulatory Permit Management | permit, regulatory | permits, regulations |
| Vendor Compliance & Pre-Qualification | vendor compliance, prequalification | vendor compliance, prequal records |
| Employee Training Compliance | training compliance | training records, compliance status |
| Risk Register & Controls Management | risk register, controls | risks, controls |

**Scheduling & Dispatch**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Field Crew & Technician Scheduling | crew schedule, technician schedule | crew schedules, technician assignments |
| Appointment Booking | appointment, booking | appointments, bookings |
| Shift & On-Call Roster Management | shift, on-call, roster | shifts, on-call schedules, rosters |
| Resource Allocation to Job Sites | resource allocation, job site | resource assignments, job sites |
| Event & Room Scheduling | event schedule, room booking | events, room bookings |

**Approval & Review Workflows**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Change Request & Change Control | change request, change control | change requests, change orders |
| Document Sign-Off Routing | sign-off, signature routing | sign-offs, approvals |
| Budget & Spend Approvals | budget approval, spend approval | budget approvals, spend requests |
| Leave & HR Approvals | leave approval, hr approval | leave requests, hr approvals |
| Regulatory Submission Reviews | regulatory review, submission review | regulatory submissions, reviews |

**Onboarding & Lifecycle Management**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Employee Onboarding & Offboarding | onboarding, offboarding | onboarding tasks, offboarding tasks |
| Client / Patient Enrollment | client enrollment, patient enrollment | enrollments, client records |
| Student Registration & Lifecycle | student registration | registrations, student records |
| IT Provisioning & Access Management | it provisioning, access management | provisioning tasks, access requests |
| Product / Project Lifecycle Gates | lifecycle gate, project gate | lifecycle stages, gate approvals |

**Tests & Archives**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Sandbox & Dev Environments | sandbox, dev environment | dev records, sandbox data |
| Backup & Restore Copies | backup, restore, copy of | backup records |
| UAT / QA Apps | uat, qa | qa records, test cases |
| Demos & Pilots | demo, pilot | demo records, pilot data |
| CSV Exports & Data Dumps | csv export, data dump | export records, data dumps |

**Specialized / Niche Tools**

| Sub-label | App Name Signals | Table Name Signals |
| --- | --- | --- |
| Personal & Hobbyist Trackers | personal, hobby | personal records |
| Highly Specialized Internal Tools | specialized tool, internal tool | tool-specific tables |
| Single-Purpose Lookup Databases | lookup, reference database | lookup tables |
| Niche Industry Workflows | niche, industry-specific | industry-specific tables |
| Platform Admin & Governance | admin console, realm, pipelines, governance | pipelines, user tokens, apps |

---

## Examples

### Example 1 — Parent Pass, clear signal

**Input:**

json{
"pass": "parent",
"app\_name": "Squawk Tracker",
"table\_names": ["Squawk Item", "Maintenance Action", "Aircraft", "Part", "Technician"]
}

**Expected output:**

json{
"candidates": [
{
"label": "Case & Issue Management",
"confidence": 0.72,
"reasoning": "The word 'Squawk' (aviation defect terminology) combined with tables like 'Squawk Item' and 'Maintenance Action' indicates this tracks and manages aircraft defect cases."
},
{
"label": "Asset & Resource Tracking",
"confidence": 0.38,
"reasoning": "Tables for 'Aircraft', 'Part', and 'Technician' suggest secondary asset and resource tracking alongside the defect workflow."
}
],
"fallback\_triggered": false
}

---

### Example 2 — Parent Pass, weak signal → fallback

**Input:**

json{
"pass": "parent",
"app\_name": "Hayden Goertz",
"table\_names": ["Benefits", "Commission", "Paid Time Off (PTO)", "Reimbursements"]
}

**Expected output:**

json{
"candidates": [
{
"label": "Specialized / Niche Tools",
"confidence": 0.55,
"reasoning": "The app name is a personal name with no operational keyword, and while the tables suggest HR/financial topics, they span multiple categories without a dominant pattern."
}
],
"fallback\_triggered": true
}

**Note:** `fallback_triggered` is `true` here not because confidence is below 0.15, but because the best-fit label IS `Specialized / Niche Tools` — a legitimate classification, not an error. Reserve `fallback_triggered: true` for cases where the model genuinely cannot identify a good fit. When `Specialized / Niche Tools` is clearly the right answer (e.g. personal name apps, hobby trackers), confidence can be moderate and `fallback_triggered` should be `false`.

---

### Example 3 — Sub-label Pass

**Input:**

json{
"pass": "sublabel",
"app\_name": "Stop Loss Calculator",
"table\_names": ["Calculations", "Stop Loss Methods"],
"selected\_parents": ["Financial Operations"]
}

**Expected output:**

json{
"candidates": [
{
"label": "Budget Planning & Tracking",
"confidence": 0.52,
"reasoning": "A stop loss calculator maps most closely to budgetary risk thresholds; the 'Calculations' and 'Stop Loss Methods' tables support a planning/modeling function rather than invoicing or payroll."
},
{
"label": "Invoice & Billing Management",
"confidence": 0.12,
"reasoning": "No invoice-related tables are present, making this a weak secondary candidate."
}
],
"fallback\_triggered": false
}

---

### Example 4 — Parent Pass, "Copy of" pattern

**Input:**

json{
"pass": "parent",
"app\_name": "Copy of LTC Facility Management - 7.23",
"table\_names": ["Assets", "Buildings", "Employees", "Locations", "Medical Leave"]
}

**Expected output:**

json{
"candidates": [
{
"label": "Tests & Archives",
"confidence": 0.78,
"reasoning": "The 'Copy of' prefix with a date stamp is a strong signal for a backup or archive copy regardless of the underlying app's purpose."
},
{
"label": "Asset & Resource Tracking",
"confidence": 0.41,
"reasoning": "Tables like 'Assets', 'Buildings', and 'Locations' indicate the original app tracked facilities and assets."
}
],
"fallback\_triggered": false
}

**Note:** When an app name starts with "Copy of", "Backup", "Restore", "Archived", or ends with a date stamp, `Tests & Archives` should nearly always be the top candidate regardless of table content.

---

## Edge Cases & Disambiguation Notes

**"Records" / "Files" tables:** These are near-universal and carry almost no signal. Do not use them as primary evidence for any label.

**Generic app names (person names, single words, acronyms):** Lean on tables for signal. If both name and tables are ambiguous, trigger fallback to `Specialized / Niche Tools`.

**Multi-category apps:** It is valid to return 2–3 parent candidates if the app genuinely spans categories (e.g. a project tracker that also handles resource scheduling). Callers decide how to handle ties.

**Tests & Archives vs. operational:** If the app name has a "Copy of" prefix but the rest of the name is clearly operational (e.g., "Copy of Invoice Tracker"), return Tests & Archives as the top candidate AND the operational label as secondary. Do not drop the operational label — it may be used downstream if the caller determines the copy is being used as a live app.

**"YAML Converter" / calculators:** These are `Specialized / Niche Tools > Highly Specialized Internal Tools`. Do not attempt to map them to `Financial Operations` or `Reporting & Analytics` based on function words alone.

**Platform admin apps** (Realm, Admin Console, pipeline builders): These are `Specialized / Niche Tools > Platform Admin & Governance`. The presence of tables like "Pipelines", "User Tokens", "Apps" is the key signal.

---

## Caller Responsibilities (not part of this skill)

* Deciding the confidence threshold for accepting a candidate as a final label  
  (recommended starting point: ≥ 0.40 for a strong assignment, 0.20–0.39 for a  
  soft assignment flagged for review).
* Logging all `fallback_triggered: true` results for human review.
* Merging this skill's output with any partial rule-based scores from the primary  
  pipeline (not applicable for apps that fully bypassed rule-based matching, but  
  relevant if this skill is later adapted for tie-breaking).
* Iterating the sub-label pass once per selected parent.
