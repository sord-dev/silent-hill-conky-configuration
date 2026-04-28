#!/usr/bin/env python3
import sys
import json
import urllib.request
import os

import time
import os

CACHE = '/tmp/portfolio_cache.json'
SERVICE = 'https://212portfolio.picxi.uk/summary'

def fetch():
    try:
        with urllib.request.urlopen(SERVICE, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        with open(CACHE, 'w') as f:
            json.dump(data, f)
        return data
    except Exception as e:
        with open('/tmp/fetch_debug.txt', 'a') as f:
            f.write(f"{time.time()} fetch error: {type(e).__name__}: {e}\n")
        return None

def load(max_age=300):
    try:
        if time.time() - os.path.getmtime(CACHE) > max_age:
            return None
        with open(CACHE) as f:
            return json.load(f)
    except:
        return None

d = load() or fetch() or load(max_age=86400) or {}
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
