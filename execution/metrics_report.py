# -*- coding: utf-8 -*-
"""Evidence-standard metrics snapshot — the charter's north-star metric.

Prints the distribution of entry `status` tiers, sourcing depth, and the
names still in the hold queue, so "entries meeting the highest evidence
standard" is trackable over time. Run: py execution/metrics_report.py
"""
import json
import io
import os
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "data", "entries.json")

d = json.load(io.open(P, encoding="utf-8"))
entries = d["entries"]

print(f"The Jersey City Sound — evidence metrics · {date.today().isoformat()}")
print(f"Total entries: {len(entries)}\n")

# Status tier distribution (highest standard first)
TIER_ORDER = ["doc-verified", "web-verified", "community-verified", "handle-provided"]
tiers = Counter(e.get("status", "(none)") for e in entries)
print("Status tiers:")
for t in TIER_ORDER + sorted(set(tiers) - set(TIER_ORDER)):
    if t in tiers:
        bar = "#" * round(40 * tiers[t] / len(entries))
        print(f"  {t:20s} {tiers[t]:4d}  {bar}")

# Sourcing depth
no_src = [e for e in entries if not [s for s in e.get("sources", []) if s.get("url") or s.get("label")]]
one_src = [e for e in entries if len([s for s in e.get("sources", []) if s.get("url")]) == 1]
print(f"\nSourcing:")
print(f"  entries with zero usable sources : {len(no_src)}")
print(f"  entries with exactly one source  : {len(one_src)}")
if no_src:
    print("  zero-source entries (upgrade targets):")
    for e in sorted(no_src, key=lambda x: x["entry_no"]):
        print(f"    #{e['entry_no']} {e['name']} [{e.get('status','?')}]")

# Hold queue
held = d.get("discovered_candidates", {}).get("held_pending_source", {}).get("names", [])
print(f"\nHold queue (private, unpublished): {len(held)} names")
for n in held:
    print(f"  - {n['name']}")

# Todo debt
todo = sum(len(e.get("todo_robert", [])) for e in entries)
print(f"\nOpen todo_robert items across all entries: {todo}")
