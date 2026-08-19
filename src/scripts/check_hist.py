import csv
p='src/data/BerryHillScores_All_Latest.csv'
with open(p, newline='', encoding='utf-8') as f:
    r=csv.DictReader(f)
    m={}
    for row in r:
        try:
            year=int(row.get('season_year','') or 0)
        except:
            continue
        if year!=2026:
            continue
        week=row.get('week_num','')
        team=row.get('team_num','')
        net_s=row.get('net_score','')
        try:
            net=float(net_s)
        except:
            continue
        if net!=net:
            continue
        key=f"{week}-{team}"
        if key not in m:
            date=row.get('date','')
            m[key]={'date':date,'week':week,'team':team,'net_sum':0,'count':0}
        m[key]['net_sum']+=net
        m[key]['count']+=1
team_rows=list(m.values())
vals=[tr['net_sum'] for tr in team_rows]
print('team_rows:', len(team_rows))
if len(vals):
    print('min,max,mean:', min(vals), max(vals), sum(vals)/len(vals))
    print('first 10:', vals[:10])
else:
    print('no values')
