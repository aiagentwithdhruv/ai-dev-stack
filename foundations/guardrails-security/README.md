# Guardrails & Security

> An LLM with tool access is an untrusted code path that takes attacker-controlled input. Treat every prompt as hostile until proven otherwise, and never let the model take an irreversible action without a control in front of it.

## What this is

The defensive layer around an LLM system: redacting sensitive data, resisting prompt injection, enforcing an output policy, and constraining what agentic actions the model is allowed to take. Mapped to the frameworks reviewers and auditors expect — **OWASP LLM Top 10**, **NIST AI RMF**, and the **EU AI Act**.

## Why it matters

The model is the easy part. The risk is everything around it: a support bot that leaks another customer's data, an agent tricked by a poisoned document into calling a destructive tool, a summarizer that echoes a secret it read. These are not edge cases — they're the default failure mode of a naive integration. Guardrails are what turn a clever demo into a system that legal, security, and compliance will sign off on.

## Defense layers

| Layer | Defends against | Control |
|-------|----------------|---------|
| **Policy** | Out-of-scope use | Define allowed use, data classes, and prohibited actions up front |
| **Input** | Injection, PII ingress | Redact/classify input; isolate untrusted content from instructions |
| **Instruction** | Goal hijacking | Keep system rules above user/retrieved content; never concatenate blindly |
| **Execution** | Unsafe tool use | Allow-list tools; least privilege; human-in-the-loop on irreversible actions |
| **Output** | Data egress, toxic/unsafe output | Validate, filter, redact before anything leaves the system |
| **Monitor** | Slow-burn abuse | Log, trace, and alert on anomalies — see [../observability](../observability/README.md) |

### PII redaction

- Detect and mask sensitive data **on the way in** (before it hits the prompt or logs) and **on the way out** (before it reaches the user or another system).
- Never log raw prompts or completions that may contain PII or secrets.
- Prefer tokenization/pseudonymization over free-text so you can still trace without exposing data.

### Prompt-injection defense

- **Trust boundary:** system instructions are trusted; user input and retrieved/tool content are *not*. Keep them structurally separated, never merged into one instruction blob.
- Assume any document, web page, or tool result can contain "ignore previous instructions." Design so that even if the model is fooled, it **can't** do damage — the real control is at the execution layer, not the prompt.
- Constrain outputs to a schema so injected free-form instructions have nowhere to land.

### Agentic action control

- **Allow-list** tools per agent; default deny.
- **Least privilege** — scoped, read-only credentials wherever possible; no standing write/delete access.
- **Confirmation gates** on irreversible or high-impact actions (writes, payments, deletions, external sends).
- **Audit trail** on every tool call: who/what/when/why, tied to the request trace.

## Compliance checklist

- [ ] **OWASP LLM Top 10** reviewed — injection, insecure output handling, data leakage, excessive agency, supply chain.
- [ ] **NIST AI RMF** — Govern / Map / Measure / Manage documented for the system.
- [ ] **EU AI Act** — risk tier identified; transparency, human oversight, and logging obligations met if in scope.
- [ ] PII redaction on input and output paths; no sensitive data in logs.
- [ ] Trust boundary enforced between system instructions and untrusted content.
- [ ] Tools allow-listed, least-privilege credentials, confirmation on irreversible actions.
- [ ] Every tool call audited and traceable.
- [ ] Output validated against a schema/policy before egress.

## How to use this

Pick the layers your system actually needs — a read-only chatbot doesn't need execution gates, but anything with tools does. Design the execution layer first: assume the prompt *will* eventually be injected and make sure the blast radius is small regardless. Pair this with [../observability](../observability/README.md) for the Monitor layer and with [../evals-testing](../evals-testing/README.md) to add adversarial/injection cases to your golden set.
