# Switch 4 — Screenshot Smoke

> **Status:** PROVISIONAL — designed, not yet validated across 2+ projects.
> **Category:** UI verification
> **Cost:** 30-60 seconds per UI task
> **Benefit:** moves visual verification one gate earlier; orchestrator reviews before human smoke

---

## The Rule

Any prompt-file that touches UI (adds a page, modifies a component, changes layout or routing)
MUST include this terminal step in Gate 3:

```
After restarting the dev server, capture a screenshot of the relevant page.
Include the screenshot path or data in the REPORT.
```

The orchestrator reviews the screenshot before telling the human to smoke the UI.

---

## Why

The current Gate 3 requires the specialist to open the browser and describe what they see.
But descriptions are unreliable — a specialist can write "renders correctly" while the
page is blank except for the nav bar, or while a button is present but in the wrong place.

A screenshot is objective. The orchestrator can see with their own eyes whether the
rendered state matches the spec before the human spends time testing.

This moves one quality gate from Gate 5 (human smoke) to Gate 4 (orchestrator smoke).
The human's time is spent on edge-case testing, not "does this page load at all."

---

## Implementation options

Three ways to capture a screenshot, ordered by setup cost:

### Option A — Computer-use MCP (cleanest)

If the orchestrator has computer-use access and the dev server is running locally:

```
# In Gate 3 of the prompt-file:
Take a screenshot of http://localhost:5173/{ROUTE} after restarting the dev server.
Attach the screenshot to the REPORT.
```

The orchestrator calls the screenshot tool directly. No extra setup.
This is the preferred option when computer-use MCP is available.

### Option B — Headless Playwright (scriptable, no MCP required)

```bash
# Install once per project
npm install --save-dev playwright
npx playwright install chromium

# Add to Gate 3 in prompt-file:
npx playwright screenshot --browser chromium http://localhost:5173/{ROUTE} /tmp/smoke-{PROMPT_CODE}.png
```

The specialist runs this as part of Gate 3. Screenshot path goes in the REPORT.
The orchestrator opens the file to review.

### Option C — macOS screencapture (manual, zero setup)

```bash
# In Gate 3 of the prompt-file:
open http://localhost:5173/{ROUTE}
sleep 3
screencapture -T 2 /tmp/smoke-{PROMPT_CODE}.png
```

Works on macOS without any dependencies. Captures whatever is frontmost after 2 seconds.
Fragile if other windows are in front, but reliable when the dev server is the only tab.

---

## What the orchestrator checks in the screenshot

1. Does the page load without a blank screen or error overlay?
2. Is the primary UI element visible and in the expected position?
3. Is the status, data, or label correct (to the degree visible without interaction)?

If any check fails: write a targeted hotfix prompt before handing to the human.

---

## Tradeoffs

- Adds 30-60 seconds to Gate 3 for UI tasks. Worth it.
- Option B requires Playwright setup once per project. Small upfront cost.
- Screenshots do not catch interaction bugs (click → response). Those still go to Gate 5.
- This switch is most valuable in the first 2 weeks of a new UI module, when
  blank-page and routing bugs are most common.
