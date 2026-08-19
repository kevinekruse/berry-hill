import csv
from datetime import datetime
p='src/data/BerryHillScores_All_Latest.csv'
rows=[]
with open(p,newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f)
    for r in reader:
        name=r.get('display_name','') or r.get('player','')
        s=(name or '').upper()
        if 'BLIND' in s or '\u0392LIND' in s: continue
        try:
            gross=float(r.get('gross_score',''))
        except:
            continue
        if gross < 1 or gross >= 99000:
            continue
        d=r.get('date','').strip()
        # skip year 1900
        y=None
        try:
            y=datetime.fromisoformat(d).year
        except:
            try:
                y=int(d.split('-')[0])
            except:
                y=None
        if y==1900:
            continue
        if gross < 40:
            rows.append({'date':d,'player':name,'team':r.get('team_num',''),'gross':gross})

print('count',len(rows))
for r in rows[:50]:
    print(r['date'], r['player'], r['team'], r['gross'])
