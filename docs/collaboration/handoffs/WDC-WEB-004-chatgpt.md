# WDC-WEB-004 handoff

Base: ac1cdae52b45d9d956c4f15fa4d80c9c0053533c, design/approved-v2-handoff. User approved implementation after live-versus-V2 review. Production publication remains prohibited.

Added website/ generator, sources and checks; previews/candidate-v3/ output. Approved-v2 and its assets are unchanged. Eight pages: homepage, six product pages, privacy. All product descriptions and links are in static HTML. Added canonical, OG, Twitter, JSON-LD, sitemap and review noindex. Native FormSubmit POST replaces mailto draft; no email sent. CSS rewritten without previous orbital/modal code or layered V2 overrides. Video uses native 16:9 frame with contain; playback is JS-controlled after reduced-motion/save-data checks, with explicit controls and pause on backgrounding.

Executed: Python default build and verify; Python production build to /tmp/wdc-production-check and verify; node --check; node website/test-interactions.cjs. All passed. Production-build test is local output only, not deployment. Checks cover eight pages, local links/assets/fragments, metadata, six static cards, POST/consent, motion defaults, menu/filter/selector simulation and no-home-component JS guards.

Outstanding: real desktop/mobile screenshots, browser keyboard check, visually inspect full video frame, actual FormSubmit mailbox delivery with separate authorization, independently revalidate external demo/DOI targets. No browser or delivery success claimed.

Hermes next: fetch latest design/approved-v2-handoff, read website/README.md, claim WDC-WEB-002, serve previews/candidate-v3 and return screenshots/findings in a task branch. Preserve any existing local Next.js work. Do not publish, merge, deploy or alter DNS.
