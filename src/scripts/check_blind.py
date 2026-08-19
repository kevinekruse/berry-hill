import csv
import unicodedata

path = r"c:/Users/kevin/OneDrive/DataViz/D3_Observable/berry_hill/src/data/BerryHillScores_Rounds_NoBlind.csv"
count = 0
with open(path, newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        dn = row.get('display_name') or ''
        s = unicodedata.normalize('NFKD', dn).replace('\u0392', 'B').replace('\u03B2', 'b')
        s = ''.join(ch for ch in s if ord(ch) < 128).strip().casefold()
        if s == 'blind':
            count += 1

print('blind_count=', count)
