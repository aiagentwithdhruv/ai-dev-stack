# Free & Low-Cost LLM Providers (for a self-hosted agent)

Run a self-hosted agent for ~$0/month in model costs by pointing it at a free or generous-free-tier
LLM provider. All providers below are mainstream and publicly available.

## Provider comparison

| Provider | Free tier | Context | Quality | Best for |
|----------|-----------|---------|---------|----------|
| **Moonshot AI (Kimi)** | Free (subject to change) | ~256K | Great | Primary model, long context |
| **Google Gemini** | ~1,500 req/day | ~1M | Great | Vision/images, very long context |
| **Groq** | Free, rate-limited | ~128K | Good | Fastest responses, quick Q&A |
| **Cerebras** | Free, rate-limited | ~128K | Good | Fast inference |
| **OpenRouter** | ~50 req/day (free models) | Varies | Varies | Backup / model variety |
| **Ollama (local)** | Unlimited | Varies | Good | Privacy, offline, no API cost |

> Free tiers and pricing change often — verify current limits on each provider's site before relying on them.

## Moonshot AI (Kimi) — common primary
- Sign up at the Moonshot platform, create an **API key** (starts with `sk-`).
- In the agent's onboarding wizard, select the Moonshot/Kimi provider and paste the key.
- Large context window fits long documents; quality is competitive with mainstream frontier-lite models.

## Google Gemini (free tier)
- Generous free tier with a very large context window and vision support.
- Useful models: a fast/cheap flash tier for most chat, a higher-quality pro tier for harder reasoning,
  and a vision-capable model for image analysis.
- Get an API key from Google AI Studio, then select **Google** as the provider during onboarding.

## Groq / Cerebras (free, very fast)
- Extremely fast inference; great for snappy Q&A.
- Rate limits can throttle heavy use — good as a "fast lane," not always the primary.

## Ollama (local, unlimited)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.3            # or llama3.1:8b (light), qwen2.5:32b (multilingual)
# serves on http://localhost:11434
```
Point the agent at the local Ollama/OpenAI-compatible endpoint. **Note:** running local models on a
small 2-CPU / 8 GB VPS is slow — local models are better on a 16 GB+ machine or a GPU box.

## Cost-optimization checklist
1. **Use a free model as primary.** A free long-context model handles the large majority of tasks at $0.
2. **Raise the heartbeat interval to 6h+.** Each heartbeat is a full API call; frequent ticks burn tokens.
3. **Reset sessions after big tasks.** A 50-message thread resends 100K+ tokens of context on every new
   message — start a fresh session per new topic.
4. **Use local memory search.** Set `memorySearch.provider = local` to avoid embedding-API costs.
5. **Monitor usage.** Most agents expose a usage/status command in-chat and a Usage panel in the dashboard.

## Mixing providers by task
| Task | Provider choice | Why |
|------|-----------------|-----|
| General chat | Free long-context model | Zero cost |
| Image analysis | Gemini (vision) | Multimodal |
| Fast Q&A | Groq / Cerebras | Lowest latency |
| Hard reasoning | A pro-tier or frontier model | Higher quality |
| Privacy-sensitive | Ollama (local) | Data stays on your box |

Configure multiple providers in the dashboard under **Config → Models**, then route per task.
