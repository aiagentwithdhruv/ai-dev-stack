# AI Coding Rules — Content Distribution Kit

> One file. Everything you need to launch ai-dev-stack across all platforms.

---

## 1. Hand-Drawn Diagram Prompt (Gemini)

Copy-paste this into Google Gemini to generate the hero image.

```
Hand-drawn whiteboard infographic on white lined notebook paper, sitting on a natural wooden desk surface visible at the edges. Black marker lines, cyan (#00D4FF) marker highlights, yellow highlighter on key numbers. Real marker ink texture, natural paper grain. Photo of a real whiteboard after a brainstorming session. 16:9 aspect ratio.

=== TOP TITLE BAR ===
Hand-written bold title: "AI Coding Rules"
Below it: "15 Rules + 9 Templates = Your AI Writes Like a Senior Engineer" with yellow highlight on "Senior Engineer"
Cyan marker underline stroke under the main title.
TOP-RIGHT: "AiwithDhruv" in bold cyan marker inside a hand-drawn rounded rectangle badge. Smaller text below: "youtube | github | linkedin"

=== LEFT COLUMN — "What You Get" ===
Header: "What You Get" inside a hand-drawn box

Numbered checklist with small hand-drawn icons next to each:
[x] "15 Engineering Rules" — small gear icon
[x] "9 Doc Templates" — small document icon
[x] "Cursor + Claude Code" — small terminal icon
[x] "One-Line Install" — small download arrow icon
[x] "Compose Your Own" — small puzzle piece icon
[x] "MIT License — Free" — small heart icon

Each checkbox drawn with cyan marker tick marks.

=== CENTER — "The 15 Rules" (largest section) ===
Header: "The 15 Rules" with a circle around it

Flowchart showing a vertical stack of hand-drawn rounded boxes, grouped and connected by bracket arrows:

GROUP 1 — "Foundation":
[00] "Global Architect" — "think architect first"
[10] "Backend FastAPI" — "thin routes, fat services"
[20] "Frontend Next.js" — "TypeScript, small components"

GROUP 2 — "Data Layer":
[30] "Database PostgreSQL" — "migrations, indexes"
[35] "API Contracts" — "versioned, typed schemas"
[40] "Cache Redis" — "intentional TTLs"

GROUP 3 — "AI/ML":
[45] "Environment Config" — "validate at startup"
[50] "RAG System" — "separate ingestion from gen"
[55] "Data Versioning" — "named checkpoints"
[60] "AI Agents" — "tool schemas, validated outputs"

GROUP 4 — "Ship It":
[70] "Security" — "no secrets in code"
[80] "Testing" — "deterministic tests"
[85] "Observability" — "structured errors"
[90] "DevOps" — "Docker, AWS, Vercel, VPS"
[99] "Response Style" — "production code only"

Hand-drawn arrows connecting each group downward. Small cyan dots between groups.

=== FLASH CARDS scattered around like sticky notes, tilted at slight angles ===

Yellow sticky note (tilted, near top-right):
"Works With"
"Cursor (.mdc files)"
"Claude Code (CLAUDE.md)"
Small terminal cursor doodle

Light blue sticky note (tilted, near center-right):
"9 Doc Templates"
"PRD + Architecture + API"
"DB Schema + Deployment"
Small document stack doodle

Pink sticky note (tilted, near bottom-left):
"Compose.sh"
"Pick only rules you need"
"./compose.sh 00 10 30 70"
Small gear doodle

Light green sticky note (tilted, near center-left):
"One Command Install"
"curl ... | bash"
"Works in 30 seconds"
Small rocket doodle

Light purple sticky note (tilted, near bottom-center):
"Production Tested"
"30+ Projects"
"AI Agents, RAG, SaaS"
Small checkmark doodle

Some flash cards have paper clip or tape marks holding them on.

=== RIGHT COLUMN — "Before vs After" ===
Header: "Before vs After"

Split comparison drawn as two browser windows stacked:

TOP browser window labeled "Before (no rules)":
- Messy code lines with red X marks
- "secrets in code" with strikethrough
- "fat controllers" with strikethrough
- "no tests" with strikethrough
- Sad face doodle

BOTTOM browser window labeled "After (with rules)":
- Clean code lines with green checkmarks
- "env vars validated"
- "clean architecture"
- "tested + observable"
- Star doodle

=== BOTTOM LEFT — How It Works ===
Architecture diagram with 3 boxes connected by arrows:

Box 1: "rules/*.mdc" with Cursor logo sketch → "AI reads rules"
Box 2: "CLAUDE.md" with Claude logo sketch → "AI follows patterns"
Box 3: "docs/" with document icon → "AI knows your project"

Arrow from all 3 pointing to a final box: "Production-Grade Code" with a star

=== BOTTOM CENTER — Stats Row ===
Three items in a row, each circled with yellow highlight:
"15 Rules"    "9 Templates"    "30+ Projects Tested"
Small star doodles around the stats

=== BOTTOM RIGHT — Author + Branding ===
"AiwithDhruv" with cyan lightning bolt
"@aiwithdhruv" and "github.com/aiagentwithdhruv"
"AD" monogram in a hand-drawn circle

=== AMBIENT DETAILS ===
- Coffee ring stain near bottom-left (subtle)
- Paper clips on 1-2 flash cards
- Tape marks on corners of some sticky notes
- Blue pen lying on the desk
- Small doodle arrows and stars in empty spaces
- Wooden desk texture at all edges
- Faint "AiwithDhruv" watermark diagonally across center in light grey

=== STYLE — CRITICAL ===
- Real black marker on white paper — authentic hand-drawn feel
- Slightly imperfect handwriting but always readable
- Cyan for headers, connections, branding
- Yellow highlighter for numbers and stats
- Pastel colored sticky notes at slight angles
- Small recognizable tech logos hand-drawn next to every tool
- Everything hand-drawn — NO computer fonts
- Clean enough to read on a phone screen
```

