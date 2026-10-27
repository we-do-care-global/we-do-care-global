# Approved website design V2 — source only

User accepted this visual direction on 16 October 2026, Sarajevo time. Publishing is NOT authorized.

This is the static preview: near-black/graphite, cyan, restrained gold, original logo and user-provided infrastructure video. It is not a completed backend platform and not a Next.js migration.

## Run locally

From the repository root:

```sh
python -m http.server 8080 --bind 127.0.0.1 --directory previews/approved-v2
```

Open http://127.0.0.1:8080 . No installation or build needed. Google Fonts is optional; local fallback fonts are configured. The contact form opens a mail draft and sends nothing itself.

## Evidence

Source snapshot: Sites commit 15e69ad61d688032fca998df3ee06eca474df5da.
JS syntax, local asset/anchor checks, simulated filter/dialog/recommendation tests passed. Browser visual QA remains incomplete due to internal preview infrastructure failure. Video: H.264, 1280x720, 10 seconds, no audio track. Original uploads remain unchanged.

The earlier private design preview already existed before the user's no-publish instruction. This GitHub handoff does not update that site or production. No deployment workflow is included.

External project links point to the same organization; they are not API integrations. DOI values were carried from the current portfolio, not independently revalidated here.
