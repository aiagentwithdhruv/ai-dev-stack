---
type: dashboard
tags:
  - dashboard
  - skills
---

# Skills Library

> Check here before building anything new. Reuse > Rebuild.

---

## Your Skills

```dataview
TABLE category, version
FROM "03-Resources/Skills"
WHERE type = "skill"
SORT category ASC
```

---

## How to Add a Skill

1. Create a new note in `03-Resources/Skills/`
2. Use the **Skill** template
3. Fill in: inputs, outputs, steps, composable skills
4. Link it from relevant project notes

## Example Categories

| Category | Examples |
|----------|----------|
| **Lead Generation** | Web scraping, maps lookup, enrichment |
| **Email** | Cold outreach, auto-replies, sequences |
| **Content** | Video editing, thumbnails, research |
| **Infrastructure** | Deployment, webhooks, servers |
| **Browser Automation** | Scraping, form-fill, demos |