**4:5 version (LinkedIn/Instagram):** Change first line to `4:5 aspect ratio` and remove the "Before vs After" right column to keep it readable on mobile.

---

## 2. LinkedIn Post

```
I open-sourced the exact system that makes my AI write production-grade code.

Not prompts. Not hacks. Engineering rules.

Here's what happened:

I was building across 30+ projects — AI agents, RAG systems, SaaS products, client work.

Every time I started a new project, my AI would:
- Hardcode secrets
- Put business logic in routes
- Skip migrations
- Write toy code instead of production code

So I codified 15 engineering rules that fix this permanently.

Now when I open any project, my AI already thinks like a senior engineer.

What's inside:

00 — Global Architect (clean architecture, separation of concerns)
10 — Backend FastAPI (thin routes, services, repositories)
20 — Frontend Next.js (TypeScript, small components)
30 — Database PostgreSQL (migrations, indexes, constraints)
35 — API Contracts (versioned, typed, consistent errors)
40 — Cache Redis (intentional TTLs, wrapped access)
50 — RAG System (separate ingestion from generation)
60 — AI Agents (tool schemas, validated outputs)
70 — Security (no hardcoded secrets, prompt injection resistance)
80 — Testing (deterministic tests, mocked externals)
90 — DevOps (Docker, AWS, Vercel, VPS, CI/CD)
+ 4 more rules

Also included:
- 9 project doc templates (PRD, Architecture, API Spec, DB Schema, Deployment, and more)
- Works with both Cursor and Claude Code
- One-line install
- Compose script to pick only the rules you need

This isn't theory. It's battle-tested across 30+ real projects.

Install in 10 seconds:
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

GitHub: github.com/aiagentwithdhruv/ai-dev-stack

Your AI is only as good as the rules you give it.

---
Built with Claude Code. Open source. MIT license.
```

---

## 3. LinkedIn Comment-Style Post (Engagement)

