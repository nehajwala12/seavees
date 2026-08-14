# SeaVees report — PRIVATE MASTER COPY

**Do not upload either of these files to a public repository or deploy them.**

| File | What it is |
|---|---|
| `index-plain.html` | The complete report, **unencrypted**. Anyone who opens this URL reads everything with no password. This is the editable source. |
| `build_gate.py` | Encrypts `index-plain.html` into the password-protected `index.html`. |

## Editing the report

The encrypted `index.html` cannot be edited directly. To make changes:

1. Edit `index-plain.html`.
2. Rebuild:
   ```bash
   pip install cryptography
   python3 build_gate.py index-plain.html index.html
   ```
3. Deploy only the resulting `index.html`.

## Changing the password

Edit the `PASSWORD` line near the top of `build_gate.py`, then rebuild as above.
The current password is `SeaVees2026`. A longer passphrase costs the reader nothing
and is meaningfully stronger — e.g. `seavees-harbor-audit-2026`.

## Verifying a build before you deploy it

```bash
grep -c "EBITDA" index.html      # must print 0
grep -c "Casey Bower" index.html # must print 0
```

Any result above 0 means the file is not encrypted. Do not deploy it.
