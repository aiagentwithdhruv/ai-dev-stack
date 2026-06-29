---
type: dashboard
tags:
  - dashboard
  - projects
---

# Projects Map

> All projects at a glance. Each linked to its GitHub, skills used, and related clients.

---

## Active Projects

```dataview
TABLE status, priority, deadline, github
FROM "01-Projects"
WHERE type = "project" AND status = "active"
SORT priority ASC
```

## All Projects

```dataview
TABLE status, priority, started
FROM "01-Projects"
WHERE type = "project"
SORT status ASC
```

---

## How to Add a Project

1. Create a new note in `01-Projects/`
2. Use the **Project** template
3. Fill in: goals, architecture, key files, skills used
4. Link to relevant clients and skills