```
Hot take: Most developers using AI coding tools are getting junior-level output from a senior-level model.

The problem isn't the AI.
The problem is you gave it zero engineering standards.

No architecture rules.
No security rules.
No testing expectations.
No deployment patterns.

You're asking a principal engineer to code like an intern — because you never told it otherwise.

I fixed this with 15 rules that load automatically into Cursor and Claude Code.

Now my AI:
- Never hardcodes secrets
- Always uses clean architecture
- Writes migrations, not raw SQL
- Tests critical paths
- Deploys to AWS/Vercel/VPS correctly

The difference between "AI-assisted coding" and "AI-native engineering" is rules.

Would you hire a senior engineer and give them zero context about your codebase?

Then why do that to your AI?

Link in comments.
```

**Comment to post immediately after:**
```
Here's the repo (free, MIT license):
github.com/aiagentwithdhruv/ai-dev-stack

15 rules + 9 doc templates.
Works with Cursor (.mdc) and Claude Code (CLAUDE.md).
One-line install.

Star it if it saves you time.
```

---

## 4. Twitter/X Posts (X Premium — 2 Month Window)

> **X Premium perks we're using:** 4,000 char tweets, bold/italic formatting (Unicode), blue checkmark, boosted reply ranking, edit button (30 min), analytics, longer video uploads (up to 3 hrs).
>
> **Strategy:** Mix long-form value tweets (use the full 4K chars) with punchy hooks. Premium tweets rank higher in replies — comment on AI/dev creator tweets with substance to drive profile visits. Post 1-2x daily for the full 2 months.
>
> **Formatting:** X doesn't support markdown. Use Unicode bold (𝗯𝗼𝗹𝗱) and italic (𝘪𝘵𝘢𝘭𝘪𝘤) characters. Generate at: lingojam.com/BoldTextGenerator

---

### Tweet 1 — Launch Tweet (Long-Form, ~2000 chars)
```
I open-sourced the exact system that makes my AI write production-grade code.

Not prompts. Not "tips." 𝟭𝟱 𝗲𝗻𝗴𝗶𝗻𝗲𝗲𝗿𝗶𝗻𝗴 𝗿𝘂𝗹𝗲𝘀 that load into Cursor and Claude Code automatically.

Here's the problem:

You open Cursor or Claude Code, ask it to build something, and it writes:
→ Secrets hardcoded in the codebase
→ Business logic stuffed in route handlers
→ No migrations, just raw SQL
→ Zero tests
→ "It works on my machine" deployment

You're getting junior-level output from a senior-level model.

𝗧𝗵𝗲 𝗳𝗶𝘅 𝗶𝘀𝗻'𝘁 𝗯𝗲𝘁𝘁𝗲𝗿 𝗽𝗿𝗼𝗺𝗽𝘁𝘀. It's engineering standards.

I built 15 rules across 30+ real projects (AI agents, RAG systems, SaaS, client work) and packaged them as:

• Cursor rules (.mdc files) — AI reads them automatically
• Claude Code rules (CLAUDE.md) — same rules, different format
• Compose script — pick only the rules you need

𝗧𝗵𝗲 𝟭𝟱 𝗿𝘂𝗹𝗲𝘀:

00 Global Architect — clean architecture, separation of concerns
10 Backend FastAPI — thin routes, fat services
20 Frontend Next.js — TypeScript, small components
30 Database PostgreSQL — migrations, indexes, constraints
35 API Contracts — versioned, typed, consistent errors
40 Cache Redis — intentional TTLs, wrapped access
45 Environment Config — validate at startup
50 RAG System — separate ingestion from generation
55 Data Versioning — named checkpoints
60 AI Agents — tool schemas, validated outputs
70 Security — no secrets in code, prompt injection resistance
80 Testing — deterministic tests, mocked externals
85 Observability — structured errors, audit trails
90 DevOps — Docker, AWS, Vercel, VPS, CI/CD
99 Response Style — production code, not tutorials

+ 𝟵 𝗱𝗼𝗰 𝘁𝗲𝗺𝗽𝗹𝗮𝘁𝗲𝘀: PRD, Architecture, API Spec, DB Schema, Deployment, Skills, Agents, Loadout, MCP Server

Install in 10 seconds:
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

Or compose your own:
./compose.sh 00 10 30 70 80 99

Free. MIT license. Star it if it saves you time.

github.com/aiagentwithdhruv/ai-dev-stack

#CursorIDE #ClaudeCode #AIEngineering #OpenSource #CodingRules #DevTools #AI #SoftwareEngineering #WebDev #Programming
```

