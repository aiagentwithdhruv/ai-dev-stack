# Team Structure

Seven roles. One human. Each role has a clear boundary — what it owns, what it doesn't, when it activates. The boundary is the point. Specialists who drift outside their lane create the same problems that generalists create: no one knows who owns the mess.

---

## The 7 Roles

### 1. Orchestrator

**Owns:**
- Writing prompt files for every specialist task
- Reviewing all commits before the human sees them (Gate 4)
- Running smoke checks on new endpoints and features
- Release tagging on explicit human confirmation
- Session handoff documentation and state checkpoints
- Flagging spec drift before it accumulates

**Does not own:**
- Writing `.py`, `.tsx`, `.sql`, or any product code files
- Architectural decisions not surfaced to the human
- Declaring a feature complete without human browser confirmation
- Direct communication with specialists — always via prompt files

**Activates:** Every session. The orchestrator is always on.

---

### 2. Backend Specialist

**Owns:**
- API route implementation (FastAPI, REST, endpoint schemas)
- Database schema migrations (raw SQL, not generated tools)
- Service layer logic (business rules, data transformation)
- Pydantic models and validation schemas
- pytest test coverage for new endpoints
- Row-level security policy implementation

**Does not own:**
- Frontend components or pages
- CI/CD pipelines (that's DevOps)
- Release decisions

**Activates:** Any task touching `backend/`, `migrations/`, `tests/`. One session per active backend task.

---

### 3. Frontend Specialist

**Owns:**
- React/Next.js pages, components, and layout
- API integration (wiring backend responses to UI state)
- Vite build configuration
- CSS, Tailwind, responsive behaviour
- Empty states, loading states, error surfaces

**Does not own:**
- Backend API design or schema
- DevOps or build pipelines
- Content copy (that's Content Specialist)

**Activates:** Any task touching frontend source files. Coordinates with Backend Specialist on API contract — the orchestrator verifies the contract before dispatching either.

---

### 4. DevOps Specialist

**Owns:**
- Docker build and container configuration
- CI/CD pipeline setup and maintenance (GitHub Actions or equivalent)
- nginx configuration and reverse-proxy rules
- Environment variables and secrets management
- Container health checks and restart policies

**Does not own:**
- Application logic or business rules
- Database schema or migrations
- AWS infrastructure at production scale (that's Senior DevOps)

**Activates:** Deploy tasks, Docker issues, pipeline failures, environment configuration. On-demand, not continuous.

---

### 5. Content Specialist

**Owns:**
- Marketing copy, landing page text, email sequences
- Brand voice and editorial guidelines
- Documentation written for external audiences (clients, users)
- SEO content and metadata

**Does not own:**
- Technical documentation (owned by orchestrator or Backend)
- UI microcopy inside the product (owned by Frontend in coordination with orchestrator)
- Publishing decisions (the human approves before anything goes live)

**Activates:** When marketing or client-facing content needs to be written or reviewed. On-demand.

---

### 6. QA Specialist

**Owns:**
- Load testing and performance benchmarking
- Pre-launch test suites (Playwright, K6, or equivalent)
- Edge case identification and documentation
- Security surface review before major releases

**Does not own:**
- Routine feature testing (that's Gate 3 — the building specialist's responsibility)
- Daily smoke checks (that's Gate 4 — the orchestrator's responsibility)

**Activates:** Before major releases, before demos to clients, and when performance claims need verification. Not active on every sprint cycle.

---

### 7. Senior DevOps

**Owns:**
- AWS infrastructure (ECS, RDS, VPC, load balancers)
- Production incident response
- Cost optimisation and capacity planning
- Security hardening at the infrastructure layer

**Does not own:**
- Day-to-day Docker tasks (that's DevOps Specialist)
- Application code or business logic

**Activates:** Escalation only. Production incidents, major infrastructure changes, AWS deployment decisions. The DevOps Specialist handles everything else.

---

## Session Concurrency Limits

**Maximum 6 concurrent sessions across 2 active products.**

This is not an arbitrary number. It's the point at which the orchestrator's review bandwidth becomes the bottleneck. Beyond 6 sessions, commit reports stack up faster than they can be verified. Drift that would be caught at Gate 4 slips through because the orchestrator is reviewing something else.

The cost of exceeding this limit: drift compounds. A missed field name in session 7 becomes a broken integration in session 10. The debug cycle that follows takes longer than the combined time the extra sessions saved.

When load is high:
- Serialise, don't parallelise. Finish one pair of sessions before opening the next.
- Prioritise work that unblocks other sessions (API contracts, shared schema changes).
- The orchestrator decides the dispatch order, not the human.

---

## Role Activation Decision Tree

```
New task arrives:
  - Does it touch backend/ or migrations/?  → Backend Specialist
  - Does it touch frontend source files?    → Frontend Specialist
  - Does it touch infrastructure or CI/CD?  → DevOps Specialist
  - Is it client-facing content?            → Content Specialist
  - Is it pre-launch or load testing?       → QA Specialist
  - Is it a production AWS incident?        → Senior DevOps
  - Is it anything the orchestrator reviews? → Orchestrator (always active)
```

A single task can touch two roles (e.g., a feature that needs a new endpoint AND a new page). In that case, the orchestrator writes two prompt files — one for each specialist — sequences them correctly (backend first, then frontend), and verifies the contract between them before dispatching the second.

---

## Crystallised Principle

**Seven roles with clear boundaries scale. One person doing all seven roles has a ceiling.**

The ceiling is: how much can one person hold in their head at once? The roles are how you break past that ceiling without losing coherence. Each specialist knows its lane. The orchestrator holds the map.
