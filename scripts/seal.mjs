#!/usr/bin/env node
// The Jersey City Sound — "Sealed in the Record" offline signer.
// Implements RECORD-SEAL-SPEC.md v1.0. Runs locally at authoring time only.
// No network, no wallets, no contracts. Ed25519 via Node native crypto.
//
// Modes:  keygen | seal <slug> | reseal <slug> | revoke <slug> --reason "..."
//         | seal-tier | verify-all | anchor
// <slug> is the entry filename without extension, e.g. entry-roy-hamilton.
import {
  readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync,
  statSync, chmodSync, readdirSync,
} from 'node:fs';
import { createHash, sign as edSign, verify as edVerify, generateKeyPairSync, createPublicKey, createPrivateKey } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { parse as parseHTML } from 'node-html-parser';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DESIGN = join(ROOT, 'design');
const DOMAIN = 'https://jerseycitysound.com';
const DID = 'did:web:jerseycitysound.com';
const VM = DID + '#seal-2026-1';
const KEY_PATH = process.env.SEAL_KEY_PATH || join(ROOT, 'keys', 'seal-ed25519.key');
const LEDGER = join(DESIGN, 'ledger', 'seals.jsonl');
const ANCHORS = join(DESIGN, 'ledger', 'anchors.json');
const CRED_DIR = join(DESIGN, 'credentials');
const DIDDOC = join(DESIGN, '.well-known', 'did.json');
const CHART_PATH = join(ROOT, 'data', 'chart-data.json');
const ENTRIES_PATH = join(ROOT, 'data', 'entries.json');
const ZERO64 = '0'.repeat(64);

// ---------- hashing ----------
const sha256hex = (buf) => createHash('sha256').update(buf).digest('hex');
const sha256bytes = (buf) => createHash('sha256').update(buf).digest();

// ---------- JCS (RFC 8785) for JSON without floats ----------
// Recursively sort object keys (UTF-16 order), then JSON.stringify (compact).
// For our data (strings, integers, booleans, null, arrays, objects) this is
// byte-identical to RFC 8785. Locked by test/jcs-vectors.json.
function jcsCanon(v) {
  if (v === null || typeof v !== 'object') return v;
  if (Array.isArray(v)) return v.map(jcsCanon);
  const out = {};
  for (const k of Object.keys(v).sort()) out[k] = jcsCanon(v[k]);
  return out;
}
const jcs = (v) => JSON.stringify(jcsCanon(v));

// ---------- base58btc ----------
const B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
function base58encode(bytes) {
  let zeros = 0;
  while (zeros < bytes.length && bytes[zeros] === 0) zeros++;
  const digits = [0];
  for (let i = zeros; i < bytes.length; i++) {
    let carry = bytes[i];
    for (let j = 0; j < digits.length; j++) {
      carry += digits[j] << 8;
      digits[j] = carry % 58;
      carry = (carry / 58) | 0;
    }
    while (carry) { digits.push(carry % 58); carry = (carry / 58) | 0; }
  }
  let out = '1'.repeat(zeros);
  for (let i = digits.length - 1; i >= 0; i--) out += B58[digits[i]];
  return out;
}
function base58decode(str) {
  const map = {};
  for (let i = 0; i < B58.length; i++) map[B58[i]] = i;
  let zeros = 0;
  while (zeros < str.length && str[zeros] === '1') zeros++;
  const bytes = [0];
  for (let i = zeros; i < str.length; i++) {
    let carry = map[str[i]];
    if (carry === undefined) throw new Error('invalid base58 char: ' + str[i]);
    for (let j = 0; j < bytes.length; j++) {
      carry += bytes[j] * 58;
      bytes[j] = carry & 0xff;
      carry >>= 8;
    }
    while (carry) { bytes.push(carry & 0xff); carry >>= 8; }
  }
  const out = Buffer.alloc(zeros + bytes.length);
  for (let i = 0; i < bytes.length; i++) out[zeros + bytes.length - 1 - i] = bytes[i];
  return out;
}
const multibase58 = (bytes) => 'z' + base58encode(bytes);
const unmultibase58 = (str) => {
  if (str[0] !== 'z') throw new Error('unsupported multibase prefix');
  return base58decode(str.slice(1));
};

