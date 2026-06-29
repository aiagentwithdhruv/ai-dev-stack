---
type: dashboard
tags:
  - dashboard
  - crm
---

# Client Pipeline

> CRM powered by Obsidian. One note per client. Dataview pulls everything together.

---

## Leads
```dataview
TABLE channel, value, last_contact
FROM "02-Areas/Clients"
WHERE type = "client" AND status = "lead"
SORT last_contact DESC
```

## Proposals Sent
```dataview
TABLE channel, value, last_contact
FROM "02-Areas/Clients"
WHERE type = "client" AND status = "proposal"
SORT value DESC
```

## Active Clients
```dataview
TABLE channel, value, start_date
FROM "02-Areas/Clients"
WHERE type = "client" AND status = "active"
SORT value DESC
```

## Completed
```dataview
TABLE channel, value, start_date
FROM "02-Areas/Clients"
WHERE type = "client" AND status = "delivered"
SORT start_date DESC
```

---

## Add New Client

Use the **Client** template: `status`, `channel`, `value`, `currency`

Pipeline stages: `lead` → `proposal` → `active` → `delivered` → `archived`
