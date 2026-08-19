import csv
import unicodedata
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'data' / 'BerryHillScores_Rounds_NoBlind.csv'
if not p.exists():
    print('MISSING', p)
    raise SystemExit(2)

def normalize(s):
    if s is None:
        return ''
    s = unicodedata.normalize('NFKD', str(s))
    s = s.replace('\u0392', 'B').replace('\u03B2', 'b')
    s = ''.join(ch for ch in s if ord(ch) < 128)
    return s.strip().casefold()

gross = []
row_types = {}
with p.open(newline='', encoding='utf-8') as f:
    rdr = csv.DictReader(f)
    for r in rdr:
        rt = normalize(r.get('row_type') or r.get('row') or '')
        row_types[rt] = row_types.get(rt, 0) + 1
        if rt != 'round':
            continue
        dn = normalize(r.get('display_name') or r.get('display') or '')
        if 'blind' in dn:
            continue
        try:
            g = float(r.get('gross_score'))
        except Exception:
            continue
        if g != g:
            continue
        gross.append(g)

gross.sort()
print('rows_total_by_row_type=', row_types)
print('gross_count=', len(gross))
if gross:
    print('min,max,median=', gross[0], gross[-1], gross[len(gross)//2])
    print('sample(10)=', gross[:10])
else:
    print('no gross values')
