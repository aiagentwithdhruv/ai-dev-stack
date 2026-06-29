# Skill Schema Section Convention

> A small, typed `## Schema` block at the end of every `SKILL.md` makes skills **programmatically
> discoverable and composable** — a CLI/MCP can list them, search them, validate that one skill's
> outputs satisfy another's inputs, and route an intent to the right skill. It also forces you to be
> explicit about credentials and cost up front.

Add this section to each skill. Keep types to a small closed set so tooling can reason about them.

```markdown
## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | What to search for |
| `limit` | integer | No | Max results (default 20) |
| `source_file` | file_path | No | Optional input file |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `results` | array | List of result objects |
| `report_path` | file_path | Where the written report landed |

### Credentials
| Name | Source |
|------|--------|
| `SOME_API_KEY` | .env |

### Composable With
Skills that chain well after this one: `classify-records`, `draft-outreach`

### Cost
Free  ·  or "$X per run"  ·  or "N API credits"
```

## Type vocabulary

Use only these so tooling stays simple and validation is mechanical:

- `string`, `integer`, `boolean`
- `array`, `object`
- `file_path`

## Credentials: name the variable, never the value

The Credentials table lists **env-var names and where they come from** (`.env`, a secrets manager, a
dashboard) — never the secret itself. This keeps skills shareable: a public skill advertises *that* it
needs `SOME_API_KEY` without leaking one. Secrets stay in the environment / a secrets manager.

## Why this powers composition

Because Inputs and Outputs are typed, a chain `A → B` is **valid when every required Input of B is
satisfied by an Output of A** (or by a constant the caller supplies). `Composable With` is the
human-curated hint; the typed tables are the machine-checkable contract. A `doctor`/`verify` command can
flag any skill missing a Schema section or any chain whose types don't line up.
