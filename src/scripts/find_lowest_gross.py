import csv
from datetime import datetime
p='src/data/BerryHillScores_All_Latest.csv'
rows=[]
with open(p,newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f)
    for r in reader:
        name=r.get('display_name','')
        if not name: name=r.get('player','')
        s=name.upper()
        if 'BLIND' in s or '\u0392LIND' in s: continue
        try:
            gross=float(r.get('gross_score',''))
        except:
            continue
        if gross < 1 or gross >= 99000:
            continue
        # skip year 1900
        d=r.get('date','')
        year=None
        try:
            year=datetime.fromisoformat(d.strip()).year
        except Exception:
            try:
                year=int(d.strip().split('-')[0])
            except:
                pass
        if year==1900:
            continue
        rows.append({'date':d.strip(), 'player':name, 'gross':gross, 'line':r})
if not rows:
    print('no rows')
else:
    m=min(r['gross'] for r in rows)
    tied=[r for r in rows if r['gross']==m]
    print('min gross',m,'count',len(tied))
    for t in tied:
        print(t['date'], t['player'], t['gross'])
