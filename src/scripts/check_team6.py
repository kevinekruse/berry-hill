import csv
from collections import defaultdict
p='src/data/BerryHillScores_All_Latest.csv'
bydate=defaultdict(float)
count=defaultdict(int)
with open(p, newline='', encoding='utf-8') as f:
    r=csv.DictReader(f)
    for row in r:
        try:
            year=int(float(row.get('season_year','0')))
        except:
            continue
        if year!=2026:
            continue
        team=row.get('team_num','')
        if team not in ('6','6.0'):
            continue
        date=row.get('date','')
        if '2026-07' not in date:
            continue
        try:
            net=float(row.get('net_score',''))
        except:
            continue
        if not (net==net):
            continue
        bydate[date]+=net
        count[date]+=1
for d in sorted(bydate):
    print(d, 'sum=', bydate[d], 'count=', count[d])
