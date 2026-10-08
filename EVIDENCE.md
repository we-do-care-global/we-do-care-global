# We Do Care Global — Evidence & DOI Registry
> Canonical source: https://wedocare-global.com / https://github.com/we-do-care-global/we-do-care-global
> Last verified: 2026-10-08 (Europe/Sarajevo). Verify via `https://zenodo.org/api/records/{id}`.

## Verified Zenodo records (API-checked 2026-10-08)

| Project | Version DOI | Concept DOI | Date | Version | Creators | License | Status |
|---|---|---|---|---|---|---|---|
| AgentGuard | [10.5281/zenodo.22945778](https://doi.org/10.5281/zenodo.22945778) | 10.5281/zenodo.22945777 | 2026-09-24 | v0.1.0 | Perla, Emir | Apache-2.0 | ✅ Published |
| Enterprise Hybrid-RAG | [10.5281/zenodo.22945802](https://doi.org/10.5281/zenodo.22945802) | 10.5281/zenodo.22945801 | 2026-09-24 | v0.1.0 | Perla, Emir | Apache-2.0 | ✅ Published |
| Agent Eval | [10.5281/zenodo.22945804](https://doi.org/10.5281/zenodo.22945804) | 10.5281/zenodo.22945803 | 2026-09-24 | v0.1.0 | Perla, Emir | Apache-2.0 | ✅ Published |
| AgentVault | [10.5281/zenodo.22983557](https://doi.org/10.5281/zenodo.22983557) | — | 2026-09-26 | v0.1.3 | Perla, Emir | Apache-2.0 | ✅ Published |
| Pharma Intelligence OS | [10.5281/zenodo.22983388](https://doi.org/10.5281/zenodo.22983388) | — | 2026-09-26 | v0.1.1 | Perla, Emir | Apache-2.0 | ✅ Published |
| Portal (old) | [10.5281/zenodo.22983601](https://doi.org/10.5281/zenodo.22983601) | — | 2026-09-26 | v0.1.0 | Perla, Emir | Apache-2.0 | ⚠️ Duplicate of 22983603 — deprecate one |
| Portal (old dup) | [10.5281/zenodo.22983603](https://doi.org/10.5281/zenodo.22983603) | — | 2026-09-26 | v0.1.0 | Perla, Emir | Apache-2.0 | ⚠️ Duplicate — keep ONE canonical |
| FoundationCentar | [10.5281/zenodo.23073888](https://doi.org/10.5281/zenodo.23073888) | — | 2026-10-01 | v0.1.0 (record shows `vv0.1.0` typo — fix on next deposit) | We Do Care Global, Perla Emir | Apache-2.0 | ✅ Published, fix version string |
| Portal (current) | [10.5281/zenodo.23217953](https://doi.org/10.5281/zenodo.23217953) | — | 2026-10-01 | v1.0.0 | Perla Emir, We Do Care Global | Apache-2.0 | ✅ Published, canonical portal DOI |

## Known issues (fix queue)
- `22983602` → Zenodo API 302 to `22983603` (merged/deleted). Remove from READMEs.
- `22983604` → 404. Remove from READMEs until re-deposited.
- Portal README table reuses `23073888` for both FoundationCentar AND Hybrid-RAG — Hybrid-RAG must be `22945802`.
- `23073888` metadata version `vv0.1.0` — correct to `v0.1.0` on next release.
- `agentproof` has NO DOI yet — deposit as `v1.0.0` after pushing LICENSE + citation.cff from this pack.

## Live demos (HTTP 200 verified 2026-10-08)
- https://wedocare-global.com/
- https://we-do-care-global.github.io/we-do-care-global/
- https://we-do-care-global.github.io/agentguard/
- https://wedocareglobal-cc.github.io/FoundationCentar/
- https://we-do-care-global.github.io/enterprise-hybrid-rag/
- https://we-do-care-global.github.io/agent-eval/
- https://we-do-care-global.github.io/agentvault/
- https://we-do-care-global.github.io/pharma-intelligence-os/

## Research identity
- ORCID: https://orcid.org/0009-0009-8515-2727 (7 work groups, verified via ORCID API)
- GitHub canonical code: https://github.com/WeDoCareGlobal-CC (org, 7 repos) + https://github.com/we-do-care-global (user, 8 public repos, portal + agentproof canonical)
- License: Apache-2.0 everywhere (after agentproof LICENSE lands)

## How to re-verify
```bash
for id in 22945778 22945802 22945804 22983557 22983388 23073888 23217953; do
  curl -s "https://zenodo.org/api/records/$id" | python3 -c "import json,sys; d=json.load(sys.stdin); m=d['metadata']; print(d['doi'], m['title'][:60], m['publication_date'])"
done
```
