<!-- Synced from Confluence page 6399885467: confluence-submit 2026-06-30 -->

---

## name: confluence-submit description: > Trigger this skill whenever the user says "/submit" — with or without anything else in the message. This skill takes the skill being discussed in the current conversation and publishes it as a new child page in the Internal AI Skills Confluence space (IAS), filed under the current week's parent page (titled "Week of [Month] [Day]"). If this week's page doesn't exist yet, it asks the user before creating one. Use this skill immediately when "/submit" appears anywhere in the user's message. Do not ask for confirmation before proceeding with the skill submission itself — just submit and report back with the URL. The only thing requiring confirmation is creating a brand-new week page.

# /submit — Publish Skill to Confluence

When the user says `/submit`, immediately publish the skill currently being discussed to Confluence,  
filed under the correct week's parent page.

---

## Step 1: Identify the Skill Content

Look at the current conversation to find the skill. It will be one of:

**A) Pasted content or uploaded file** — the user has shared raw [SKILL.md](http://SKILL.md) text directly in the chat or uploaded a file. Use that.

**B) A named skill on disk** — the user has referred to a skill by name (e.g. "the cloud vowel counter skill"). Find it under:

* `/mnt/skills/user/[skill-name]/SKILL.md`
* `/mnt/skills/public/[skill-name]/SKILL.md`

Read the file with the `view` tool to get the full content.

**C) A skill just created this session** — a [SKILL.md](http://SKILL.md) was written to `/home/claude/` during this conversation. Use that content.

If it's ambiguous which skill the user means, check the most recent skill mentioned or worked on in the conversation. Only ask for clarification if there are genuinely multiple candidates and no clear most-recent one.

---

## Step 2: Extract the Skill Name

Parse the YAML frontmatter at the top of the skill file to get the `name` field. This will be the Confluence page title.

yaml---
name: my-skill-name ← use this as the page title
description: ...
---

If no `name` field exists, use the filename (minus `.md`) as the title.

---

## Step 3: Find or Create This Week's Parent Page

Skills are no longer filed directly under a single static "Skills" page — they're organized by  
week. Each week has its own parent page titled `Week of [Month] [Day]` (e.g. `Week of Jun 29`),  
where the date is the Monday that starts that week. New skills get published as a child page  
under the current week's page.

**3a. Determine the current week's label**

Using today's date, find the most recent Monday (if today is Monday, that's today). Format the  
label as `Week of [Mon] [D]` — three-letter month abbreviation, no leading zero on the day  
(e.g. `Week of Jun 29`, not `Week of June 29` or `Week of Jun 09`).

**3b. List existing week pages**

Call `getConfluencePageDescendants` on the IAS space's top-level skills container  
(`pageId: 6386385580`, the "Internal AI Skills" homepage) to list its child pages, and check  
their titles for one matching this week's label exactly.

**3c. Branch based on what you find**

* **If a page with this week's exact title already exists** — use its page ID as the parent for  
  the new skill page. Skip to Step 4.
* **If no page with this week's title exists** — don't create it silently. Ask the user whether  
  to create this week's page now (as a new top-level page under the IAS homepage) or file the  
  skill under a different existing week's page instead. Only proceed to create the page after  
  they confirm.

  + If they confirm creation: call `createConfluencePage` with  
    `cloudId: 20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`, `spaceId: 6386384916`,  
    `parentId: 6386385580` (top-level, alongside other week pages), `title`: this week's label,  
    and a minimal body (a single space or short placeholder is fine). Use the new page's ID as  
    the parent for the skill page. Continue to Step 4.

---

## Step 4: Publish the Skill as a Child Page

Use the Atlassian MCP to create the page with these values:

* **Cloud ID:** `20d966ed-3d3f-4c0c-b14b-c1dbb9bb6aa7`
* **Space ID:** `6386384916` (Internal AI Skills / IAS)
* **Parent page ID:** the current week's page ID, resolved or created in Step 3
* **Title:** the skill's `name` from frontmatter
* **Content format:** `markdown`
* **Body:** the full raw [SKILL.md](http://SKILL.md) content, exactly as written — no summarizing, no paraphrasing, no abbreviating

Call `createConfluencePage` with these parameters.

---

## Step 5: Handle Duplicate Titles

If the API returns a `409 Conflict` or duplicate title error, append the current date to the title (e.g. `my-skill-name 2026-06-25`) and retry once.

---

## Step 6: Confirm with the URL

Once the page is created, respond with:

> ✅ **[skill name]** submitted to Confluence under **[week page title]**.  
> 🔗 [View it in the Skills space](webui link from API response)

Keep it short — just the confirmation and the link.
