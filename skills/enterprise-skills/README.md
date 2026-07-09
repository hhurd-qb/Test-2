<!-- Synced from Confluence page 6386352141: Enterprise Skills -->

# What Are Skills?

Skills are reusable instruction sets that teach Claude how to handle specific tasks, workflows, or domains. Each skill is a `SKILL.md` file containing a name, a triggering description, and step-by-step instructions that Claude follows when the skill is activated.

## How Skills Work

Skills appear in Claude's context as a list of available capabilities. Claude reads each skill's name and description to decide whether to consult it for a given task. When a skill is triggered, Claude loads the full instructions and follows them to complete the request.

## Anatomy of a Skill

Every skill has three core components:

* **Frontmatter** — A YAML block at the top of the file containing the skill's `name` and `description`. The description is the primary triggering mechanism — it tells Claude when to use the skill.
* **Instructions** — The body of the skill: step-by-step guidance, rules, examples, and output formats that Claude follows when the skill is active.
* **Bundled resources** (optional) — Reference files, scripts, or assets that the skill can load as needed without bloating the main instruction file.

## Types of Skills

* **Individual** — Personal or fun; not intended for shared company use.
* **Team** — Useful for a specific team's workflow; encodes domain-specific knowledge or processes.
* **Enterprise** — Broadly useful across the entire organization; encodes company-wide standards or policies.

## Skills in This Space

This section contains documentation for the skills installed and maintained by this team. Each child page covers a specific skill — its purpose, how it triggers, and what it produces.
