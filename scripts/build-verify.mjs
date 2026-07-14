// Build design/verify.html: the client-side "Sealed in the Record" verifier.
// Vendors @noble/ed25519 inline (no CDN), plus an inline JCS/base58/pageHash
// identical to the signer. Re-run after the signer or the chrome changes.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DESIGN = join(ROOT, 'design');
const NOBLE = readFileSync(join(ROOT, 'scripts', 'node_modules', '@noble', 'ed25519', 'index.js'), 'utf8');
const PINNED = JSON.parse(readFileSync(join(DESIGN, '.well-known', 'did.json'), 'utf8'))
  .verificationMethod[0].publicKeyMultibase;

// Reuse the site chrome from an existing generated light page.
const about = readFileSync(join(DESIGN, 'about.html'), 'utf8');
const grab = (re) => (about.match(re) || [''])[0];
const masthead = grab(/<header class="masthead[\s\S]*?<\/header>/).replace(/ aria-current="page"/g, '');
const footer = grab(/<footer class="footer[\s\S]*?<\/footer>/);

// ---- the verifier module (browser). JCS + pageHash are byte-identical to the signer. ----
const VERIFIER = `
const PINNED_KEY = ${JSON.stringify(PINNED)};
const DID = 'did:web:jerseycitysound.com';

function jcsCanon(v){ if(v===null||typeof v!=='object')return v; if(Array.isArray(v))return v.map(jcsCanon); const o={}; for(const k of Object.keys(v).sort())o[k]=jcsCanon(v[k]); return o; }
const jcs=(v)=>JSON.stringify(jcsCanon(v));

const B58='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
function base58decode(str){ const map={}; for(let i=0;i<B58.length;i++)map[B58[i]]=i; let zeros=0; while(zeros<str.length&&str[zeros]==='1')zeros++; const bytes=[0]; for(let i=zeros;i<str.length;i++){ let carry=map[str[i]]; if(carry===undefined)throw new Error('bad base58'); for(let j=0;j<bytes.length;j++){carry+=bytes[j]*58;bytes[j]=carry&255;carry>>=8;} while(carry){bytes.push(carry&255);carry>>=8;} } const out=new Uint8Array(zeros+bytes.length); for(let i=0;i<bytes.length;i++)out[zeros+bytes.length-1-i]=bytes[i]; return out; }
const unmb=(s)=>{ if(s[0]!=='z')throw new Error('bad multibase'); return base58decode(s.slice(1)); };
function multikeyToPub(mk){ const raw=unmb(mk); if(raw[0]!==0xed||raw[1]!==0x01)throw new Error('not ed25519 multikey'); return raw.slice(2); }

const enc=(s)=>new TextEncoder().encode(s);
async function sha256hex(bytes){ const b=await crypto.subtle.digest('SHA-256',bytes); return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join(''); }
async function sha256bytes(bytes){ return new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)); }

async function pageHash(html){ const doc=new DOMParser().parseFromString(html,'text/html'); const art=doc.querySelector('article'); if(!art)throw new Error('no <article> in page'); art.querySelectorAll('script, style, form, [data-noseal]').forEach(e=>e.remove()); let t=art.textContent.normalize('NFC').replace(/\\s+/gu,' ').trim(); return sha256hex(enc(t)); }

async function verifyCredential(cred, rawPub){
  const { proof, ...unsecured } = cred;
  const { proofValue, ...proofRest } = proof;
  const proofOptions = { '@context': unsecured['@context'], ...proofRest };
  const hashData = new Uint8Array(64);
  hashData.set(await sha256bytes(enc(jcs(proofOptions))), 0);
  hashData.set(await sha256bytes(enc(jcs(unsecured))), 32);
  return verifyAsync(unmb(proofValue), hashData, rawPub);   // @noble, vendored above
}
async function lineHashOf(obj){ const { lineHash, ...rest } = obj; return sha256hex(enc(jcs(rest))); }

async function jget(u){ const r=await fetch(u,{cache:'no-store'}); if(!r.ok)throw new Error('fetch '+u+' → '+r.status); return r.json(); }
async function tget(u){ const r=await fetch(u,{cache:'no-store'}); if(!r.ok)throw new Error('fetch '+u+' → '+r.status); return r.text(); }
async function getLedger(){ return (await tget('/ledger/seals.jsonl')).split('\\n').filter(l=>l.length).map(l=>JSON.parse(l)); }

const out = document.getElementById('verify-out');
const row = (ok, label, detail) => {
  const d = document.createElement('div');
  d.className = 'vrow ' + (ok===true?'vrow--ok':ok===false?'vrow--fail':'vrow--info');
  d.innerHTML = '<span class="vrow__mark">'+(ok===true?'✓':ok===false?'✕':'·')+'</span><span class="vrow__label">'+label+'</span><span class="vrow__detail">'+(detail||'')+'</span>';
  out.appendChild(d);
  return ok;
};
const esc = (s)=>String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));

async function chainReplay(ledger){
  const ZERO='0'.repeat(64);
  for(let i=0;i<ledger.length;i++){ const l=ledger[i];
    if(l.seq!==i) return {ok:false, at:i, why:'seq'};
    if(i===0){ if(l.event!=='genesis'||l.prev!==ZERO) return {ok:false, at:0, why:'genesis'}; }
    else if(l.prev!==ledger[i-1].lineHash) return {ok:false, at:i, why:'prev'};
    if(await lineHashOf(l)!==l.lineHash) return {ok:false, at:i, why:'lineHash'};
  }
  return {ok:true};
}

async function verifyEntry(slug){
  out.innerHTML='';
  let did, rawPub, pinnedPub, mismatch=false;
  try{
    did = await jget('/.well-known/did.json');
    const mk = did.verificationMethod[0].publicKeyMultibase;
    rawPub = multikeyToPub(mk); pinnedPub = multikeyToPub(PINNED_KEY);
    mismatch = mk !== PINNED_KEY;
  }catch(e){ row(false,'DID document','could not load /.well-known/did.json: '+esc(e.message)); return; }
  if(mismatch) row(null,'Key notice','the served DID key differs from the pinned key; a hostile mirror could do this. External anchors are the backstop.');

  let cred;
  try{ cred = await jget('/credentials/'+slug+'.vc.json'); }
  catch(e){ row(false,'Credential','no credential for this entry: '+esc(e.message)); return; }

  // 1. Signature (against DID key; and pinned key)
  const sigDid = await verifyCredential(cred, rawPub).catch(()=>false);
  const sigPin = await verifyCredential(cred, pinnedPub).catch(()=>false);
  row(sigDid && sigPin, 'Signature', sigDid&&sigPin ? 'Ed25519 proof verifies against the archive key' : 'signature did NOT verify');

  // 2. Page integrity
  let liveHash='';
  try{ const html = await tget('/'+slug+'.html'); liveHash = await pageHash(html); }catch(e){ row(false,'Page integrity','could not read the live page: '+esc(e.message)); }
  row(liveHash===cred.credentialSubject.pageHash, 'Page integrity', liveHash===cred.credentialSubject.pageHash ? 'the live page text matches the sealed hash' : 'the page text has changed since sealing');

  // 4. Ledger
  const ledger = await getLedger();
  const mine = ledger.filter(l=>l.entry===slug && (l.event==='seal'||l.event==='reseal'));
  const revoked = ledger.some(l=>l.entry===slug && l.event==='revoke') && !(mine.length && ledger.filter(l=>l.entry===slug).slice(-1)[0].event!=='revoke');
  const last = mine[mine.length-1];
  const credHash = await sha256hex(enc(jcs(cred)));
  row(!!last && last.credentialHash===credHash && last.pageHash===cred.credentialSubject.pageHash, 'Ledger', last ? 'the seal ledger records this exact credential (seq '+last.seq+', '+esc(last.ts.slice(0,10))+', '+esc(last.event)+')' : 'no seal line for this entry');
  if(revoked) row(false,'Revocation','this credential has been REVOKED in the ledger');

  // 3. Facts integrity (informational)
  try{
    const chart = await jget('/data/chart-data.json');
    const same = JSON.stringify(chart[slug+'.html']) === JSON.stringify(cred.credentialSubject.record);
    row(null, 'Facts', same ? 'the sealed chart facts are unchanged since sealing' : 'the chart facts have been updated since sealing (a reseal is pending)');
  }catch(e){ /* optional */ }

  // 5. Chain
  const cr = await chainReplay(ledger);
  row(cr.ok, 'Seal chain', cr.ok ? 'the full hash-chained ledger ('+ledger.length+' lines) replays cleanly from genesis' : 'chain broke at line '+cr.at+' ('+cr.why+')');

  // 6. Anchor (informational)
  try{
    const anchors = await jget('/ledger/anchors.json');
    if(anchors.length){ const a=anchors[anchors.length-1]; const headOk = ledger[a.seq] && ledger[a.seq].lineHash===a.head;
      row(null,'External anchor', (headOk?'anchored ':'anchor MISMATCH ')+esc(a.date)+' · seq '+a.seq+(a.wayback?' · <a href="'+esc(a.wayback)+'">Wayback</a>':'')+(a.x?' · <a href="'+esc(a.x)+'">X</a>':''));
    } else row(null,'External anchor','no anchor recorded yet (first anchor pending)');
  }catch(e){}

  const head=document.getElementById('vhead');
  head.textContent = (sigDid&&liveHash===cred.credentialSubject.pageHash&&cr.ok&&!revoked) ? 'Sealed and verified: '+cred.credentialSubject.name : 'Verification found a problem: '+cred.credentialSubject.name;
}

async function verifyChain(){
  out.innerHTML='';
  document.getElementById('vhead').textContent='The seal ledger';
  const ledger = await getLedger();
  const cr = await chainReplay(ledger);
  row(cr.ok, 'Seal chain', cr.ok ? 'the full hash-chained ledger ('+ledger.length+' lines) replays cleanly from genesis' : 'chain broke at line '+cr.at+' ('+cr.why+')');
  const latest={};
  for(const l of ledger){ if(l.event==='seal'||l.event==='reseal') latest[l.entry]=l; else if(l.event==='revoke') delete latest[l.entry]; }
  const entries=Object.values(latest).sort((a,b)=>a.entry.localeCompare(b.entry));
  row(null, 'Sealed records', entries.length+' entries currently sealed');
  const list=document.createElement('div'); list.className='vlist';
  for(const l of entries){ const a=document.createElement('a'); a.href='verify.html?entry='+encodeURIComponent(l.entry); a.className='vlist__item';
    a.innerHTML='<span>'+esc(l.entry.replace(/^entry-/,''))+'</span><span class="vlist__date">'+esc(l.event)+' · '+esc(l.ts.slice(0,10))+'</span>'; list.appendChild(a); }
  out.appendChild(list);
}

const params = new URLSearchParams(location.search);
const entry = params.get('entry');
(entry ? verifyEntry(entry) : verifyChain()).catch(e=>{ out.innerHTML=''; row(false,'Error', esc(e.message)); });
`;

const STYLE = `<style>
.vrow{display:grid;grid-template-columns:1.6rem 9rem 1fr;gap:0.9rem;align-items:baseline;padding:0.8rem 0;border-top:1px solid var(--rule);line-height:1.5;}
.vrow:first-child{border-top:0;}
.vrow__mark{font-size:1.1rem;text-align:center;}
.vrow--ok .vrow__mark{color:#2e7d32;} .vrow--fail .vrow__mark{color:#a3352b;} .vrow--info .vrow__mark{color:var(--gold-ink);}
.vrow--fail{color:#a3352b;}
.vrow__label{font-family:var(--caps);font-size:var(--t-xs);text-transform:uppercase;letter-spacing:0.12em;color:#6b6557;}
.vrow__detail{color:#423e34;}
.vlist{display:flex;flex-direction:column;gap:0.4rem;margin-top:1rem;}
.vlist__item{display:flex;justify-content:space-between;gap:1rem;padding:0.6rem 0.9rem;border:1px solid var(--rule);text-decoration:none;color:var(--ink);}
.vlist__item:hover{border-color:var(--gold-mid);}
.vlist__date{color:#8a8474;font-size:var(--t-sm);}
@media (max-width:620px){.vrow{grid-template-columns:1.4rem 1fr;} .vrow__detail{grid-column:2;}}
</style>`;

const body = `<main class="wrap" style="max-width:60rem;">
  <header class="entry-header">
    <span class="entry-no">Sealed in the Record</span>
    <h1 id="vhead">Verifying…</h1>
    <p class="descriptor">This page checks an archive record against The Jersey City Sound's cryptographic seal, entirely in your browser. Nothing is sent anywhere. The seal proves <em>integrity and provenance</em> — that the page and its cited facts are unchanged since the archive signed them. It does not prove the facts are true; that is the cite-or-cut standard's job.</p>
  </header>
  <div id="verify-out">Verifying…</div>
  <section class="section wrap" style="padding-left:0;padding-right:0;">
    <div class="section__head"><h2 class="caps caps--wide">How this works</h2></div>
    <p style="max-width:64ch;color:#4a4636;">The archive holds one <code>did:web</code> identity and an Ed25519 signing key. Each sealed entry gets a W3C Verifiable Credential binding a hash of the page text to its chart-facts record. Every seal is written to an append-only, hash-chained ledger whose head is periodically anchored on the public web (Internet Archive and X). To verify, this page fetches the credential, re-hashes the live page, checks the signature against the published key, and replays the chain. A hostile copy of the site could alter this verifier itself, which is why the external anchors are the ultimate backstop. See the <a href="/ledger/seals.jsonl">seal ledger</a> and <a href="/.well-known/did.json">DID document</a>.</p>
  </section>
</main>`;

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Verify a Sealed Record | The Jersey City Sound</title>
<meta name="description" content="Verify an archive record against The Jersey City Sound's cryptographic seal, entirely in your browser. Proves the page and its cited facts are unchanged since sealing.">
<meta name="robots" content="index, follow">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32">
<link rel="icon" href="assets/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<link rel="stylesheet" href="styles.css">
${STYLE}
</head>
<body>

${masthead}

${body}

${footer}

<script type="module">
${NOBLE}
${VERIFIER}
</script>
</body>
</html>
`;

writeFileSync(join(DESIGN, 'verify.html'), html);
console.log('wrote design/verify.html  (pinned key ' + PINNED.slice(0, 12) + '… , @noble ' + NOBLE.length + ' bytes inlined)');