---

### Tweet 2 — Hot Take (Punchy, ~600 chars)
```
Your AI writes junior code because you gave it zero engineering standards.

No architecture rules.
No security rules.
No testing expectations.
No deployment patterns.

You're asking a principal engineer to code like an intern — because you never told it otherwise.

I codified 15 rules that load into Cursor + Claude Code automatically.

Now my AI never hardcodes secrets, always uses clean architecture, writes migrations instead of raw SQL, and deploys correctly.

The difference between "AI-assisted coding" and "AI-native engineering" is rules.

github.com/aiagentwithdhruv/ai-dev-stack

#CursorIDE #ClaudeCode #AIcoding #DevTools #OpenSource #Programming #BuildInPublic
```

---

### Tweet 3 — Before/After Proof (Long-Form, ~1500 chars)
```
𝗕𝗲𝗳𝗼𝗿𝗲 I added engineering rules to my AI:

❌ API keys hardcoded in source files
❌ 500-line route handlers with business logic
❌ Direct SQL queries, no migrations
❌ "Tests? I'll add them later"
❌ Manual deployment via SSH
❌ Same mistakes in every new project

𝗔𝗳𝘁𝗲𝗿 15 rules loaded into Cursor + Claude Code:

✅ Environment variables validated at startup
✅ Thin routes → services → repositories
✅ Alembic migrations, typed models, indexes
✅ Deterministic tests with mocked externals
✅ Docker + CI/CD + one-command deploy
✅ Every project starts at senior-engineer baseline

The rules aren't complicated. They're just 𝘤𝘰𝘥𝘪𝘧𝘪𝘦𝘥 𝘴𝘦𝘯𝘪𝘰𝘳 𝘦𝘯𝘨𝘪𝘯𝘦𝘦𝘳 𝘩𝘢𝘣𝘪𝘵𝘴.

Most developers using Cursor or Claude Code don't realize:
→ The AI is capable of writing production code
→ It just doesn't know YOUR standards
→ One config file changes everything

This took me 30+ projects to figure out. Took 10 seconds to install.

github.com/aiagentwithdhruv/ai-dev-stack

Free. Open source. MIT license.

#AIcoding #CursorIDE #ClaudeCode #SoftwareEngineering #DevTools #OpenSource #CodeQuality #BuildInPublic #Programming #AI
```

---

### Tweet 4 — Thread: "How I Set Up Every New Project" (5 tweets)

**Thread tweet 1/5:**
```
How I set up every new project so my AI writes production code from day one.

A thread 🧵

(This system is free and open source — link at the end)

#CursorIDE #ClaudeCode #AIEngineering #OpenSource #DevTools
```

**Thread tweet 2/5:**
```
𝗦𝘁𝗲𝗽 𝟭: Install the rules (10 seconds)

curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

This drops 15 engineering rules into your project as:
• .cursor/rules/*.mdc (for Cursor)
• claude/CLAUDE.md (for Claude Code)

Your AI reads them automatically. Zero config.
```

**Thread tweet 3/5:**
```
𝗦𝘁𝗲𝗽 𝟮: Compose for your stack

Don't need all 15? Pick only what matters:

./compose.sh 00 10 30 70 80 99    → Backend only
./compose.sh 00 20 70 80 99        → Frontend only
./compose.sh 00 50 55 60 70 99     → AI/ML only

The compose script builds a custom CLAUDE.md with just your rules.

This is like .gitignore but for engineering standards.
```

**Thread tweet 4/5:**
```
𝗦𝘁𝗲𝗽 𝟯: Add project docs (optional but powerful)

9 templates included:
• PRD — what you're building
• Architecture — how it's structured
• API Spec — endpoint contracts
• DB Schema — models and relations
• Deployment — where and how it ships

Your AI reads these too. Now it doesn't just follow rules — it understands 𝘺𝘰𝘶𝘳 𝘱𝘳𝘰𝘫𝘦𝘤𝘵.
```

