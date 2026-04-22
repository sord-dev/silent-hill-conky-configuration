#!/usr/bin/env python3
import sys
import json
import subprocess
import os

CACHE = '/tmp/portfolio_cache.json'
SERVICE = 'https://212portforlio.picxi.uk/summary'

def fetch():
    try:
        r = subprocess.run(['curl', '-s', '--max-time', '5', SERVICE], 
                          capture_output=True, text=True)
        data = json.loads(r.stdout)
        with open(CACHE, 'w') as f:
            json.dump(data, f)
        return data
    except:
        return None

def load():
    try:
        with open(CACHE) as f:
            return json.load(f)
    except:
        return None

d = load() or fetch() or {}
field = sys.argv[1] if len(sys.argv) > 1 else 'total'

if field == 'total':
    print(f"£{d.get('total', 0):,.2f}")
elif field == 'pnl':
    pnl = d.get('unrealised_pnl', 0)
    pct = d.get('unrealised_pct', 0)
    sign = '+' if pnl >= 0 else ''
    print(f"{sign}£{pnl:,.2f} ({sign}{pct:.1f}%)")
elif field == 'cash':
    print(f"£{d.get('cash', 0):,.2f}")
elif field == 'positions':
    print(d.get('positions', '—'))
elif field == 'summary':
    import re, textwrap
    s = d.get('ai_summary', '')
    if not s:
        print('—')
    else:
        # split on **Label:** pattern, format as uppercase headers
        parts = re.split(r'\*\*([^*]+):\*\*', s)
        out = []
        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            if i % 2 == 1:
                out.append(part.upper() + ':')
            else:
                out.extend(textwrap.wrap(part, 42))
        print('\n'.join(out))
elif field == 'fetch':
    fetch()
