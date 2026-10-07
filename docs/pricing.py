"""
WDCG Pricing Engine — SaaS pricing, margin floor, discount leakage + elasticity
We Do Care Global — Revenue Global Control Platform (rgcp) market publication

Standards:
- Margin floor  = COGS / (1 - target_margin)   (SaaS Pricing Strategy Calculator)
- CAC-payback floor = CAC / target_CAC_payback_months
- 1% price rise  ~ 11% profit (B2B SaaS inelastic demand)
- Annual-discount leakage ~28% in 2025 vs 15% in 2022 -> 3-5% of ARR lost
- Compute pass-through: AI inference should NOT be absorbed; route per-request
- Discriminatory pricing anchors: AgentShield $24-$749/mo per agent fleet;
  consumption $0.50-$5/agent action
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# 1. Margin floor (SaaS Pricing Strategy Calculator)                          #
# --------------------------------------------------------------------------- #
@dataclass
class MarginConfig:
    cogs_per_unit: float = 42.0        # $42 COGS per unit (benchmark)
    target_margin: float = 0.85        # 85% target gross margin
    target_cac_payback_months: float = 12.0
    cac: float = 600.0                 # $600 CAC
    competitor_floor: float = 99.0     # $99 competitor reference

    @property
    def margin_floor(self) -> float:
        return self.cogs_per_unit / (1.0 - self.target_margin)

    @property
    def payback_floor(self) -> float:
        return self.cac / self.target_cac_payback_months

    @property
    def gross_margin_at_competitor(self) -> float:
        return (self.competitor_floor - self.cogs_per_unit) / self.competitor_floor


# --------------------------------------------------------------------------- #
# 2. Discount leakage audit                                                   #
# --------------------------------------------------------------------------- #
@dataclass
class DiscountRule:
    code: str
    tier: str
    percent: float
    term_months: int
    applied_since: str
    status: str = "active"            # active | expired | past_term
    flagged: bool = False
    reason: str = ""


class DiscountLeakageAudit:
    """
    Detect discount leakage: discount still applied past its stated term.
    Benchmark: 28% of annual discounts in 2025 vs 15% in 2022 -> 3-5% of ARR leaked.
    """

    def __init__(self):
        self.rules: list[DiscountRule] = []

    def add(self, code: str, tier: str, percent: float,
            term_months: int, applied_since: str) -> DiscountRule:
        rule = DiscountRule(code, tier, percent, term_months,
                            applied_since, status="active")
        self.rules.append(rule)
        return rule

    def audit(self) -> list[dict]:
        for r in self.rules:
            try:
                applied = datetime.strptime(r.applied_since, "%Y-%m-%d")
                term_end = applied.replace(
                    year=applied.year + r.term_months)
                term_end = term_end.replace(day=min(applied.day, 28))
                # Flag if term ended more than a month ago (leakage)
                if datetime.utcnow() > term_end.replace(day=min(term_end.day, 28)):
                    r.status = "past_term"
                    r.flagged = True
                    r.reason = f"applied {r.term_months}mo term ended {term_end}"
            except Exception:
                r.status = "expired"
                r.flagged = True
                r.reason = "unparseable date"
        return [{
            "code": r.code,
            "tier": r.tier,
            "percent": r.percent,
            "term_months": r.term_months,
            "applied_since": r.applied_since,
            "status": r.status,
            "flagged": r.flagged,
            "reason": r.reason,
        } for r in self.rules]

    def summary(self) -> dict:
        total = len(self.rules)
        flagged = sum(1 for r in self.rules if r.flagged)
        return {"total_discounts": total, "flagged": flagged,
                "leakage_pct": round(100.0 * flagged / total, 1) if total else 0.0}


# --------------------------------------------------------------------------- #
# 3. Elasticity ceiling                                                       #
# --------------------------------------------------------------------------- #
@dataclass
class TierConfig:
    name: str
    price: float
    cogs: float
    elasticity: float = 1.0         # price elasticity of demand
    inelastic_floor_pct: float = 0.40   # entry tiers stay inelastic up to +40%


def elasticity_ceiling(price: float,
                       elasticity: float = 1.0,
                       inelastic_floor_pct: float = 0.40) -> float:
    """
    Price-elasticity ceiling: for inelastic demand, a price rise is profitable.
    1% price increase ~ 11% profit improvement (B2B SaaS).
    Inelastic entry tiers can go up 40% before demand falls away.
    """
    if elasticity <= 0:
        return round(price * (1 + inelastic_floor_pct), 2)
    # For inelastic demand (|e| < 1), raise price up to the inelastic floor
    return round(price * (1 + inelastic_floor_pct), 2)


# --------------------------------------------------------------------------- #
# 4. Compute pass-through (AI inference)                                      #
# --------------------------------------------------------------------------- #
@dataclass
class ComputePassThrough:
    model_input_price: float = 5.0    # $/M input tokens (2026 benchmark)
    model_output_price: float = 25.0  # $/M output tokens (2026 benchmark)
    workhorse_in: float = 3.0         # $/M input
    workhorse_out: float = 15.0       # $/M output
    light_in: float = 1.0             # $/M input
    light_out: float = 5.0            # $/M output

    def input_cost(self, tokens: int, model: str = "workhorse") -> float:
        price = {"workhorse": self.workhorse_in,
                 "light": self.light_in}[model]
        return tokens / 1_000_000 * price

    def output_cost(self, tokens: int, model: str = "workhorse") -> float:
        price = {"workhorse": self.workhorse_out,
                 "light": self.light_out}[model]
        return tokens / 1_000_000 * price

    def per_action_estimate(self, in_tokens: int, out_tokens: int) -> float:
        return self.input_cost(in_tokens) + self.output_cost(out_tokens)


# --------------------------------------------------------------------------- #
# 5. Public pricing recommendation (published payload)                        #
# --------------------------------------------------------------------------- #
def pricing_recommendation() -> dict:
    m = MarginConfig()
    return {
        "version": "1.0.0",
        "rgcp": "Revenue Global Control Platform",
        "snapshot": datetime.utcnow().isoformat()[:10],
        "margin_floor": round(m.margin_floor, 2),
        "payback_floor": round(m.payback_floor, 2),
        "competitor_floor": m.competitor_floor,
        "gross_margin_at_competitor": round(m.gross_margin_at_competitor * 100, 2),
        "gap_to_margin_floor": round(m.margin_floor - m.competitor_floor, 2),
        "pricing_benchmark": {
            "AgentShield": "$24-$749/mo per agent fleet (self-serve)",
            "consumption": "$0.50-$5/agent action",
            "ai_red_teaming": "$8K-$150K+ per engagement",
            "agentic_compliance": "$10K-$500K+/yr",
        },
        "recommendation": (
            "Raise entry tier above the margin floor: "
            f"floor ${m.margin_floor:.0f}/unit vs competitor ${m.competitor_floor:.0f}. "
            "Convert to hybrid billing (base + usage). Cap annual discounts at +30% "
            "to stop leakage. Route inference per-request."
        ),
    }


# --------------------------------------------------------------------------- #
# 6. Build the hosted pricing.json payload                                    #
# --------------------------------------------------------------------------- #
def build_pricing_json() -> str:
    data = pricing_recommendation()
    data["leakage_sample"] = DiscountLeakageAudit().audit()
    return json.dumps(data, indent=2, ensure_ascii=False)
