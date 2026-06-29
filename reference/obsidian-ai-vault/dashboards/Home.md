---
type: dashboard
tags:
  - dashboard
  - home
---

# Knowledge Vault — Home

> One vault. Everything linked. Claude Code reads it all.

---

## Quick Navigation

| Section | Link |
|---------|------|
| Inbox | [[00-Inbox]] |
| Active Projects | [[01-Projects]] |
| Client CRM | [[Client Pipeline]] |
| Skills Library | [[Skills Index]] |
| Revenue | [[02-Areas/Revenue]] |
| Memory | [[Memory]] |
| Context | [[Context]] |

---

## Active Clients

```dataview
TABLE status, channel, value
FROM "02-Areas/Clients"
WHERE type = "client" AND status != "archived"
SORT value DESC
```

---

## Active Projects

```dataview
TABLE status, priority, deadline
FROM "01-Projects"
WHERE type = "project" AND status = "active"
SORT priority ASC
```

---

## Recent Notes

```dataview
TABLE file.mtime AS "Modified"
FROM ""
WHERE file.name != "Home"
SORT file.mtime DESC
LIMIT 10
```

---

## Today's Tasks

```tasks
not done
due today
```

---

*Your AI thinks with your entire knowledge base.*
