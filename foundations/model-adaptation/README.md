# Model Adaptation

> Don't fine-tune when RAG works. Don't RAG when prompting works. Each step up the ladder costs more to build and maintain — climb only when the step below provably can't do the job.

## What this is

A decision framework for closing the gap between what a base model does out of the box and what your task needs. The options, cheapest to most expensive: **prompt → RAG → fine-tune**. This doc is about choosing correctly, then executing each well.

## Why it matters

The instinct to "fine-tune our own model" kills more AI projects than it saves. Fine-tuning is slow to iterate, expensive to maintain, and goes stale the moment your data changes — and most problems people reach for it to solve are actually prompting or retrieval problems. Picking the right rung saves months. Picking the wrong one buys you a custom model you have to babysit forever.

## The decision tree

```
Is the base model capable of the task with clear instructions?
├── YES → PROMPT. Stop here. Iterate on the prompt + few-shot examples.
└── NO → Is the gap missing KNOWLEDGE (facts, docs, current data)?
         ├── YES → RAG. Retrieve the right context at request time.
         └── NO → Is the gap missing BEHAVIOR (format, style, a narrow skill)?
                  ├── YES → FINE-TUNE. And first try prompt + RAG once more.
                  └── STILL NO → Revisit the task. The model may be wrong for it.
```

| Rung | Use when | Cost | Iteration speed |
|------|----------|------|-----------------|
| **Prompt** | Capability is there, instructions just need to be clear | Lowest | Minutes |
| **RAG** | Model lacks *knowledge* — your docs, fresh or proprietary data | Medium | Hours |
| **Fine-tune** | Model lacks *behavior* — consistent format/style, narrow skill, or you need to shrink a big model into a small one | Highest | Days+ |

**Key distinction:** RAG fixes *what the model knows*; fine-tuning changes *how the model behaves*. Confusing the two is the most common and most expensive mistake. If your answers are wrong because the model lacks facts, no amount of fine-tuning fixes it — you need retrieval.

## When you do fine-tune

### PEFT / LoRA — fine-tune efficiently

- Use parameter-efficient methods (LoRA and friends) instead of full fine-tuning: train a small set of adapter weights, keep the base frozen.
- Far cheaper, faster to train, and you can keep multiple adapters per use case.
- This is the default fine-tuning approach now — full fine-tunes are rarely worth it.

### Distillation — shrink a big model into a small one

- Use a large, capable model to generate high-quality outputs, then train a smaller, cheaper model to reproduce them.
- Goal: frontier-ish quality on a narrow task at a fraction of the serving cost and latency.
- Feeds directly into the cheap tier of [../model-routing-cost](../model-routing-cost/README.md).

### Synthetic data — when you don't have enough labels

- Generate training examples with a capable model when real labeled data is scarce.
- **Guard quality ruthlessly** — synthetic data inherits the generator's biases and errors; filter, validate, and mix with real data.
- Never train solely on unvetted synthetic output; you'll bake in failures.

## Adaptation checklist

- [ ] Tried prompting + few-shot seriously before anything heavier.
- [ ] Classified the gap as **knowledge** (→ RAG) vs **behavior** (→ fine-tune).
- [ ] Ruled out RAG before committing to a fine-tune.
- [ ] If fine-tuning, using PEFT/LoRA unless a full fine-tune is justified.
- [ ] Considered distillation to cut serving cost on a narrow task.
- [ ] Any synthetic training data is filtered, validated, and mixed with real data.
- [ ] Every adaptation is measured against a golden set (see [../evals-testing](../evals-testing/README.md)) — climbing the ladder must prove a quality gain.

## How to use this

Walk the tree top-down every time and write down *why* you ruled out the cheaper rung — that note is what stops the team from defaulting to fine-tuning out of habit. Validate each step with evals: if RAG doesn't beat the prompt on your golden set, the problem isn't knowledge. When a fine-tune or distilled model does win, ship it through [../deploy-mlops](../deploy-mlops/README.md) with the dataset versioned so the result is reproducible.
