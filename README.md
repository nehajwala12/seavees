# SeaVees — Consolidated Findings & Recommendations
CreditSwan-branded diligence report. Single static page, no build step.

## Deploy
1. Push this folder to a GitHub repo (files at the repo root).
2. In Vercel: Add New → Project → import the repo.
3. Framework preset: **Other**. Build command: none. Output directory: default.
4. Deploy — the report serves at `/`.

`vercel.json` adds noindex + security headers so the report stays out of search engines.
