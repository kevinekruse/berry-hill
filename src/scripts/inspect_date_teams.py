import csv
from collections import defaultdict
from datetime import datetime
p='src/data/BerryHillScores_All_Latest.csv'
date_target='2021-05-11'
map=defaultdict(lambda:{'net_sum':0,'count':0,'dates':set()})
rows=0
with open(p,newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f)
    for r in reader:
        d=r.get('date','')
        if not d: continue
        if date_target not in d: continue
        rows+=1
        try:
            year=datetime.fromisoformat(d.strip()).year
        except Exception:
            try:
                year=int(d.strip().split('-')[0])
            except:
                year=None
        if year==1900: continue
        try:
            season=float(r.get('season_year',''))
            week=float(r.get('week_num',''))
            team=float(r.get('team_num',''))
            net=float(r.get('net_score',''))
        except:
            continue
        if not (week==week and team==team and net==net):
            continue
        key=f"{int(season)}-{int(week)}-{int(team)}"
        map[key]['net_sum']+=net
        map[key]['count']+=1
        map[key]['dates'].add(d.strip())
print('rows for date',date_target,rows)
print('unique team keys:',len(map))
for k in sorted(map.keys()):
    print(k,map[k])
