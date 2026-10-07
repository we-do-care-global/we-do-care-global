#!/usr/bin/env python3
"""
Compute Pass-Through Metering Engine
=====================================
Per-request pricing model that passes AI inference costs directly to customers,
keeping gross margins at 80-90% instead of 50-60%.

Key insight: AI inference cost is variable, not fixed. If you absorb it,
gross margin compresses to 50-60%. If you pass it through per-request,
margin rebuilds to 80-90% on the non-AI layer.

Usage:
    python compute_metering.py calculate --requests 1000 --model nvidia-nim
    python compute_metering.py calculate --requests 10000 --model custom
    python compute_metering.py report
"""

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


# Model inference costs per 1K tokens (USD)
MODEL_COSTS = {
    "nvidia-nim-49b": {"input": 0.02, "output": 0.04, "context": 32000},
    "nvidia-nim-30b": {"input": 0.01, "output": 0.02, "context": 32000},
    "xai-grok": {"input": 0.015, "output": 0.03, "context": 128000},
    "mistral-large": {"input": 0.012, "output": "0.025", "context": 128000},
    "custom": {"input": 0.01, "output": 0.02, "context": 8000},
}

# Pricing tiers (per-request, USD)
PRICING_TIERS = {
    "starter": {
        "base_price": 99,
        "included_requests": 100,
        "overage_rate": 0.50,  # per request
        "margin_target": 0.85,
    },
    "pro": {
        "base_price": 299,
        "included_requests": 1000,
        "overage_rate": 0.30,
        "margin_target": 0.88,
    },
    "enterprise": {
        "base_price": 999,
        "included_requests": 10000,
        "overage_rate": 0.15,
        "margin_target": 0.90,
    },
}


@dataclass
class MeteringResult:
    tier: str
    requests: int
    model: str
    base_price: float
    included_requests: int
    overage_requests: int
    overage_rate: float
    overage_revenue: float
    inference_cost: float
    total_revenue: float
    gross_profit: float
    gross_margin: float
    margin_target: float
    margin_gap: float


def calculate_inference_cost(
    requests: int, model: str, avg_input_tokens: int = 500, avg_output_tokens: int = 200
) -> float:
    """Calculate total inference cost for given request volume."""
    costs = MODEL_COSTS.get(model, MODEL_COSTS["custom"])
    input_cost = (requests * avg_input_tokens / 1000) * costs["input"]
    output_cost = (requests * avg_output_tokens / 1000) * costs["output"]
    return input_cost + output_cost


def calculate_tier(
    tier_name: str, requests: int, model: str = "nvidia-nim-49b"
) -> MeteringResult:
    """Calculate metering result for a specific tier."""
    tier = PRICING_TIERS[tier_name]
    base_price = tier["base_price"]
    included = tier["included_requests"]
    overage_rate = tier["overage_rate"]
    margin_target = tier["margin_target"]

    overage_requests = max(0, requests - included)
    overage_revenue = overage_requests * overage_rate
    total_revenue = base_price + overage_revenue

    inference_cost = calculate_inference_cost(requests, model)
    gross_profit = total_revenue - inference_cost
    gross_margin = gross_profit / total_revenue if total_revenue > 0 else 0
    margin_gap = margin_target - gross_margin

    return MeteringResult(
        tier=tier_name,
        requests=requests,
        model=model,
        base_price=base_price,
        included_requests=included,
        overage_requests=overage_requests,
        overage_rate=overage_rate,
        overage_revenue=overage_revenue,
        inference_cost=inference_cost,
        total_revenue=total_revenue,
        gross_profit=gross_profit,
        gross_margin=gross_margin,
        margin_target=margin_target,
        margin_gap=margin_gap,
    )


def format_report(results: list[MeteringResult]) -> str:
    """Format metering results as human-readable report."""
    lines = [
        "=" * 70,
        "COMPUTE PASS-THROUGH METERING REPORT",
        "=" * 70,
        "",
    ]

    for r in results:
        lines.extend([
            f"Tier: {r.tier.upper()}",
            f"  Requests: {r.requests:,}",
            f"  Model: {r.model}",
            f"  Base price: ${r.base_price:.2f}",
            f"  Included requests: {r.included_requests:,}",
            f"  Overage requests: {r.overage_requests:,}",
            f"  Overage rate: ${r.overage_rate:.2f}/request",
            f"  Overage revenue: ${r.overage_revenue:.2f}",
            f"  Inference cost: ${r.inference_cost:.2f}",
            f"  Total revenue: ${r.total_revenue:.2f}",
            f"  Gross profit: ${r.gross_profit:.2f}",
            f"  Gross margin: {r.gross_margin:.1%}",
            f"  Margin target: {r.margin_target:.1%}",
            f"  Margin gap: {r.margin_gap:+.1%}",
            "",
        ])

    lines.append("=" * 70)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Pass-Through Metering")
    sub = parser.add_subparsers(dest="command")

    calc = sub.add_parser("calculate", help="Calculate metering for a tier")
    calc.add_argument("--tier", choices=list(PRICING_TIERS), required=True)
    calc.add_argument("--requests", type=int, required=True)
    calc.add_argument("--model", choices=list(MODEL_COSTS), default="nvidia-nim-49b")

    report = sub.add_parser("report", help="Full metering report")
    report.add_argument("--requests", type=int, default=1000)

    args = parser.parse_args()

    if args.command == "calculate":
        result = calculate_tier(args.tier, args.requests, args.model)
        print(format_report([result]))
        return 0
    elif args.command == "report":
        results = [
            calculate_tier(tier, args.requests) for tier in PRICING_TIERS
        ]
        print(format_report(results))
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