**Thread tweet 5/5:**
```
𝗥𝗲𝘀𝘂𝗹𝘁: Every project starts at senior-engineer baseline.

No more:
• Re-teaching the AI your patterns
• Fixing the same mistakes
• Writing prompts to compensate for bad defaults

15 rules. 9 templates. One install.

Tested across 30+ projects — AI agents, RAG systems, SaaS, client work.

github.com/aiagentwithdhruv/ai-dev-stack

Free. MIT. Star it if it helps. ⭐

#CursorIDE #ClaudeCode #AIcoding #OpenSource #DevTools #SoftwareEngineering #BuildInPublic #AI #Programming #WebDev
```

---

### Tweet 5 — Engagement Bait (Short, Reply-Optimized)
```
What's the first thing you configure when starting a new AI coding project?

I load 15 engineering rules into Cursor/Claude Code before writing a single line.

My AI never hardcodes secrets, always writes migrations, always tests critical paths.

Most devs skip this step. That's why their AI writes toy code.

#AIcoding #CursorIDE #ClaudeCode #DevTools #Programming #BuildInPublic #SoftwareEngineering
```

---

### Tweet 6 — Quote Tweet / Reply Template (For AI Dev Conversations)
```
This is exactly why I open-sourced 15 engineering rules for Cursor + Claude Code.

The AI is smart enough. The problem is we give it zero standards.

One config file = your AI thinks like a senior engineer on every project.

github.com/aiagentwithdhruv/ai-dev-stack

#CursorIDE #ClaudeCode #AIcoding #OpenSource #DevTools
```

---

### Hashtag Strategy

> **Core tags (use on every tweet):** `#CursorIDE` `#ClaudeCode` `#AIcoding` `#OpenSource` `#DevTools`
>
> **Rotating tags (mix 2-3 per tweet):** `#BuildInPublic` `#SoftwareEngineering` `#Programming` `#WebDev` `#AI` `#CodeQuality` `#AIEngineering` `#IndieHacker`
>
> **Trend-jack when relevant:** `#Cursor` `#Claude` `#Anthropic` `#AItools` `#100DaysOfCode` `#CodeNewbie`
>
> **Rule:** 5-10 tags per tweet. Put them at the end, separated by one blank line from the content. Premium long-form tweets can handle more tags without looking spammy.

---

### X Premium 2-Month Posting Calendar

| Week | Day | Tweet | Type | Goal |
|------|-----|-------|------|------|
| 1 | Mon | Tweet 1 (Launch) | Long-form value | Announce + drive stars |
| 1 | Wed | Tweet 2 (Hot take) | Punchy hook | Engagement + profile visits |
| 1 | Fri | Tweet 4 (Thread) | 5-tweet thread | Deep value + saves |
| 2 | Tue | Tweet 3 (Before/After) | Long-form proof | Social proof |
| 2 | Thu | Tweet 5 (Engagement) | Question hook | Replies + reach |
| 2 | Sat | Tweet 6 (QT/Reply) | Reply to trending AI tweet | Piggyback reach |
| 3-8 | Ongoing | Reply to AI/dev creators | Short value replies | Profile visits via boosted ranking |
| 3-8 | 2x/week | New variations of above | Mix long + short | Consistent presence |

**Premium tactics for the 2-month window:**
- 𝗕𝗼𝗼𝘀𝘁𝗲𝗱 𝗿𝗲𝗽𝗹𝗶𝗲𝘀: Reply to big AI creators (Fireship, ThePrimeagen, LevelUpTuts, AI Jason, Matt Shumer) with substance — Premium replies rank higher
- 𝗘𝗱𝗶𝘁 𝗯𝘂𝘁𝘁𝗼𝗻: Post, monitor for 15 min, edit typos or add link if engagement is high
- 𝗔𝗻𝗮𝗹𝘆𝘁𝗶𝗰𝘀: Check which tweet format gets most saves/bookmarks — double down on that format
- 𝗟𝗼𝗻𝗴-𝗳𝗼𝗿𝗺: Use full 4K chars at least 2x/week — long tweets get more time-on-tweet = more impressions
- 𝗕𝗹𝘂𝗲 𝗰𝗵𝗲𝗰𝗸: Adds credibility to every reply and quote tweet — use it to build authority fast

