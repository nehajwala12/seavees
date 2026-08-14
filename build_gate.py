#!/usr/bin/env python3
"""Encrypt the SeaVees report and wrap it in a CreditSwan-branded password gate.

AES-256-GCM, key derived by PBKDF2-HMAC-SHA256. The plaintext report never
appears in the deployed file -- only ciphertext. Decryption happens in the
browser via WebCrypto using the password the reader types.
"""
import base64, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SRC   = sys.argv[1] if len(sys.argv) > 1 else "index-plain.html"
DST   = sys.argv[2] if len(sys.argv) > 2 else "index.html"
PASSWORD = "SeaVees2026"
ITERATIONS = 600_000

plaintext = open(SRC, encoding="utf-8").read().encode("utf-8")

salt = os.urandom(16)
iv   = os.urandom(12)
key  = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                  salt=salt, iterations=ITERATIONS).derive(PASSWORD.encode("utf-8"))
blob = AESGCM(key).encrypt(iv, plaintext, None)   # ciphertext || 16-byte tag

payload = {
    "v": 1,
    "kdf": {"name": "PBKDF2", "hash": "SHA-256", "iterations": ITERATIONS,
            "salt": base64.b64encode(salt).decode()},
    "cipher": {"name": "AES-GCM", "iv": base64.b64encode(iv).decode(),
               "tagBits": 128},
    "data": base64.b64encode(blob).decode(),
}

GATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<meta name="referrer" content="no-referrer">
<title>SeaVees &mdash; Findings &amp; Recommendations | CreditSwan</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#16211F; --cream:#F4EFE6; --gold:#A98543; --teal:#1C4A45; --pale:#E9C583;
  --claret:#5C2B2E;
  --ink78:rgba(22,33,31,.78); --ink55:rgba(22,33,31,.55); --ink14:rgba(22,33,31,.14);
  --ink30:rgba(22,33,31,.30);
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--cream);color:var(--ink);
  font-family:'Manrope',system-ui,-apple-system,sans-serif;font-size:15px;line-height:1.6;
  -webkit-font-smoothing:antialiased;display:flex;align-items:center;justify-content:center;padding:26px}
.goldrule{position:fixed;top:0;left:0;right:0;height:5px;background:var(--gold)}
.gate{width:100%;max-width:452px;position:relative}
.gate > *{position:relative;z-index:1}
.swan{position:absolute;z-index:0;bottom:-70px;right:-104px;width:268px;opacity:.045;pointer-events:none}
.mark{display:flex;align-items:center;gap:10px;margin-bottom:34px}
.mark svg{width:30px;height:30px;flex:none}
.mark b{font-family:'Cormorant Garamond',Georgia,serif;font-size:23px;font-weight:600;letter-spacing:-.5px}
.kick{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:500;letter-spacing:.15em;
  text-transform:uppercase;color:var(--teal);margin-bottom:9px}
h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:35px;letter-spacing:-1px;
  line-height:1.08;margin:0 0 12px}
.sub{color:var(--ink78);font-size:14.5px;margin:0 0 28px}
label{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:500;
  letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:7px}
.row{display:flex;gap:8px}
input{flex:1;min-width:0;padding:12px 14px;font-family:'IBM Plex Mono',monospace;font-size:14px;
  color:var(--ink);background:transparent;border:1px solid var(--ink30);border-radius:4px;letter-spacing:.02em}
input::placeholder{color:rgba(22,33,31,.35);letter-spacing:0}
input:focus{outline:none;border-color:var(--gold);box-shadow:inset 0 0 0 1px var(--gold)}
button{padding:12px 22px;font-family:'IBM Plex Mono',monospace;font-size:11.5px;font-weight:500;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ink);background:var(--gold);
  border:none;border-radius:4px;cursor:pointer;white-space:nowrap}
button:hover{background:var(--pale)}
button:disabled{opacity:.5;cursor:default}
.msg{min-height:20px;margin-top:13px;font-family:'IBM Plex Mono',monospace;font-size:12px;
  letter-spacing:.01em;color:var(--claret)}
.msg.busy{color:var(--ink55)}
.foot{margin-top:30px;padding-top:17px;border-top:1px solid var(--ink14);
  font-size:12.5px;color:var(--ink55);line-height:1.55}
.foot b{color:var(--ink78);font-weight:700}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--gold);
  margin-right:8px;vertical-align:middle}
