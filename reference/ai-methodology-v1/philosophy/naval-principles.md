# Naval Principles for AI-Assisted Development

These principles come from production scars, not theory. Each one was learned the hard way — through lost commits, broken deploys, wasted hours, and trust rebuilt. Read them as operating rules, not inspiration.

---

## On Knowledge

**"You don't need to know everything. You need to know enough to choose, and enough to recover when it breaks."**

The architect who knows every line of code is a bottleneck. The architect who can read a stack trace, understand the failure mode, and write the correction prompt — that person scales. Breadth to choose. Depth to recover. Everything else is noise. When your enterprise product hits a production incident at 2am, you don't need theory. You need the 3 questions: what changed, what broke, how do we revert safely.

---

## On Complexity

**"Complexity hides failure. Simplicity surfaces it."**

A system with 11 moving parts fails silently. A system with 3 fails loudly. Loud failures are a gift — you catch them in development, not in the client's hands. Every time you're tempted to add another abstraction, another middleware layer, another config option: ask what it's hiding. Production discipline means stripping complexity until the system screams clearly when something goes wrong. Silent failures compound. Loud ones teach.

---

## On Building Teams

**"A team that needs you to move is an employee. A team that moves on its own is a business."**

If every decision routes through you, you haven't built a team — you've built a dependency. The goal is agents (human or AI) who understand the context well enough to move in the right direction without a hand on their back. They have the spec. They have the rules. They have the constraints. They execute. You review. When something breaks they flag it — they don't wait. That's the difference between a person and a role, between a tool and a system.

---

## On Position

**"A question is not a correction. Push-back is not a verdict. Hold the line until the data changes."**

When a stakeholder asks "why are you doing it this way?" — that's not an instruction to change. It's a request for clarity. Answer the question. If the reasoning holds, the position holds. If the new information changes the calculation, update. But don't flip on tone alone. Sycophancy is invisible to the person doing it — it feels like responsiveness. What it actually costs: the person you're working with can no longer trust that your stated position is your real position. That trust, once lost, is expensive to rebuild.

---

## On Knowledge Tools

**"Obsidian is passive. Prompt-files are active."**

A note-taking system stores what you know. A prompt-file system deploys what you know. Notes sit in a vault waiting to be consulted. Prompt files sit in a directory waiting to be executed. The difference is agency. A knowledge base that never gets turned into action is an archive. Build prompt files — discrete, self-contained units of instruction that an agent can pick up cold and execute. That's the file that earns its place in the repository.

---

## On Generators

**"The generator is never the problem. The generator's input is."**

Code generators, document generators, prompt generators — they do exactly what you tell them. The bug is never in the generator. It's in the schema you fed it, the field names you assumed, the spec you didn't cross-check against the actual database. When the output is wrong, resist the reflex to fix the generator. Trace back to the input. In practice: before blaming the template, grep the real table. Before blaming the prompt, read the actual API response. The generator faithfully reproduced your mistake.

---

## On Constraints

**"Constrain the environment, not the intelligence."**

An agent given total freedom will drift. An agent given a well-constrained environment — explicit file paths, explicit git branches, explicit scope lock, explicit DO-NOT sections — will execute precisely. The instinct is to hire (or build) smarter agents. The leverage is in tighter environments. Intelligence is abundant. Clear constraints are scarce. When an agent goes off-spec, the first question is: did the prompt tell it what NOT to touch? Usually the answer is no.

---

## Crystallised Principle

The principles above share one root: **production discipline is clarity enforced before problems arrive, not explanations written after they hit.**

Know enough to recover. Simplify until failures surface. Build teams that move without you. Hold position under pressure. Make knowledge executable. Trace problems to inputs. Constrain environments, not intelligence.

These aren't ideals. They're the minimum viable operating conditions for shipping consistently.
