# Website candidate V3

Scope: accepted V2 visual identity with static product pages, progressive enhancement, metadata, native contact POST and cleaned CSS. No deployment or production modification is authorized or performed.

## Build and check

```sh
python website/build.py
python website/verify.py
node --check website/app.js
node website/test-interactions.cjs
python -m http.server 8080 --bind 127.0.0.1 --directory previews/candidate-v3
```

Open http://127.0.0.1:8080 . Browser QA remains outstanding. Eight HTML pages work without JavaScript. Filters and selector enhance them when JavaScript is available. Assets are copied from the immutable approved-v2 snapshot. Edit website/home.template.html, systems.json, style.css and app.js; rebuild instead of editing output.

## Review versus production

Default build emits noindex,nofollow and robots Disallow. Canonical/OG URLs describe the intended wedocare-global.com root deployment. `python website/build.py --production --output /tmp/wdc-release` emits indexable metadata and removes the review banner; it does NOT publish anything. Do not publish until explicitly approved. Do not use a production build for a public staging location.

## Contact

Native POST uses the same FormSubmit mailbox endpoint as the live homepage. Required name/email/message and consent; CAPTCHA enabled and honeypot present. JavaScript does not intercept the form or falsely report delivery. Submission navigates to FormSubmit. No test mail has been sent; mailbox activation and actual delivery are unverified. Privacy page describes this third-party flow. Operator must review provider/privacy details and perform a separately approved end-to-end mail test before release.

## Verification limits

Static integrity and simulated interactions pass. These do not prove browser layout, keyboard usability in a real browser, measured performance, external demo availability, mailbox delivery or production readiness. No Lighthouse score is claimed. Existing private hosted V2 has not been updated.
