<!-- Synced from Confluence page 6420234248: app-taxonomy-classifier 2026-07-06 -->

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

---

## Edge Cases & Disambiguation Notes

**"Records" / "Files" tables:** These are near-universal and carry almost no signal. Do not use them as primary evidence for any label.

**Generic app names (person names, single words, acronyms):** Lean on tables for signal. If both name and tables are ambiguous, trigger fallback to `Specialized / Niche Tools`.

**Multi-category apps:** It is valid to return 2–3 parent candidates if the app genuinely spans categories. Callers decide how to handle ties.

**Tests & Archives vs. operational:** If the app name has a "Copy of" prefix but the rest of the name is clearly operational, return Tests & Archives as the top candidate AND the operational label as secondary.

**"YAML Converter" / calculators:** These are `Specialized / Niche Tools > Highly Specialized Internal Tools`.

**Platform admin apps:** These are `Specialized / Niche Tools > Platform Admin & Governance`.

---

## Caller Responsibilities (not part of this skill)

* Deciding the confidence threshold for accepting a candidate as a final label (recommended: ≥ 0.40 strong, 0.20–0.39 soft/flagged).
* Logging all `fallback_triggered: true` results for human review.
* Iterating the sub-label pass once per selected parent.