---

## 5. Short Video #1 — "WHAT" (The Problem + Solution)

### Concept
Screen recording: Open a fresh project, show AI writing bad code (secrets hardcoded, fat controllers, no tests). Then drop in ai-dev-stack, show the SAME prompt producing clean code. Before/after split.

### Title Options
1. `I Made My AI Write Like a Senior Engineer (15 Rules)`
2. `Your AI Writes Bad Code. Here's the Fix.`
3. `15 Rules That Turned My AI Into a Principal Architect`

### Description
```
Most developers using Cursor or Claude Code are getting junior-level output from senior-level AI.

The fix? Engineering rules that load automatically.

I open-sourced 15 production-grade rules + 9 doc templates that make your AI think like a principal architect.

Works with Cursor (.mdc files) and Claude Code (CLAUDE.md).

Install in 10 seconds:
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

GitHub: https://github.com/aiagentwithdhruv/ai-dev-stack

What's inside:
- 15 engineering rules (architecture, backend, frontend, database, security, testing, DevOps)
- 9 doc templates (PRD, Architecture, API Spec, DB Schema, Deployment)
- Compose script to pick only rules you need
- MIT License — completely free

Built with Claude Code. Tested across 30+ real projects.

#cursor #claudecode #aiengineering #programming #webdev
```

### Tags
```
ai coding, cursor rules, claude code, ai engineering, coding rules, clean architecture, fastapi, nextjs, postgresql, devops, ai agents, production code, open source, cursor ide, claude code cli, ai programming, software engineering, coding best practices
```

---

## 6. Short Video #2 — "HOW" (Install + Customize)

### Concept
Terminal recording: Run the install command, show files appearing. Open compose.sh, build a custom CLAUDE.md for a backend-only project. Open Cursor, show rules auto-loading. 60-90 seconds, fast cuts.

### Title Options
1. `Set Up AI Coding Rules in 30 Seconds (Cursor + Claude Code)`
2. `One Command. Your AI Becomes a Senior Engineer.`
3. `How I Configure Every New Project for AI (15 Rules)`

### Description
```
How to set up ai-dev-stack in any project — takes 30 seconds.

Step 1: Run the install command
Step 2: Customize with compose.sh (pick only rules you need)
Step 3: Your AI now follows production engineering standards

Works with both Cursor and Claude Code. Zero conflict.

Install:
curl -fsSL https://raw.githubusercontent.com/aiagentwithdhruv/ai-dev-stack/main/install.sh | bash

Compose examples:
./compose.sh 00 10 30 70 80 99    # Backend only
./compose.sh 00 20 70 80 99        # Frontend only
./compose.sh 00 50 55 60 70 99     # AI/ML only

GitHub: https://github.com/aiagentwithdhruv/ai-dev-stack

15 rules + 9 doc templates. Free. MIT license.

#cursor #claudecode #aitools #programming #devtools
```

### Tags
```
cursor setup, claude code setup, ai coding rules, cursor rules, claude code rules, ai tools, developer tools, coding setup, project setup, clean code, ai programming tutorial, cursor tutorial, claude code tutorial
```

---

## 7. Cinematic Thumbnail Prompts (Dhruv's Style)

