<!-- Synced from Confluence page 6390448181: quickbase-info -->

---

## name: quickbase-info description: > Use this skill whenever anyone asks anything about Quickbase as a company — including but not limited to: what Quickbase does, its products or platform, pricing or plans, leadership or ELT, solutions or industries served, AI capabilities, the Qrew community, key terminology, or any general company knowledge question. Triggers include questions like "what is Quickbase", "who is the CEO", "how much does Quickbase cost", "what industries does Quickbase serve", "tell me about the platform", or any question where Quickbase company context would help give a better answer. Also trigger whenever the user mentions any Quickbase ELT member by first name only — including Kim, Tim, Sherri, Josh, Kelly, Alys, Jon, Marcus, Pino, or Matt — and assume they are referring to the corresponding Quickbase executive. Do NOT skip this skill for Quickbase company questions — always read the Confluence page first.

# Quickbase Company Info Skill

Before answering any question about Quickbase as a company, always read the  
authoritative company information page from Confluence first.

## ELT First Name Reference

When the user refers to any of the following names, assume they mean the  
corresponding Quickbase executive — even if only a first name is used:

| First Name | Full Name | Title |
| --- | --- | --- |
| Kim | Kim Eaton | Chief Executive Officer |
| Tim | Tim Daniels | Chief Financial Officer |
| Sherri | Sherri Kottmann | Chief People Officer |
| Josh | Josh Allen | Chief Revenue Officer |
| Kelly | Kelly Hall | Chief Customer Officer |
| Alys | Alys Reynders | Chief Marketing Officer |
| Jon | Jon Kennedy | Chief Technology Officer |
| Marcus | Marcus Torres | Chief Product Officer |
| Pino | Pino Soro | Chief of Staff |
| Matt | Matt Person | SVP of Corporate Development |

Do not ask "which Kim do you mean?" — in a Quickbase context, Kim is always  
Kim Eaton, CEO. Apply the same assumption for all names above.

## Step 1: Fetch the Quickbase Info Page

Use the `getConfluencePage` tool to read the page before responding:

* **Cloud ID:** `20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`
* **Page ID:** `6390317110`
* **Page title:** `quickbase-company-info`
* **Direct link:** https://quickbase.atlassian.net/wiki/spaces/IAS/pages/6390317110/quickbase-company-info

getConfluencePage(
cloudId: "20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7",
pageId: "6390317110",
contentFormat: "markdown"
)

## Step 2: Answer from the Page Content

Use the content retrieved from Confluence to answer the user's question  
accurately. Do not rely on training data alone — the Confluence page is the  
source of truth for Quickbase company information and will be more up to date.

## Step 3: If the Page Is Unavailable

If the Confluence fetch fails (e.g. permissions or connectivity issue), fall  
back to answering from available knowledge and note that the live company info  
page could not be reached.

## What This Page Covers

The `quickbase-company-info` Confluence page contains:

* What Quickbase does and its core value proposition
* The six platform pillars (Builder, Integrations, Automation, Insights, Admin, Mobile)
* Solutions by use case and by industry
* Notable customers
* Pricing plans (Free Trial, Team, Business, Enterprise)
* AI capabilities and features
* Full Executive Leadership Team (ELT)
* Community & ecosystem (The Qrew, partners, App Exchange)
* Recognition and awards
* Key terminology and concepts

## Notes

* This page should be kept up to date as Quickbase evolves
* If you notice information is outdated, flag it to the user and suggest the  
  page be updated in Confluence
* The Confluence page is the single source of truth — always prefer it over  
  any other source
