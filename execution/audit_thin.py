import json
from pathlib import Path

DATA = Path('data/entries.json')
with DATA.open('r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['entries']
thin = []
for e in entries:
    facts = e.get('facts', [])
    total_chars = sum(len(f) for f in facts)
    is_placeholder = any('Entry pending' in f or 'awaits fuller' in f or 'await fuller' in f or 'holds his place' in f for f in facts)
    has_card = bool(e.get('card'))
    if len(facts) <= 1 or total_chars < 200 or is_placeholder:
        thin.append({
            'no': e.get('entry_no'),
            'name': e.get('name'),
            'slug': e.get('slug'),
            'facts_count': len(facts),
            'chars': total_chars,
            'placeholder': is_placeholder,
            'has_card': has_card,
        })

print(f'Thin profiles: {len(thin)}')
print()
for t in thin:
    flag = ' [PLACEHOLDER]' if t['placeholder'] else ''
    card_flag = '' if t['has_card'] else ' [NO CARD]'
    print(f"  [{t['no']}] {t['name']} ({t['slug']}) -- {t['facts_count']} facts, {t['chars']} chars{flag}{card_flag}")
