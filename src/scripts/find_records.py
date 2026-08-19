import csv
from collections import defaultdict
from math import isfinite

PATH = 'src/data/BerryHillScores_All_Latest.csv'

def num(v):
    try:
        if v == '' or v is None:
            return float('nan')
        return float(v)
    except:
        return float('nan')

def valid(v):
    return isfinite(v) and v < 99000

rows = []
with open(PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

gross_rows = [r for r in rows if valid(num(r.get('gross_score')))]
net_rows = [r for r in rows if valid(num(r.get('net_score')))]

print('Total rows:', len(rows))
print('Valid gross rows:', len(gross_rows))
print('Valid net rows:', len(net_rows))

if gross_rows:
    min_g = min(num(r.get('gross_score')) for r in gross_rows)
    print('Min gross:', min_g)
    for r in gross_rows:
        if num(r.get('gross_score')) == min_g:
            print('  ', r.get('date'), r.get('display_name'), r.get('gross_score'))

if net_rows:
    min_n = min(num(r.get('net_score')) for r in net_rows)
    print('Min net:', min_n)
    for r in net_rows:
        if num(r.get('net_score')) == min_n:
            print('  ', r.get('date'), r.get('display_name'), r.get('net_score'))

# team aggregation
team_map = defaultdict(float)
team_count = defaultdict(int)
team_date = {}
for r in rows:
    net = num(r.get('net_score'))
    if not valid(net):
        continue
    season = r.get('season_year','')
    week = r.get('week_num','')
    team = r.get('team_num','')
    key = f"{season}-{week}-{team}"
    team_map[key] += net
    team_count[key] += 1
    if key not in team_date:
        team_date[key] = r.get('date','')

if team_map:
    min_team = min(team_map.values())
    print('Min team net:', min_team)
    for k,v in team_map.items():
        if v == min_team:
            print('  ', k, team_date.get(k), v, 'count=', team_count[k])
