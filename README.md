# SeaVees — Findings & Recommendations (password-protected)

**Access password: `SeaVees2026`**

Static site. No build step, no dependencies, no framework.

---

## The one rule

`index.html` must sit at the **root of the repository**, not inside a folder.

```
your-repo/
├── index.html        ← must be here
├── vercel.json
└── robots.txt
```

**Not this** — this is what produces `404: NOT_FOUND`:

```
your-repo/
└── some-folder/
    └── index.html    ← Vercel will not find this
```

If your repo already looks like the second one, you don't have to re-upload. In Vercel go to **Settings → Build & Deployment → Root Directory**, enter the folder name, save, and redeploy.

---

## Deploy from GitHub

1. Create a new repository (private is fine — Vercel can read private repos).
2. Upload the three files **individually**: click **Add file → Upload files**, drag `index.html`, `vercel.json` and `robots.txt` in together, and commit. Do not drag a folder.
3. Go to [vercel.com/new](https://vercel.com/new) and import the repo.
4. **Framework Preset: Other.** Leave Build Command, Output Directory and Install Command blank.
5. Deploy.

The whole site is one HTML file, so there is nothing to build. If Vercel offers to auto-detect a framework, decline it — picking a preset like Vite or Next.js makes Vercel look for a build output folder that doesn't exist, which also gives a 404.

## Or deploy from the command line

```bash
npm i -g vercel
cd <folder with these files>
vercel --prod
```

---

## If you still get "not found"

| Symptom | Cause | Fix |
|---|---|---|
| 404 on the root URL | `index.html` is in a subfolder | Move it to the repo root, or set **Root Directory** in Vercel settings |
| 404 on the root URL | A framework preset was selected | Settings → Build & Deployment → Framework Preset → **Other**, clear Output Directory, redeploy |
| 404, and the build log mentions a missing directory | Output Directory is set | Clear it, redeploy |
| Page loads but the password box does nothing | Site opened over `file://` | Must be served over https — Vercel does this automatically |
| Deployment succeeded but shows an old version | Vercel cached the previous build | Deployments → ⋯ → Redeploy, with cache disabled |

To confirm what actually deployed, open the Vercel deployment and click **Source** — you'll see the exact file tree Vercel is serving.

---

## What's in here

| File | Required | Purpose |
|---|---|---|
| `index.html` | **Yes** | Password gate plus the encrypted report. The whole site. |
| `vercel.json` | Optional | `noindex` and security headers. Deleting it does not break the site. |
| `robots.txt` | Optional | Keeps crawlers away. |

There is deliberately **no `package.json`** — adding one would make Vercel try to run a build.

There are deliberately **no dotfiles**. GitHub's web uploader silently skips files beginning with `.`, so nothing here depends on one arriving.

**The unencrypted master copy is not in this folder.** It ships separately, so it cannot be uploaded to a public repo by accident. Keep it private — it is the editable source, and the encrypted file cannot be edited directly.

---

## How the protection works

The report is encrypted with **AES-256-GCM**, key derived from the password by **PBKDF2-HMAC-SHA256 at 600,000 iterations** over a random salt. The deployed file contains ciphertext only. Viewing source, opening devtools or disabling JavaScript reveals nothing — the plaintext is not in the file. Unlock takes about half a second.

**The password is the whole of the security.** Anyone given it has the report permanently. Someone who downloads the file can brute-force it offline with no rate limiting, and `SeaVees2026` is a guessable brand-plus-year password. The iterations make each guess slow; they do not make a predictable password safe.

For a client convenience gate that is a fair trade. If the report needs to be genuinely locked down, also switch on **Vercel Settings → Deployment Protection → Vercel Authentication** — that stops the file being downloaded at all.

To change the password, edit `PASSWORD` in `build_gate.py` (shipped with the master copy) and rebuild:

```bash
pip install cryptography
python3 build_gate.py index-plain.html index.html
```

A longer passphrase costs the reader nothing: `seavees-harbor-audit-2026` is far stronger and just as easy to paste into an email.

---

## Reader experience

- Password prompt on first visit; **Enter** submits. Wrong password shows an error and clears the field.
- Unlocking lasts for the browser session only. Reloads and deep links don't re-prompt; closing the tab clears it. No cookies, no permanent storage.
- Deep links work through the gate: `.../#p10` prompts, then opens the EBITDA bridge tab.
- Light/dark toggle, search, expand-all and print all work after unlock.
- Print/PDF prints only the open tab — open the tab you want first.
- Responsive to 390px.
