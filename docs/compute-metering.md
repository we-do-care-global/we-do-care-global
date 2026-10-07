# Compute Pass-Through Metering

## Problem

AI inference cost is **variable, not fixed**. If you absorb it into your base price, gross margin compresses to **50–60%** (vs 80–90% for legacy SaaS).

## Solution

**Per-request pricing** — pass AI inference costs directly to customers. Margin rebuilds to **80–90%** on the non-AI layer.

## How It Works

1. **Base subscription** — predictable revenue (e.g. $99/mo)
2. **Included requests** — fixed allowance (e.g. 100 requests)
3. **Overage rate** — per-request charge above allowance (e.g. $0.50/request)
4. **Inference cost** — passed through at cost (e.g. $0.018/request)

## Margin Impact

| Tier | Requests | Revenue | Inference Cost | Gross Margin |
|------|----------|---------|----------------|--------------|
| Starter | 1,000 | $549 | $18 | **96.7%** |
| Pro | 1,000 | $299 | $18 | **94.0%** |
| Enterprise | 1,000 | $999 | $18 | **98.2%** |

## Model Costs (per 1K tokens)

| Model | Input | Output |
|-------|-------|--------|
| NVIDIA NIM 49B | $0.02 | $0.04 |
| NVIDIA NIM 30B | $0.01 | $0.02 |
| xAI Grok | $0.015 | $0.03 |
| Mistral Large | $0.012 | $0.025 |

## Implementation

```bash
# Calculate metering for a tier
python compute_metering.py calculate --tier pro --requests 1000

# Full report
python compute_metering.py report --requests 1000
```

## Key Insight

> **1% price increase → ~11% profit improvement** (B2B SaaS inelastic demand).  
> Compute pass-through removes the margin compression risk entirely.

---

**We Do Care Global** — Autonomous AI Governance from First Principles
