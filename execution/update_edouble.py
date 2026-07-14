import json
from pathlib import Path

DATA = Path('data/entries.json')

def run():
    with DATA.open('r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data['entries']:
        if entry.get('slug') == 'dj-e-double':
            # Fix facts
            new_facts = []
            for fact in entry.get('facts', []):
                if "Greenbean, Thunderkatt, Smurfet, DJ Q, Deejay Luchionney" in fact:
                    new_facts.append(
                        "He was the founder and head of Double Platinum Entertainment. "
                        "The crew's members included Greenbean, Thunderkatt, Smurfet, DJ Q, DJ DYCE, "
                        "Deejay Luchionney, DJ Walleykatt, DJ DX (Double X), and Exclusive (R.I.P Jamie)."
                    )
                else:
                    new_facts.append(fact)
            entry['facts'] = new_facts
            
            # Fix card
            for c in entry.get('card', []):
                if c.get('label') == 'Double Platinum Entertainment':
                    c['value'] = "Greenbean, Thunderkatt, Smurfet, DJ Q, DJ DYCE, Deejay Luchionney, DJ Walleykatt, DJ DX (Double X), Exclusive (R.I.P Jamie)"
            break

    with DATA.open('w', encoding='utf-8', newline='\r\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print("Updated DJ E Double with DJ DYCE.")

if __name__ == '__main__':
    run()
