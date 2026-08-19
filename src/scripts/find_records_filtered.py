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
    return isfinite(v) and v >= 1 and v < 99000

def is_blind(name):
    if not name:
        return False
    s = str(name).upper()
    return 'BLIND' in s or '\u0392LIND' in s

rows = []
with open(PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

# filter out BLIND and invalid scores
valid_gross = [r for r in rows if valid(num(r.get('gross_score'))) and not is_blind(r.get('display_name'))]
valid_net = [r for r in rows if valid(num(r.get('net_score'))) and not is_blind(r.get('display_name'))]

print('Total rows:', len(rows))
print('Valid gross rows (filtered):', len(valid_gross))
print('Valid net rows (filtered):', len(valid_net))

if valid_gross:
    min_g = min(num(r.get('gross_score')) for r in valid_gross)
    print('Min gross:', min_g)
    for r in valid_gross:
        if num(r.get('gross_score')) == min_g:
            print('  ', r.get('date'), r.get('display_name'), r.get('gross_score'))

if valid_net:
    min_n = min(num(r.get('net_score')) for r in valid_net)
    print('Min net:', min_n)
    for r in valid_net:
        if num(r.get('net_score')) == min_n:
            print('  ', r.get('date'), r.get('display_name'), r.get('net_score'))

# team aggregation ignoring BLIND and invalid nets
team_map = defaultdict(float)
team_count = defaultdict(int)
team_date = {}
for r in rows:
    if is_blind(r.get('display_name')):
        continue
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
