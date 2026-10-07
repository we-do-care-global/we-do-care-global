# AgentProof Evidence Pack

## SOC 2 / ISO 27001 / EU AI Act Compliance Evidence

**Bundled, base price — not add-on.**

Every agentproof ExecutionBlock is automatically mapped to compliance controls across 4 frameworks. The Merkle chain + Ed25519 signature becomes your audit evidence.

---

## What's Included

| Framework | Controls | Evidence |
|-----------|----------|----------|
| **SOC 2** | 6 Trust Services Criteria | Access controls, incident detection, change management |
| **ISO 27001** | 6 Annex A controls | Privileged access, data masking, leakage prevention |
| **EU AI Act** | 7 Articles | Risk management, data governance, human oversight |
| **NIST AI RMF** | 4 Functions | Govern, Map, Measure, Manage |

**Total: 23 compliance controls mapped to agentproof ExecutionBlock fields.**

---

## How It Works

```
agentproof ExecutionBlock
├── agent_id → SOC 2 CC6.1, ISO A.8.1
├── policy_context → SOC 2 CC6.1, ISO A.8.2, EU AI Act Art. 9/14, NIST GOVERN
├── invocation → SOC 2 CC6.2, EU AI Act Art. 13
├── telemetry → SOC 2 CC7.1, ISO A.8.11, EU AI Act Art. 10, NIST MAP
├── merkle_root → SOC 2 CC6.3, ISO A.8.3/8.12, EU AI Act Art. 12, NIST MEASURE
├── signature → SOC 2 CC7.2, ISO A.8.4, EU AI Act Art. 15, NIST MANAGE
├── version → SOC 2 CC8.1, EU AI Act Art. 11
└── timestamp_ns → SOC 2 CC7.2, ISO A.8.4, EU AI Act Art. 12/15
```

---

## Usage

```python
from evidence_pack.compliance_mapping import ComplianceMapper

mapper = ComplianceMapper()
evidence_pack = mapper.generate_evidence_pack(execution_blocks)

# Returns:
# {
#   "soc2": {"total_controls": 6, "satisfied": 6, ...},
#   "iso27001": {"total_controls": 6, "satisfied": 6, ...},
#   "eu_ai_act": {"total_controls": 7, "satisfied": 7, ...},
#   "nist_ai_rmf": {"total_controls": 4, "satisfied": 4, ...}
# }
```

---

## Pricing

**Bundled — base price, not add-on.**

| Tier | Price | Evidence Pack |
|------|-------|---------------|
| Starter | $99/mo | ✅ Included |
| Pro | $299/mo | ✅ Included |
| Enterprise | $999/mo | ✅ Included |

> **Productize audit trail** — agentproof chain + signing = regulatory artifact. Bundling is table stakes.

---

## Key Insight

> **Compliance-as-Code (CAC)** — sync agentproof ExecutionBlock + Ed25519 chain into a policy-as-code engine that maps EU AI Act / NIST AI RMF / ISO 42001 / SOC 2 controls to executed actions.
>
> Monetization: $25K–$120K/yr mid-market.

---

**We Do Care Global** — Autonomous AI Governance from First Principles
