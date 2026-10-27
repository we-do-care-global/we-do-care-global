# Website continuation — 2026-10-17

## Verified remote state
- Main: 5a46635e2337a1e59307060da245f53e35ee3e16.
- V3 review branch before this report: 9ec8a2ba86cd2fd461e31f5a9b962642d644248c.
- PR #1 remains open/draft/unmerged. No issue-conversation comments were returned.
- Main has newer website commits: bc073177 (fixed design), 6ec7805b (audited pages/evidence/accessibility), 5a46635 (restored theme variables).

## Checks executed during this continuation
Fetched 24 current text files pinned to main SHA. Exact local content was verified against all 24 Git blob hashes. Inspected 16 HTML pages and 336 local href/src/poster references against the remote Git tree: no missing paths, missing fragments or duplicate IDs. CSS asset references also resolve in the remote tree. This verifies referenced asset existence, not downloaded media/font integrity or browser rendering.

node --check passed for app.js, shared.js and project-demos.js. These checks are not browser interaction tests.

Fetched https://wedocare-global.com/ homepage. Comparing markup against organization main after splitting tags onto separate lines found one added footer paragraph on live, containing an analytics/privacy claim and inline styles. No analytics behavior or privacy claim was independently validated. The newer source CSP disallows inline styles; visual impact of this live-only footer requires browser confirmation.

## Reconciliation decision
Do not treat the old V3 candidate as the newest implementation or deploy it over current main. Current main already contains permanent project pages, evidence index, local fonts/licenses, metadata, demo labels and browser-local inquiry handling. The original accepted V2 and V3 remain useful historical review snapshots.

Current contact intentionally prepares/copies/downloads inquiries; it does not deliver them through a server. Do not silently restore the earlier candidate's FormSubmit integration. Mail delivery remains unverified and is a separate implementation decision.

README on main identifies production source as we-do-care-global/we-do-care-global main:/docs. WEBSITE_AUDIT_FIXES.md has copied wording saying this repository's docs/ even though this org repository serves as a root-level source mirror. Hosting provenance is documented, not independently established by a successful deployment in this turn.

## Next bounded work
1. Start future website fixes from current main, in a separate task branch; preserve existing review snapshots.
2. Reconcile the live-only footer against the actual production repository and verify any analytics statement against code and network behavior before changing it.
3. Run real desktop/mobile browser tests of current main/live, including project links, menu, inquiry controls and reduced motion. Do not submit an email.
4. Correct copied hosting-path documentation in a reviewed change.
5. Keep PR #1 draft until its archive-only purpose and relationship to newer main are resolved. No deployment, merge, DNS or visibility change is authorized by this continuation.

No production files, runtime services, repository visibility or deployment settings were changed in this turn.