// ---------- keys ----------
const PKCS8_PREFIX = Buffer.from('302e020100300506032b657004220420', 'hex');
function seedToPrivateKey(seed) {
  return createPrivateKey({ key: Buffer.concat([PKCS8_PREFIX, seed]), format: 'der', type: 'pkcs8' });
}
function rawPubFromPrivate(priv) {
  const jwk = createPublicKey(priv).export({ format: 'jwk' });
  return Buffer.from(jwk.x, 'base64url');
}
function pubToMultikey(rawPub) {
  return multibase58(Buffer.concat([Buffer.from([0xed, 0x01]), rawPub]));
}
function multikeyToPub(mk) {
  const raw = unmultibase58(mk);
  if (raw[0] !== 0xed || raw[1] !== 0x01) throw new Error('not an ed25519 multikey');
  return raw.subarray(2);
}
function loadKey() {
  if (!existsSync(KEY_PATH)) throw new Error(`key not found at ${KEY_PATH} (run: node seal.mjs keygen)`);
  // Unix permission check (spec §4). NTFS has no Unix mode bits — Node reports
  // 0666 regardless — so this guard only applies on non-Windows platforms.
  if (process.platform !== 'win32') {
    const mode = statSync(KEY_PATH).mode & 0o777;
    if (mode & 0o077) throw new Error(`refusing to use key ${KEY_PATH}: mode ${mode.toString(8)} is group/world accessible; chmod 600 it`);
  }
  const seed = Buffer.from(readFileSync(KEY_PATH, 'utf8').trim(), 'hex');
  if (seed.length !== 32) throw new Error('key must be 64 hex chars (32-byte seed)');
  const priv = seedToPrivateKey(seed);
  return { priv, rawPub: rawPubFromPrivate(priv) };
}

// ---------- pageHash (§1a) ----------
function pageHash(html) {
  const doc = parseHTML(html, { comment: false, blockTextElements: { script: true, style: true } });
  const article = doc.querySelector('article');
  if (!article) throw new Error('no <article> element in page');
  for (const sel of ['script', 'style', 'form', '[data-noseal]']) {
    for (const el of article.querySelectorAll(sel)) el.remove();
  }
  let text = article.textContent;
  text = text.normalize('NFC').replace(/\s+/gu, ' ').trim();
  return sha256hex(Buffer.from(text, 'utf8'));
}

// ---------- credential signing (§2, eddsa-jcs-2022) ----------
function buildCredential(slug, name, record, phash, nowISO, priv) {
  const unsecured = {
    '@context': ['https://www.w3.org/ns/credentials/v2'],
    id: `${DOMAIN}/credentials/${slug}.vc.json`,
    type: ['VerifiableCredential', 'ArchiveRecordAttestation'],
    issuer: DID,
    validFrom: nowISO,
    credentialSubject: {
      id: `${DOMAIN}/${slug}.html#main`,
      name,
      entry: slug,
      pageHash: phash,
      record,
    },
  };
  const proofOptionsBase = {
    type: 'DataIntegrityProof',
    cryptosuite: 'eddsa-jcs-2022',
    created: nowISO,
    verificationMethod: VM,
    proofPurpose: 'assertionMethod',
  };
  const proofOptions = { '@context': unsecured['@context'], ...proofOptionsBase };
  const hashData = Buffer.concat([
    sha256bytes(Buffer.from(jcs(proofOptions), 'utf8')),   // proof options hash FIRST
    sha256bytes(Buffer.from(jcs(unsecured), 'utf8')),
  ]);
  const sig = edSign(null, hashData, priv);               // 64-byte Ed25519 signature
  const proof = { ...proofOptionsBase, proofValue: multibase58(sig) };
  return { ...unsecured, proof };
}

function verifyCredential(cred, rawPub) {
  const { proof, ...unsecured } = cred;
  const { proofValue, ...proofRest } = proof;
  const proofOptions = { '@context': unsecured['@context'], ...proofRest };
  const hashData = Buffer.concat([
    sha256bytes(Buffer.from(jcs(proofOptions), 'utf8')),
    sha256bytes(Buffer.from(jcs(unsecured), 'utf8')),
  ]);
  const sig = unmultibase58(proofValue);
  return edVerify(null, hashData, createPublicKey(seedToPubKeyObject(rawPub)), sig);
}
function seedToPubKeyObject(rawPub) {
  return { key: { kty: 'OKP', crv: 'Ed25519', x: Buffer.from(rawPub).toString('base64url') }, format: 'jwk' };
}

// ---------- ledger (§3) ----------
function readLedger() {
  if (!existsSync(LEDGER)) return [];
  return readFileSync(LEDGER, 'utf8').split('\n').filter((l) => l.length).map((l) => JSON.parse(l));
}
function lineHashOf(obj) {
  const { lineHash, ...rest } = obj;
  return sha256hex(Buffer.from(jcs(rest), 'utf8'));
}
function appendLine(obj) {
  obj.lineHash = lineHashOf(obj);
  appendFileSync(LEDGER, JSON.stringify(obj) + '\n', 'utf8');
  return obj;
}