@media (max-width:420px){ .row{flex-direction:column} h1{font-size:29px} .swan{display:none} }
</style></head>
<body>
<div class="goldrule"></div>
<main class="gate">
  <svg class="swan" viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M8 30c0-9 6-16 15-16 4 0 7 1 9 4-2-1-4-1-6 0 3 0 5 2 6 5-4-2-8-1-11 2-3 3-8 4-13 5z" fill="#16211F"/><circle cx="30.5" cy="15.5" r="1.4" fill="#A98543"/></svg>

  <div class="mark">
    <svg viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M8 30c0-9 6-16 15-16 4 0 7 1 9 4-2-1-4-1-6 0 3 0 5 2 6 5-4-2-8-1-11 2-3 3-8 4-13 5z" fill="#16211F"/><circle cx="30.5" cy="15.5" r="1.4" fill="#A98543"/></svg>
    <b>CreditSwan</b>
  </div>

  <div class="kick">Confidential &middot; Draft for discussion</div>
  <h1>SeaVees &mdash; Findings &amp; Recommendations</h1>
  <p class="sub">This report is encrypted. Enter the access password to open it.</p>

  <form id="f" autocomplete="off">
    <label for="pw">Access password</label>
    <div class="row">
      <input id="pw" type="password" placeholder="&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;&bull;"
             autocomplete="current-password" autocapitalize="off" autocorrect="off" spellcheck="false" required>
      <button type="submit" id="go">Open report</button>
    </div>
    <div class="msg" id="msg" role="status" aria-live="polite"></div>
  </form>

  <div class="foot">
    <span class="dot"></span><b>Contents are commercially confidential and not for redistribution.</b>
    Access is limited to named recipients. If you need the password,
    contact your CreditSwan engagement lead.
  </div>
</main>

<script id="payload" type="application/json">__PAYLOAD__</script>
<script>
(function(){
  var P = JSON.parse(document.getElementById('payload').textContent);
  var f = document.getElementById('f'), pw = document.getElementById('pw'),
      go = document.getElementById('go'), msg = document.getElementById('msg');
  var KEY = 'cs.seavees.k';

  function b64(s){ var r = atob(s), a = new Uint8Array(r.length);
    for (var i=0;i<r.length;i++) a[i]=r.charCodeAt(i); return a; }

  function say(t, busy){ msg.textContent = t; msg.className = busy ? 'msg busy' : 'msg'; }

  function open_(html){
    var hash = location.hash;
    document.open(); document.write(html); document.close();
    if (hash) { try { location.hash = hash; } catch(e){} }
  }

  function unlock(pass, quiet){
    if (!window.crypto || !crypto.subtle) {
      say('This browser cannot decrypt the report. Use a current version of Chrome, Safari, Edge or Firefox over https.');
      return Promise.resolve(false);
    }
    go.disabled = true; if (!quiet) say('Decrypting\u2026', true);
    return crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey'])
      .then(function(base){
        return crypto.subtle.deriveKey(
          { name:'PBKDF2', salt:b64(P.kdf.salt), iterations:P.kdf.iterations, hash:P.kdf.hash },
          base, { name:'AES-GCM', length:256 }, false, ['decrypt']);
      })
      .then(function(k){
        return crypto.subtle.decrypt({ name:'AES-GCM', iv:b64(P.cipher.iv), tagLength:P.cipher.tagBits },
                                     k, b64(P.data));
      })
      .then(function(buf){
        try { sessionStorage.setItem(KEY, pass); } catch(e){}
        open_(new TextDecoder().decode(buf));
        return true;
      })
      .catch(function(){
        go.disabled = false;
        try { sessionStorage.removeItem(KEY); } catch(e){}
        if (!quiet) { say('That password is not correct.'); pw.value=''; pw.focus(); }
        else { say(''); }
        return false;
      });
  }

  f.addEventListener('submit', function(e){ e.preventDefault();
    var v = pw.value; if (!v) return; unlock(v, false); });

  // Same-session convenience: reloads and deep links do not re-prompt.
  var saved = null; try { saved = sessionStorage.getItem(KEY); } catch(e){}
  if (saved) { unlock(saved, true); } else { pw.focus(); }
})();
</script>
</body></html>
"""

out = GATE.replace("__PAYLOAD__", json.dumps(payload, separators=(",", ":")))
_d = os.path.dirname(DST)
if _d:
    os.makedirs(_d, exist_ok=True)
open(DST, "w", encoding="utf-8").write(out)

print(f"source plaintext : {len(plaintext):,} bytes")
print(f"ciphertext       : {len(blob):,} bytes")
print(f"gated output     : {len(out):,} bytes -> {DST}")
print(f"PBKDF2 iterations: {ITERATIONS:,}")
