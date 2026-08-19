#!/usr/bin/env python3
"""Compute yearly (season) score averages from a BerryHill scores CSV.

Usage:
  python compute_season_averages.py --input <scores.csv> [--output season_averages.csv]

Default input is `../data/BerryHillScores_Rounds_NoBlind.csv` (site data folder).
"""

import argparse
import csv
import os
import unicodedata
from collections import defaultdict
from statistics import mean
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def is_blind(name: str) -> bool:
    if not name:
        return False
    s = unicodedata.normalize('NFKD', str(name)).casefold()
    return 'blind' in s


def parse_float(s):
    try:
        if s is None or s == '':
            return None
        return float(s)
    except Exception:
        return None


def season_key_from_row(row):
    # Prefer explicit season_year, fallback to year parsed from date
    sy = row.get('season_year') or row.get('season')
    if sy:
        try:
            # handle floats like "2026.0"
            return str(int(float(sy)))
        except Exception:
            return str(sy)
    # fallback: parse date column
    d = row.get('date') or row.get('round_date')
    if d:
        try:
            return str(datetime.fromisoformat(d.strip()).year)
        except Exception:
            try:
                return str(datetime.strptime(d.strip(), '%Y-%m-%d %H:%M:%S').year)
            except Exception:
                pass
    return 'unknown'


def compute(input_path, output_path=None, min_gross=0.0, max_gross=200.0):
    by_season = defaultdict(lambda: {'gross': [], 'net': [], 'round_index': [], 'teams': set()})
    total_rows = 0
    with open(input_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            row_type = (row.get('row_type') or row.get('row') or '').strip().lower()
            if row_type != 'round':
                continue
            display = row.get('display_name') or row.get('display') or ''
            if is_blind(display):
                continue
            gross = parse_float(row.get('gross_score'))
            net = parse_float(row.get('net_score'))
            round_idx = parse_float(row.get('round_index'))
            if gross is None:
                continue
            # filter gross by sensible bounds to exclude invalid/outlier rows
            if not (min_gross <= gross <= max_gross):
                continue
            season = season_key_from_row(row)
            by_season[season]['gross'].append(gross)
            if net is not None:
                by_season[season]['net'].append(net)
            if round_idx is not None:
                by_season[season]['round_index'].append(round_idx)
            # count unique teams per season (prefer numeric team_num, fall back to team or team_name)
            team = row.get('team_num') or row.get('team') or row.get('team_name') or row.get('club')
            if team is not None and str(team).strip() != '':
                by_season[season]['teams'].add(str(team).strip())

    # sort seasons numerically when possible
    def season_sort_key(s):
        try:
            return int(s)
        except Exception:
            return s

    results = []
    for season in sorted(by_season.keys(), key=season_sort_key):
        vals = by_season[season]['gross']
        nets = by_season[season]['net']
        rinds = by_season[season]['round_index']
        teams = by_season[season]['teams']
        avg = mean(vals) if vals else None
        net_avg = mean(nets) if nets else None
        round_index_avg = mean(rinds) if rinds else None
        results.append((season, len(vals), len(teams), avg, net_avg, round_index_avg))

    # print results
    print(f"Read {total_rows} rows from {input_path}")
    print("Season,Rounds,Teams,Gross_Avg,Net_Avg,RoundIndex_Avg")
    for season, rounds_cnt, teams_cnt, avg, net_avg, round_index_avg in results:
        avg_str = f"{avg:.2f}" if avg is not None else "N/A"
        net_str = f"{net_avg:.2f}" if net_avg is not None else "N/A"
        ri_str = f"{round_index_avg:.2f}" if round_index_avg is not None else "N/A"
        print(f"{season},{rounds_cnt},{teams_cnt},{avg_str},{net_str},{ri_str}")

    # write CSV if requested
    if output_path:
        with open(output_path, 'w', newline='', encoding='utf-8') as out:
            w = csv.writer(out)
            w.writerow(['season_year', 'rounds', 'teams', 'gross_avg', 'net_avg', 'round_index_avg'])
            for season, rounds_cnt, teams_cnt, avg, net_avg, round_index_avg in results:
                w.writerow([season, rounds_cnt, teams_cnt, f"{avg:.2f}" if avg is not None else '', f"{net_avg:.2f}" if net_avg is not None else '', f"{round_index_avg:.2f}" if round_index_avg is not None else ''])
        print(f"Wrote per-season averages to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute yearly score averages from a scores CSV')
    default_input = os.path.join(SCRIPT_DIR, '..', 'data', 'BerryHillScores_Rounds_NoBlind.csv')
    parser.add_argument('--input', '-i', default=default_input, help='Input CSV file path (defaults to filtered rounds CSV)')
    parser.add_argument('--output', '-o', help='Optional output CSV file path')
    parser.add_argument('--min-gross', type=float, default=0.0, help='Minimum gross score to include')
    parser.add_argument('--max-gross', type=float, default=200.0, help='Maximum gross score to include (filters out obvious outliers)')
    args = parser.parse_args()
    compute(args.input, args.output, min_gross=args.min_gross, max_gross=args.max_gross)