// ---------- data lookups ----------
function loadChart() { return JSON.parse(readFileSync(CHART_PATH, 'utf8')); }
function nameForSlug(slug) {
  const entrySlug = slug.replace(/^entry-/, '');
  if (entrySlug === 'dj-dx') return 'DJ DX';
  const entries = JSON.parse(readFileSync(ENTRIES_PATH, 'utf8')).entries;
  const e = entries.find((x) => x.slug === entrySlug);
  return e ? e.name : entrySlug;
}
const nowISO = () => new Date().toISOString().replace(/\.\d+Z$/, 'Z');

// ---------- mkdirs ----------
function ensureDirs() {
  for (const d of [CRED_DIR, dirname(LEDGER), dirname(DIDDOC)]) if (!existsSync(d)) mkdirSync(d, { recursive: true });
}

// ==================== MODES ====================
function keygen() {
  const kp = generateKeyPairSync('ed25519');
  const seed = Buffer.from(kp.privateKey.export({ format: 'jwk' }).d, 'base64url');
  const rawPub = rawPubFromPrivate(kp.privateKey);
  const keyDir = dirname(KEY_PATH);
  if (!existsSync(keyDir)) mkdirSync(keyDir, { recursive: true });
  if (existsSync(KEY_PATH)) throw new Error(`key already exists at ${KEY_PATH}; refusing to overwrite`);
  writeFileSync(KEY_PATH, seed.toString('hex') + '\n', { mode: 0o600 });
  chmodSync(KEY_PATH, 0o600);
  const mk = pubToMultikey(rawPub);
  const did = {
    '@context': ['https://www.w3.org/ns/did/v1', 'https://w3id.org/security/multikey/v1'],
    id: DID,
    verificationMethod: [{ id: VM, type: 'Multikey', controller: DID, publicKeyMultibase: mk }],
    assertionMethod: [VM],
  };
  ensureDirs();
  writeFileSync(DIDDOC, JSON.stringify(did, null, 2) + '\n');
  console.log(`key written: ${KEY_PATH} (mode 600)`);
  console.log(`publicKeyMultibase: ${mk}`);
  console.log(`did.json written: ${DIDDOC}`);
  // genesis line
  if (readLedger().length === 0) {
    appendLine({ v: 1, seq: 0, ts: nowISO(), event: 'genesis', entry: null, pageHash: null, credential: null, credentialHash: null, prev: ZERO64, note: `key ${VM}` });
    console.log('genesis line written to ledger');
  }
}

function sealEntry(slug, event = 'seal', reason = null) {
  ensureDirs();
  const chart = loadChart();
  const key = `${slug}.html`;
  if (!(key in chart)) throw new Error(`GATE: no chart-data.json record for ${key}; refusing to seal (no rows, no seal)`);
  const record = chart[key];
  const htmlPath = join(DESIGN, `${slug}.html`);
  if (!existsSync(htmlPath)) throw new Error(`page not found: ${htmlPath}`);
  const ledger = readLedger();
  if (ledger.length === 0) throw new Error('no genesis line; run keygen first');
  const prior = ledger.filter((l) => l.entry === slug && (l.event === 'seal' || l.event === 'reseal'));
  if (event === 'reseal' && prior.length === 0) throw new Error(`cannot reseal ${slug}: never sealed`);
  if (event === 'seal' && prior.length > 0) throw new Error(`${slug} already sealed; use reseal`);

  const { priv, rawPub } = loadKey();
  const phash = pageHash(readFileSync(htmlPath, 'utf8'));
  const ts = nowISO();
  const cred = buildCredential(slug, nameForSlug(slug), record, phash, ts, priv);
  if (!verifyCredential(cred, rawPub)) throw new Error('self-verify failed after signing');
  writeFileSync(join(CRED_DIR, `${slug}.vc.json`), JSON.stringify(cred, null, 2) + '\n');
  const credentialHash = sha256hex(Buffer.from(jcs(cred), 'utf8'));
  const last = ledger[ledger.length - 1];
  const line = appendLine({ v: 1, seq: last.seq + 1, ts, event, entry: slug, pageHash: phash, credential: `credentials/${slug}.vc.json`, credentialHash, prev: last.lineHash });
  console.log(`${event}: ${slug}  seq ${line.seq}  pageHash ${phash.slice(0, 12)}…  cred ${credentialHash.slice(0, 12)}…`);
}

function revokeEntry(slug, reason) {
  ensureDirs();
  const ledger = readLedger();
  const prior = ledger.filter((l) => l.entry === slug && (l.event === 'seal' || l.event === 'reseal'));
  if (prior.length === 0) throw new Error(`cannot revoke ${slug}: never sealed`);
  const last = ledger[ledger.length - 1];
  const line = appendLine({ v: 1, seq: last.seq + 1, ts: nowISO(), event: 'revoke', entry: slug, pageHash: null, credential: `credentials/${slug}.vc.json`, credentialHash: prior[prior.length - 1].credentialHash, prev: last.lineHash, note: reason || null });
  console.log(`revoke: ${slug}  seq ${line.seq}  reason: ${reason || '(none)'}`);
}

