# _frontier/edge-on-device/ — Local & Offline Inference

> **Status: reserved — coming.** Maturity: **Maturing**. Production-viable today; held here only until kit-level rules are written.

Running models on the device instead of a hosted API — laptops, phones, single-board
computers, and dedicated NPUs. The capability is already practical; it sits in
`_frontier/` only because the kit doesn't yet have a clean rule layer for the
local-vs-cloud routing decision.

See the umbrella in [`../README.md`](../README.md) and the stable core in
[`../../foundations/`](../../foundations/).

## Why it matters

On-device inference changes the cost, privacy, and availability profile of a feature.
Data never leaves the machine, there's no per-token bill, and the system keeps working
offline. The tradeoff is smaller models, finite memory, and quantization-driven quality
loss — which means the *routing* decision (handle locally vs. escalate to a hosted model)
becomes the real architecture, not the model choice itself.

## What this will cover

- **Local runtimes** — model servers and embeddable libraries (e.g. Ollama, llama.cpp)
  exposed behind the same internal interface as a hosted provider.
- **Quantization** — choosing precision (4/5/8-bit and beyond) against a quality and
  memory budget; measuring the drop rather than assuming it.
- **Hardware acceleration** — NPUs and on-device runtimes (e.g. ExecuTorch and mobile
  accelerators) for phones and embedded targets.
- **Local-vs-cloud routing** — a policy layer that keeps cheap, private, latency-sensitive
  calls local and escalates only when the task exceeds local capability.
- **Offline-first behavior** — graceful degradation and queueing when no network is present.

## Early checklist (when you adopt this)

- [ ] A provider-neutral interface wraps every model call, so local and hosted are swappable.
- [ ] Quality loss from quantization is measured on your own evals, not assumed.
- [ ] Memory and thermal limits of the target device are known before model selection.
- [ ] Routing policy is explicit: which tasks stay local, which escalate, and why.
- [ ] Offline failure modes degrade gracefully (cache, queue, clear user signal).
- [ ] Local model versions are pinned and tracked like any other dependency.

## How to use

Put every model call behind one interface and make "local or hosted" a routing decision,
not a hardcode. Prototype with a local runtime, measure quality on your own data, and let
the escalation policy carry the quality you can't get on-device. This area graduates once
the kit can state that routing policy as a rule.
