# SeaVees — Findings & Recommendations (CreditSwan)

Static, password-protected report. The entire report is AES-256-GCM encrypted
inside index.html; decryption happens in the visitor's browser after they enter
the access password. Nothing readable is served to anyone without it.

## Deploy

Option A — dashboard: drag this folder into https://vercel.com/new (framework: Other).

Option B — CLI, from inside this folder:

    npx vercel --prod

No build step, no environment variables, no dependencies.

Note: the page must be served over https (or localhost) — browsers only enable
WebCrypto decryption in secure contexts. Vercel serves https by default.
