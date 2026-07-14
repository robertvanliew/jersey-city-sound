# Record-Seal tooling

Implements **RECORD-SEAL-SPEC.md v1.0** — "Sealed in the Record" verifiable credentials.
Offline signing, client-side verification. No wallets, no contracts, no server.

## Files it produces (all under `design/`, the web root)

| Artifact | Path |
|---|---|
| DID document | `design/.well-known/did.json` |
| Per-entry credential | `design/credentials/{entry}.vc.json` |
| Seal ledger (hash-chained) | `design/ledger/seals.jsonl` |
| Anchor record | `design/ledger/anchors.json` |
| Verifier (client-side) | `design/verify.html` |
| Served fact ledger | `design/data/chart-data.json` (copied by the generator) |
| Private key | `keys/seal-ed25519.key` — **gitignored, never commit** |

## Signer: `node scripts/seal.mjs <mode>`

- `keygen` — one-time key ceremony. Writes the key (mode 600 on Unix), `did.json`, and the genesis ledger line. Prints the `publicKeyMultibase`.
- `seal <entry>` — seal one entry (e.g. `seal entry-roy-hamilton`). Gated: refuses unless the entry has a row in `data/chart-data.json`.
- `reseal <entry>` — after a legitimate content/fact change. New pageHash + credential; ledger preserves history.
- `revoke <entry> --reason "..."` — retract a credential issued in error.
- `seal-tier` — seal every `render:true` chart-data entry not yet sealed.
- `verify-all` — run all verifier checks (chain, signatures, pageHash, credentialHash, record match) + JCS test vectors in Node. **Run before every deploy.** Exits nonzero on any failure.
- `anchor` — print the current chain head and the X post text for the monthly anchor.

## Verifier build: `node scripts/build-verify.mjs`

Rebuilds `design/verify.html`, vendoring `@noble/ed25519` inline and pinning the current DID key.
Re-run after `keygen` (new key) or after the site chrome changes.

## Standard build order (after editing content)

```
py execution/generate_entry_pages.py     # 1. render pages (+ copy chart-data to design/data/)
node scripts/seal.mjs seal-tier          # 2. seal new charted entries (or: reseal <entry> after edits)
py execution/generate_entry_pages.py     # 3. re-render so pages show the "Sealed in the Record" mark
node scripts/build-verify.mjs            # 4. (only if the key or chrome changed)
node scripts/seal.mjs verify-all         # 5. gate: must pass before deploy
```

The seal mark and `rel="alternate"` credential link are added by the generator for any entry with a credential. The mark is `data-noseal`, so it does not affect `pageHash` — step 3 does not invalidate step 2.

## Monthly anchor (human step)

```
node scripts/seal.mjs anchor             # prints head + the exact X post text
```
Then: Wayback-snapshot `/ledger/seals.jsonl`, post the head hash from @jerseycitysound, optionally OpenTimestamps, and add an entry to `design/ledger/anchors.json` and commit.

## Deploy notes

- `design/.nojekyll` is present so GitHub Pages serves `/.well-known/` and dotfiles.
- The private key lives only in `keys/` (gitignored) + a password manager + one offline copy. Never in CI.
