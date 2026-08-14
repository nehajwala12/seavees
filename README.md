# SeaVees — Consolidated Findings & Recommendations

Static single-page report. No build step, no dependencies, no framework.

## Deploy to Vercel

**Option A — CLI (fastest)**

```bash
npm i -g vercel      # once
cd seavees-report
vercel               # preview URL
vercel --prod        # production URL
```

Accept the defaults. When asked for a framework preset, choose **Other**. Leave build command and output directory blank — Vercel serves `index.html` directly.

**Option B — Git**

Push this folder to a repo and import it at vercel.com/new. Framework preset **Other**; no build command; output directory `.` (root).

**Option C — Drag and drop**

Zip the folder contents and drop them on vercel.com/new.

## What's in here

| File | Purpose |
|---|---|
| `index.html` | The entire report — HTML, CSS, JS and SVG inline. Only external request is Google Fonts. |
| `vercel.json` | `noindex` plus security headers. No rewrites or redirects. |
| `robots.txt` | Disallow all crawlers. |
| `.vercelignore` | Keeps this README out of the deployment. |

## Access control — read this

The report is marked **Draft for discussion** and carries confidential client figures. `noindex` keeps it out of search results; **it does not make the URL private.** Anyone with the link can read it.

Before sharing outside the immediate team, add protection in the Vercel dashboard:

- **Settings → Deployment Protection → Vercel Authentication** — restricts access to your Vercel team members, or
- **Password Protection** (Pro/Enterprise) — single shared password on the deployment.

## Notes

- Fonts (Cormorant Garamond, Manrope, IBM Plex Mono) load from Google Fonts. If the client's network blocks it, the page falls back to system serif/sans and stays fully legible. To go fully self-contained, download the woff2 files, drop them in `/fonts`, and swap the `<link>` in `<head>` for `@font-face` rules.
- Deep links work: `#p1` … `#p10` open the corresponding tab (e.g. `.../#p10` opens the EBITDA bridge).
- Light/dark toggle, expand-all, full-text search and print are built in and need no configuration.
- Print/PDF: use the **Print** button. Only the open tab prints — open the tab you want first.
