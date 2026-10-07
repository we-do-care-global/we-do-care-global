# Compliance Matrix — AgentProof Evidence Pack

## Bundled Pricing

| Tier | Price | Compliance | Evidence Pack |
|------|-------|------------|----------------|
| **Starter** | $99/mo | EU AI Act (minimal risk) | Basic audit trail |
| **Pro** | $299/mo | EU AI Act + ISO 27001 | Full evidence pack + SOC 2 |
| **Enterprise** | $999/mo | EU AI Act + ISO 27001 + SOC 2 | Complete compliance suite |

**Bundled, not add-on.** Compliance evidence is included in base price.

## Unified Compliance Matrix

| Control | SOC 2 | ISO 27001 | EU AI Act | AgentProof Evidence |
|---------|-------|-----------|-----------|---------------------|
| Access control | CC6.1 | A.9.1.2 | Art. 14 | ExecutionBlock access logs |
| Change management | CC8.1 | A.12.1.2 | Art. 17 | Versioned execution blocks |
| Event logging | CC7.1 | A.12.4.1 | Art. 12 | Real-time action logging |
| Log protection | CC7.2 | A.12.4.2 | Art. 12 | Immutable append-only log |
| Incident detection | CC7.2 | A.16.1.1 | Art. 9 | Anomaly detection |
| Incident response | CC7.3 | A.16.1.4 | Art. 9 | Automated compliance blocking |
| Risk management | CC3.1 | A.6.1.2 | Art. 9 | Risk assessment per action |
| Data governance | CC5.1 | A.8.2.1 | Art. 10 | Training data provenance |
| Human oversight | CC1.2 | A.6.1.3 | Art. 14 | Human-in-the-loop blocks |
| Transparency | CC2.1 | A.13.2.1 | Art. 13 | Agent action disclosure |
| Accuracy | CC2.2 | A.14.2.1 | Art. 15 | Model performance tracking |
| Business continuity | CC9.1 | A.17.1.1 | Art. 17 | Merkle root backup |
| Legal compliance | CC10.1 | A.18.1.1 | Art. 16 | Regulation mapping engine |

## Evidence Artifacts

1. **ExecutionBlock Chain** — SHA-256 hashed, Ed25519 signed
2. **Agent Action Log** — timestamped, immutable
3. **Compliance Report** — auto-generated per audit period
4. **Merkle Root** — daily aggregate for verification

## Audit Trail Integrity

```
Block N:   [Action Data] + [Previous Hash] → SHA-256 → Ed25519 Sign
Block N+1: [Action Data] + [Block N Hash] → SHA-256 → Ed25519 Sign
...
Merkle Root: Hash(Block 1 + Block 2 + ... + Block N)
```

## Retention

- **SOC 2:** 7 years minimum
- **ISO 27001:** 3 years minimum
- **EU AI Act:** 6 months minimum
- **Storage:** Immutable append-only log
- **Verification:** Merkle root published daily

---

**We Do Care Global** — Autonomous AI Governance from First Principles
