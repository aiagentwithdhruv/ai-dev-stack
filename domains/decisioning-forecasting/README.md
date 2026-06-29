# Decisioning / Forecasting

> The classical-ML quadrant — demand forecasting, churn prediction, recommendations. Gradient boosting over a feature store, not an LLM.

## What it is

Predictive systems over structured, tabular data: forecast next month's demand, score which customers will churn, rank what to recommend next. The output is a number or a ranked list that drives an automated decision (reorder this much, intervene with this account, show these items). This is the vertical where **the LLM is the wrong tool**. Gradient-boosted trees on well-engineered features are faster, cheaper, more accurate, and explainable for structured prediction. Knowing this is a senior-engineer signal.

## Why it matters

- **Structured prediction is everywhere and high-leverage.** Inventory, retention, and ranking decisions move margin directly.
- **The right tool beats the trendy one.** XGBoost-class models win on tabular data; an LLM here is slower, pricier, and harder to validate. (Principle: don't use an LLM when a smaller model wins.)
- **Reproducibility is the difference between a model and a liability.** Versioned data, named checkpoints, and backtests are what let you trust a number in production. (See [rule 55 — Data & Model Versioning](../../rules/55-data-model-versioning.mdc).)

## Typical stack / pattern

```
Raw events → Feature pipeline → Feature store (offline + online, point-in-time correct)
                                        │
        Train (gradient boosting) → Backtest / cross-validate → Model registry (versioned)
                                        │
        Serve: batch scores ──▶ tables / dashboards
               online scores ─▶ API for real-time decisions
                                        │
                     Monitor: data drift, prediction drift, accuracy decay → retrain trigger
```

- **The feature store is the foundation.** Offline features for training and online features for serving must be computed the same way and be point-in-time correct (no leakage of the future into the past).
- **XGBoost / gradient boosting first** for tabular data; reach for deep learning only when features are genuinely unstructured (text, image, sequence).
- **Backtesting, not a single split.** Time-series problems demand walk-forward validation; a random split leaks.
- **Everything is versioned** — dataset snapshot, feature definitions, model checkpoint — so any prediction is reproducible. ([rule 55](../../rules/55-data-model-versioning.mdc).)
- **Monitoring closes the loop:** track input drift, prediction distribution, and accuracy decay; trigger retraining on thresholds, not on a calendar alone.

## De-identified example outline

**Demand forecast + churn scoring** for a subscription/retail business:

| Layer | Choice |
|-------|--------|
| Features | Usage, recency/frequency/monetary, seasonality, derived ratios — in a shared feature store |
| Demand model | Gradient-boosted regression with walk-forward backtest per SKU/segment |
| Churn model | Gradient-boosted classifier; calibrated probabilities; feature-importance for explainability |
| Serving | Nightly batch scores to a table; an online endpoint for on-demand churn risk |
| Versioning | Dataset snapshot + model version pinned in a registry for every deployed score |
| Monitoring | Population stability and accuracy-decay alerts; scheduled + drift-triggered retrain |

## Foundations it leans on

- **Classical ML** — gradient boosting, feature engineering, calibration, backtesting
- **Feature store & data pipelines** — point-in-time-correct offline/online features
- **Evaluation** — backtests, calibration, segment-level metrics, not a single accuracy number
- **Serving & deployment** — batch and online scoring paths, model registry
- **Observability** — drift and accuracy-decay monitoring with retrain triggers

See [foundations/](../../foundations/README.md) for the reusable implementations.

## How to use

1. Confirm the data is structured/tabular — if so, reach for gradient boosting before any LLM.
2. Build the feature pipeline with point-in-time correctness first; leakage is the most common silent failure.
3. Version dataset, features, and model together per [rule 55](../../rules/55-data-model-versioning.mdc) so every score is reproducible.
4. Backtest with walk-forward validation and ship monitoring on day one — a model without drift detection is a slowly breaking one.

## Related

- [domains/](../README.md) — the other five verticals
- [foundations/](../../foundations/README.md) · [rule 55 — Data & Model Versioning](../../rules/55-data-model-versioning.mdc) · [rule 85 — Error & Observability](../../rules/85-error-observability.mdc)