### Thumbnail A — Pipeline Flow (Blue Metallic) — BEST FOR YOUTUBE
```
Photorealistic DSLR-quality photo. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, sitting at a natural wooden desk working on a MacBook Pro. The laptop screen shows a dark terminal with green text: "install.sh running... 15 rules loaded". Above the laptop, a holographic pipeline showing: "Rules → AI Reads → Production Code" with green checkmarks on each step. Glowing cyan connection lines between stages. Each stage rendered as a frosted glass card — first card shows ".mdc" file icon, second shows Cursor + Claude Code logos, third shows a clean code output with green checkmarks. Floating on the LEFT side: vertical badge-style labels stacked neatly — "Architecture", "Security", "Testing", "DevOps", "API Contracts" — each with a small cyan icon. On the RIGHT: a frosted glass panel with teal and gunmetal silver-blue neon glow border showing a before/after split — messy code with red X on top, clean code with green check on bottom. Dark moody room with warm ambient light, bookshelf with plants softly blurred in background. Natural skin tones, warm room lighting with teal and metallic silver-blue neon accents only from the floating panels. Clean composition with breathing room between elements. Photorealistic, 8K, sharp focus, shallow depth of field, DSLR quality, cinematic color grading, 16:9 YouTube thumbnail ratio.
```

**Text overlay:** `15 RULES — Your AI Writes Like a SENIOR ENGINEER`
**Highlight:** "15 RULES" in yellow, "SENIOR ENGINEER" in cyan

---

### Thumbnail B — Holographic Command Center (Blue Metallic) — LINKEDIN 4:5
```
Cinematic portrait, dark moody workspace. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, arms crossed with confident smirk. Behind him, a massive holographic screen showing "AI CODING RULES" in electric cyan text. Floating around him in orbital rings: frosted glass cards each containing a rule icon — a gear (Architecture), a shield (Security), a flask (Testing), a rocket (Deploy), a database cylinder (PostgreSQL), a lock (API Contracts). Each card has a subtle teal neon edge glow. Brushed aluminum ring connecting the orbiting cards. Holographic connection lines between related rules. MacBook Pro on the natural wooden desk showing clean terminal output. Small floating text badges: "Cursor", "Claude Code", "15 Rules", "9 Templates". Dark navy background, ice blue neon rim lighting from behind, volumetric fog between the floating cards, frosted glassmorphism panels at multiple depths. Natural skin tones, warm face lighting from the holographic glow. 8K, sharp focus, hyperrealistic, Unreal Engine 5 lighting, 4:5 ratio.
```

**Text overlay:** `Your AI = Senior Engineer`
**Highlight:** "Senior Engineer" in cyan

---

### Thumbnail C — Before/After Split (Mixed) — HIGH ENGAGEMENT
```
Split image, dramatic cinematic still. LEFT SIDE (warm red/orange tint, stressed): Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, head in hands, stressed. MacBook Pro showing messy code with red error highlights. Floating red warning icons — "SECRETS IN CODE", "NO TESTS", "FAT CONTROLLERS". Chaotic multiple browser tabs open. RIGHT SIDE (cool teal tint, calm): Same developer, confident smile, arms relaxed. MacBook Pro showing clean terminal with green checkmarks. Floating teal frosted glass badges — "Clean Architecture", "Typed APIs", "Auto-Tests", "Secure Deploy". Dramatic frosted glass dividing line in center with bright white neon glow, cracking like glass shattering. Natural wooden desk continuous across both sides. Dark moody room. Natural skin tones on both sides. Photorealistic, 8K, sharp focus, cinematic color grading, dramatic lighting, 16:9 YouTube thumbnail ratio.
```

**Text overlay:** `BEFORE vs AFTER — 15 Rules Changed Everything`
**Highlight:** "BEFORE" in red, "AFTER" in teal, "15 Rules" in yellow

---

### Thumbnail D — Ghost Copies (Purple Neon) — AUTOMATION ANGLE
```
Cinematic movie still, dark moody workspace. Young Indian male developer with short hair, trimmed beard, and glasses, wearing a plain black t-shirt, sleeping peacefully at natural wooden desk with head resting on arms. MacBook Pro open showing terminal with green text "install.sh complete — 15 rules active". Behind him, 3 translucent purple ghost copies of himself wide awake and working simultaneously — one ghost typing rules into Cursor IDE, one ghost reviewing code in Claude Code terminal, one ghost deploying with a holographic "SHIP IT" button. Each ghost has a neon purple glow outline. Holographic glassmorphism panels floating near each ghost showing different rule categories: "Architecture", "Security + Testing", "DevOps + Deploy". Floating text badge near sleeping developer: "One command. Done." Volumetric fog between the ghosts and the sleeping developer. Dark navy background, purple and teal neon ambient lighting, dramatic rim lighting, cinematic shallow depth of field, 8K, sharp focus, hyperrealistic, Unreal Engine 5 lighting, 16:9 YouTube thumbnail ratio.
```

