# Cost Optimization — Running AI Automations Cheaply

> **Applies to:** every automation that uses paid model APIs.

## Problem
Model API calls cost money, and an unattended automation can burn a lot of it fast. The system
should enforce budget discipline automatically rather than relying on care.

## The Cost Hierarchy

```
FREE first:
  1. A free-tier model API (daily token allowance)
  2. A gateway/router with free signup credits
  3. Open-source models run locally (e.g. Ollama)

CHEAP second:
  4. A small/mini model  (~$0.15/1M in,  ~$0.60/1M out)
  5. A small frontier model (~$0.25/1M in, ~$1.25/1M out)

EXPENSIVE last:
  6. A standard frontier model (~$2.50/1M in, ~$10/1M out)
  7. A top-tier reasoning model (~$15/1M in, ~$75/1M out)
```
(Prices illustrative — confirm against current provider pricing.)

## Pattern: Model Routing by Task
Route each task to the cheapest model that can do it well. Cheap tasks (classification,
extraction, summarisation) go to a mini model; depth tasks (research, code review) earn a
frontier model.

```yaml
# config/models.yaml
tasks:
  classification: mini      # cheap — simple decision
  extraction:     mini      # cheap — structured output
  summarization:  mini      # cheap — compression
  generation:     mini      # balanced
  research:       frontier  # expensive — needs depth
  code_review:    frontier  # expensive — needs accuracy
```

## Cost Reduction Techniques

### 1. Caching (50-80% savings)
```python
import hashlib, json, os

CACHE_DIR = ".tmp/llm_cache/"

def cached_llm_call(prompt, model="mini"):
    cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()
    cache_file = f"{CACHE_DIR}{cache_key}.json"
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)
    result = llm_call(prompt, model)        # actual API call
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(result, f)
    return result
```

### 2. Prompt Length Reduction (20-40% savings)
- Strip unnecessary context from prompts.
- Put repeating instructions in the system prompt (cached by some providers).
- Send only the relevant chunk, not the whole document.

### 3. Batching (10-30% savings)
- Batch multiple small tasks into one prompt where possible.
- "Classify these 10 emails" beats 10 separate "classify this email" calls.

### 4. Budget Enforcement (prevents disasters)
```python
from cost_tracker import check_budget, record_cost   # see ../agent-safety-harness/

check_budget(estimated_cost=0.50)        # raises BudgetExceededError past the daily ceiling
# ... make the paid call ...
record_cost("classify", 0.003)           # ledger the actual spend
```

## Gotchas
- **Loops kill budgets:** an LLM call inside a 1000-item loop = 1000 API calls. Batch or cache.
- **Streaming doesn't save money:** same token count whether streamed or not.
- **Retries cost double:** 3 retries on a $0.10 call = $0.30. Fix the root cause.
- **Free tiers expire:** daily allowances reset; one-time credits don't. Monitor usage.

## Related
- `../agent-safety-harness/cost_tracker.py` — the enforcement code referenced above
- `deployment-patterns.md` — free hosting to keep infra costs at $0
