# Workflow: [Name]

## Objective
<!-- One sentence: what does this workflow accomplish? -->

## Inputs
<!-- What the user must provide -->
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | yes | The main topic to research |
| `output_format` | string | no | "html" or "markdown" (default: markdown) |

## Tools Used
<!-- Which tools from tools/ this workflow calls, in order -->
1. `tools/research_web.py` — gather information
2. `tools/generate_content.py` — create the output
3. `tools/deliver.py` — send to destination

## Steps

### Step 1: Research
```bash
python tools/research_web.py --query "{topic}" --output .tmp/research.json
```
- Expected output: `.tmp/research.json` with structured research data
- On failure: check API key, retry with a simplified query

### Step 2: Generate
```bash
python tools/generate_content.py --input .tmp/research.json --format {output_format} --output .tmp/output.{ext}
```
- Expected output: `.tmp/output.md` or `.tmp/output.html`
- On failure: check research.json has data, retry with smaller context

### Step 3: Deliver
```bash
python tools/deliver.py --input .tmp/output.{ext} --destination {destination}
```
- Expected output: cloud URL or confirmation
- On failure: save locally, inform the user

## Outputs
| Output | Type | Location |
|--------|------|----------|
| Final content | markdown/html | Cloud destination or `.tmp/` |
| Research data | json | `.tmp/research.json` |

## Error Handling
| Error | Cause | Fix |
|-------|-------|-----|
| API timeout | Rate limit or network | Wait, retry with backoff |
| Empty research | Bad query or blocked site | Simplify query, try alternate source |
| Auth failure | Expired token | Re-run the auth flow |

## Cost Estimate
- Research: ~$0.0X per query
- LLM generation: ~$0.0X per run
- Total: ~$0.0X per run

## History
<!-- Updated when the agent learns something -->
- Created: YYYY-MM-DD