**Text overlay:** `I SLEEP. My AI Engineers.`
**Highlight:** "SLEEP" in purple, "Engineers" in cyan

---

### Which Thumbnail to Use Where

| Thumbnail | Best For | Platform |
|-----------|----------|----------|
| A — Pipeline Flow | Main YouTube video, GitHub README | 16:9 |
| B — Command Center | LinkedIn post, Instagram | 4:5 |
| C — Before/After | Engagement bait, Reels cover | 16:9 |
| D — Ghost Copies | Automation angle, Twitter | 16:9 |

---

## Quick Reference

| Asset | Platform | Status |
|-------|----------|--------|
| Hand-drawn diagram (16:9) | GitHub README hero | Generate in Gemini |
| Hand-drawn diagram (4:5) | LinkedIn, Instagram | Generate in Gemini |
| Thumbnail A — Pipeline Flow | YouTube main video | Generate in Ideogram/Midjourney |
| Thumbnail B — Command Center | LinkedIn post image | Generate in Ideogram/Midjourney |
| Thumbnail C — Before/After | Engagement posts, Reels cover | Generate in Ideogram/Midjourney |
| Thumbnail D — Ghost Copies | Automation angle, Twitter | Generate in Ideogram/Midjourney |
| LinkedIn post | LinkedIn | Copy-paste |
| LinkedIn comment post | LinkedIn | Copy-paste |
| X Premium Tweet 1 (Launch) | X/Twitter | Copy-paste, long-form |
| X Premium Tweet 2 (Hot take) | X/Twitter | Copy-paste, punchy |
| X Premium Tweet 3 (Before/After) | X/Twitter | Copy-paste, long-form |
| X Premium Tweet 4 (Thread, 5 tweets) | X/Twitter | Copy-paste |
| X Premium Tweet 5 (Engagement) | X/Twitter | Copy-paste, short |
| X Premium Tweet 6 (QT/Reply template) | X/Twitter | Copy-paste |
| Video 1 — What | YouTube Shorts, LinkedIn, Instagram Reels | Record |
| Video 2 — How | YouTube Shorts, LinkedIn, Instagram Reels | Record |

---

## Distribution Checklist

- [ ] Generate hand-drawn diagram in Gemini (16:9 + 4:5)
- [ ] Generate cinematic thumbnails (A for YouTube, B for LinkedIn)
- [ ] Update ai-dev-stack README with hand-drawn diagram as hero image
- [ ] Post LinkedIn main post with Thumbnail B (command center)
- [ ] Post LinkedIn comment post (next day or same day PM)
- [ ] X Premium: Post Tweet 1 (Launch, long-form) — Monday
- [ ] X Premium: Post Tweet 2 (Hot take) — Wednesday
- [ ] X Premium: Post Tweet 4 (5-tweet thread) — Friday
- [ ] X Premium: Post Tweet 3 (Before/After) — Week 2
- [ ] X Premium: Post Tweet 5 (Engagement bait) — Week 2
- [ ] X Premium: Reply to 3-5 AI creator tweets with Tweet 6 template
- [ ] X Premium: Check analytics after week 1, double down on best format
- [ ] Record Video 1 (What — before/after)
- [ ] Record Video 2 (How — install + customize)
- [ ] Upload shorts to YouTube, LinkedIn, Instagram
- [ ] Cross-post to relevant subreddits (r/cursor, r/ClaudeAI, r/programming)

---

*Generated by AiwithDhruv's content pipeline. Reuse this template for any future open-source launch.*