function sealTier() {
  const chart = loadChart();
  const ledger = readLedger();
  const sealed = new Set(ledger.filter((l) => l.event === 'seal' || l.event === 'reseal').map((l) => l.entry));
  const todo = Object.entries(chart)
    .filter(([, r]) => r.render)          // "complete rows" = render:true (has real facts/medallions)
    .map(([k]) => k.replace(/\.html$/, ''))
    .filter((slug) => !sealed.has(slug));
  if (!todo.length) { console.log('seal-tier: nothing to seal (all render:true records already sealed)'); return; }
  console.log(`seal-tier: sealing ${todo.length} charted entries…`);
  for (const slug of todo) sealEntry(slug, 'seal');
  console.log('seal-tier: done');
}

function verifyAll() {
  let fail = 0;
  const say = (ok, msg) => { console.log(`${ok ? '  ok ' : ' FAIL'}  ${msg}`); if (!ok) fail++; };
  // JCS test vectors
  const vecPath = join(ROOT, 'test', 'jcs-vectors.json');
  if (existsSync(vecPath)) {
    const vecs = JSON.parse(readFileSync(vecPath, 'utf8'));
    for (const v of vecs) say(jcs(v.input) === v.canonical, `jcs vector: ${v.name}`);
  } else say(false, 'test/jcs-vectors.json missing');

  const did = JSON.parse(readFileSync(DIDDOC, 'utf8'));
  const rawPub = multikeyToPub(did.verificationMethod[0].publicKeyMultibase);
  const chart = loadChart();
  const ledger = readLedger();

  // Chain replay (check 5)
  let chainOk = true;
  for (let i = 0; i < ledger.length; i++) {
    const l = ledger[i];
    if (l.seq !== i) chainOk = false;
    if (i === 0) { if (l.event !== 'genesis' || l.prev !== ZERO64) chainOk = false; }
    else if (l.prev !== ledger[i - 1].lineHash) chainOk = false;
    if (lineHashOf(l) !== l.lineHash) chainOk = false;
  }
  say(chainOk, `ledger chain replay (${ledger.length} lines)`);

  // Latest seal/reseal per entry -> checks 1,2,4
  const latest = {};
  for (const l of ledger) if (l.event === 'seal' || l.event === 'reseal') latest[l.entry] = l;
    else if (l.event === 'revoke') delete latest[l.entry];
  for (const [slug, l] of Object.entries(latest)) {
    const cred = JSON.parse(readFileSync(join(DESIGN, l.credential), 'utf8'));
    say(verifyCredential(cred, rawPub), `signature: ${slug}`);
    const phash = pageHash(readFileSync(join(DESIGN, `${slug}.html`), 'utf8'));
    say(phash === cred.credentialSubject.pageHash && phash === l.pageHash, `pageHash: ${slug}`);
    say(sha256hex(Buffer.from(jcs(cred), 'utf8')) === l.credentialHash, `credentialHash: ${slug}`);
    say(JSON.stringify(cred.credentialSubject.record) === JSON.stringify(chart[`${slug}.html`]), `record matches live ledger: ${slug}`);
  }
  console.log(fail ? `\nverify-all: ${fail} FAILURE(S)` : `\nverify-all: all checks passed`);
  process.exit(fail ? 1 : 0);
}

function anchor() {
  const ledger = readLedger();
  const head = ledger[ledger.length - 1];
  console.log(`date: ${nowISO().slice(0, 10)}`);
  console.log(`seq:  ${head.seq}`);
  console.log(`head: ${head.lineHash}`);
  console.log(`\nX post text:\n  Record Seal head, seq ${head.seq}: ${head.lineHash}`);
  console.log(`\nSteps: 1) Wayback-snapshot ${DOMAIN}/ledger/seals.jsonl  2) post the head from @jerseycitysound  3) (optional) OpenTimestamps  4) add an entry to ${ANCHORS} and commit.`);
}

// ==================== CLI ====================
const [mode, arg, ...rest] = process.argv.slice(2);
try {
  if (mode === 'keygen') keygen();
  else if (mode === 'seal') sealEntry(arg, 'seal');
  else if (mode === 'reseal') sealEntry(arg, 'reseal');
  else if (mode === 'revoke') { const ri = rest.indexOf('--reason'); revokeEntry(arg, ri >= 0 ? rest[ri + 1] : null); }
  else if (mode === 'seal-tier') sealTier();
  else if (mode === 'verify-all') verifyAll();
  else if (mode === 'anchor') anchor();
  else { console.log('usage: node seal.mjs keygen | seal <slug> | reseal <slug> | revoke <slug> --reason "..." | seal-tier | verify-all | anchor'); process.exit(2); }
} catch (e) {
  console.error('ERROR:', e.message);
  process.exit(1);
}
