#!/usr/bin/env python3
"""Calculate season-level rainouts and blind counts from BerryHill scores CSV.

Produces a CSV with per-season metrics:
    season_year,weeks_scheduled,num_teams,total_records,max_nominal_rounds,weeks_cancelled_due_to_weather,expected_rounds,expected_blinds,extra_blinds,blind_perentage,rounds_count,blind_count,checksum_total_rounds,checksum

Usage:
    python calculate_season_rainouts_and_blinds.py --input <scores.csv> --rounds-input <rounds_no_blind.csv> --output <out.csv>

Defaults:
  input: ../data/BerryHillScores_All_Latest.csv
    rounds-input: ../data/BerryHillScores_Rounds_NoBlind.csv
  output: ../data/season_rainouts_blinds.csv
"""

import argparse
import csv
import json
import os
import unicodedata
from collections import defaultdict
from datetime import date
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen


def is_blind(name: Optional[str]) -> bool:
    if not name:
        return False
    # Normalize and map common Unicode confusables that look like Latin 'B'
    s = unicodedata.normalize('NFKD', str(name))
    confusables = {
        ord('\u0392'): 'b',  # GREEK CAPITAL LETTER BETA
        ord('\u03B2'): 'b',  # GREEK SMALL LETTER BETA
        ord('\u0412'): 'b',  # CYRILLIC CAPITAL LETTER VE
        ord('\u0432'): 'b',  # CYRILLIC SMALL LETTER VE
    }
    s2 = s.translate(confusables).casefold()
    return 'blind' in s2


def parse_float(s):
    try:
        if s is None or s == '':
            return None
        return float(s)
    except Exception:
        return None


def parse_bool(s):
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    ss = str(s).strip().lower()
    return ss in ('true', '1', 'yes', 'y')


def season_key_from_row(row):
    sy = row.get('season_year') or row.get('season')
    if sy:
        try:
            return str(int(float(sy)))
        except Exception:
            return str(sy)
    d = row.get('date') or row.get('round_date')
    if d:
        try:
            from datetime import datetime
            return str(datetime.fromisoformat(d.strip()).year)
        except Exception:
            try:
                from datetime import datetime
                return str(datetime.strptime(d.strip(), '%Y-%m-%d %H:%M:%S').year)
            except Exception:
                pass
    return 'unknown'


def is_rainout_row(row):
    # Heuristic: explicit row_type containing 'rain' OR missing gross_score for a row
    rt = (row.get('row_type') or row.get('row') or '').strip().lower()
    if 'rain' in rt:
        return True
    gross = parse_float(row.get('gross_score'))
    # if no gross score and not an explicit round, treat as rainout/other non-round
    if gross is None:
        return True
    return False


def fetch_bridgeton_tuesday_weather_averages(season_year: Optional[int]):
    """Return average Tuesday daily highs (temp and heat index) for May-Aug in Bridgeton, MO."""
    if season_year is None or season_year < 1940:
        return '', ''

    start_date = date(season_year, 5, 1)
    end_date = date(season_year, 8, 31)
    today = date.today()
    if end_date > today:
        end_date = today
    if end_date < start_date:
        return '', ''

    params = {
        'latitude': 38.767,
        'longitude': -90.411,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'daily': 'temperature_2m_max,apparent_temperature_max',
        'temperature_unit': 'fahrenheit',
        'timezone': 'America/Chicago',
    }
    url = 'https://archive-api.open-meteo.com/v1/archive?' + urlencode(params)

    try:
        with urlopen(url, timeout=20) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
    except Exception:
        return '', ''

    daily = payload.get('daily') or {}
    dates = daily.get('time') or []
    temps = daily.get('temperature_2m_max') or []
    apparent = daily.get('apparent_temperature_max') or []

    temp_vals = []
    heat_vals = []
    for d, t, h in zip(dates, temps, apparent):
        try:
            dt = date.fromisoformat(d)
        except Exception:
            continue
        # Tuesday is weekday 1 (Mon=0)
        if dt.weekday() != 1:
            continue
        if t is not None:
            temp_vals.append(float(t))
        if h is not None:
            heat_vals.append(float(h))

    avg_temp = round(sum(temp_vals) / len(temp_vals), 1) if temp_vals else ''
    avg_heat = round(sum(heat_vals) / len(heat_vals), 1) if heat_vals else ''
    return avg_temp, avg_heat


def compute(input_path, output_path=None, rounds_input_path=None):
    by_season = defaultdict(lambda: {
        'total_records': 0,
        'blind_count': 0,
        'rounds_count': 0,
        'rainouts_count': 0,
        'blinds_in_non_rainout_rounds': 0,
        'partials_no_valid_differential': 0,
        'played_weeks': set(),
        'seen_weeks': set(),
    })

    rounds_by_season = defaultdict(int)

    with open(input_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            season = season_key_from_row(row)
            stats = by_season[season]
            stats['total_records'] += 1

            wk_seen = parse_float(row.get('week_num'))
            if wk_seen is not None:
                stats['seen_weeks'].add(int(wk_seen))

            display = row.get('player_name') or row.get('display_name') or row.get('display') or ''
            if is_blind(display):
                stats['blind_count'] += 1

            row_type = (row.get('row_type') or row.get('row') or '').strip().lower()

            # Determine rainout using heuristic
            rainout = is_rainout_row(row)
            if rainout:
                stats['rainouts_count'] += 1

            # Count rounds (rows with row_type == 'round' and having a gross_score)
            gross = parse_float(row.get('gross_score'))
            if row_type == 'round' and gross is not None:
                stats['rounds_count'] += 1
                # blind in non-rainout round
                if is_blind(display):
                    stats['blinds_in_non_rainout_rounds'] += 1

                # check valid_differential
                valid_diff = parse_bool(row.get('valid_differential'))
                diff = parse_float(row.get('differential'))
                # treat missing/invalid differential as partial/no valid differential
                if not valid_diff or diff is None:
                    stats['partials_no_valid_differential'] += 1

                # A "normal" played week has at least one non-blind, non-placeholder round score.
                if (not is_blind(display)) and gross < 90000:
                    wk = parse_float(row.get('week_num'))
                    if wk is not None:
                        stats['played_weeks'].add(int(wk))

    # Rounds count is sourced from the rounds-only, no-blind dataset.
    if rounds_input_path:
        with open(rounds_input_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                season = season_key_from_row(row)
                rounds_by_season[season] += 1

    # prepare results
    results = []
    def season_sort_key(s):
        try:
            return int(s)
        except Exception:
            return s

    for season in sorted(by_season.keys(), key=season_sort_key):
        s = by_season[season]
        try:
            season_int = int(season)
        except Exception:
            season_int = None

        weeks_scheduled = ''
        if season_int == 2020:
            weeks_scheduled = 16
        elif season_int is not None and season_int >= 2021:
            weeks_scheduled = 17

        # User-provided team counts by season.
        fixed_teams_by_season = {
            2020: 5,
            2021: 10,
            2022: 8,
            2023: 8,
            2024: 8,
            2025: 8,
            2026: 6,
        }
        team_count = fixed_teams_by_season.get(season_int, '') if season_int is not None else ''

        max_nominal_rounds = ''
        if isinstance(weeks_scheduled, int) and isinstance(team_count, int) and team_count > 0:
            max_nominal_rounds = weeks_scheduled * 4 * team_count

        # Historical exception for 2021: week 17 had only two championship teams.
        # Use requested formula: 16*10*4 + 1*2*4.
        if season_int == 2021:
            max_nominal_rounds = (16 * 10 * 4) + (1 * 2 * 4)

        # Historical exception for 2023: week 17 had only two championship teams.
        # Use requested formula: 16*8*4 + 1*2*4.
        if season_int == 2023:
            max_nominal_rounds = (16 * 8 * 4) + (1 * 2 * 4)

        # Historical exception for 2024: week 17 had only two championship teams.
        # Use requested formula: 16*8*4 + 1*2*4.
        if season_int == 2024:
            max_nominal_rounds = (16 * 8 * 4) + (1 * 2 * 4)

        rainout_weeks = ''
        if isinstance(weeks_scheduled, int):
            played_weeks_count = len(s['played_weeks'])
            max_week_seen = max(s['seen_weeks']) if s['seen_weeks'] else weeks_scheduled
            effective_scheduled_weeks = min(weeks_scheduled, max_week_seen)
            rainout_weeks = max(effective_scheduled_weeks - played_weeks_count, 0)

        # Historical exception: 2021 had three rainout weeks total.
        if season_int == 2021:
            rainout_weeks = 3

        expected_rounds = ''
        if isinstance(max_nominal_rounds, int) and isinstance(rainout_weeks, int) and isinstance(team_count, int):
            expected_rounds = max_nominal_rounds - (rainout_weeks * 4 * team_count)

        expected_blinds = ''
        if isinstance(max_nominal_rounds, int) and isinstance(expected_rounds, int):
            expected_blinds = max_nominal_rounds - expected_rounds

        rounds_count = rounds_by_season.get(season, 0)

        extra_blinds = ''
        if isinstance(expected_rounds, int):
            extra_blinds = expected_rounds - rounds_count

        blind_perentage = ''
        if isinstance(extra_blinds, int) and isinstance(expected_rounds, int) and expected_rounds > 0:
            blind_perentage = round(extra_blinds / expected_rounds, 4)

        checksum_total_rounds = ''
        if isinstance(rounds_count, int) and isinstance(extra_blinds, int) and isinstance(expected_blinds, int):
            checksum_total_rounds = rounds_count + extra_blinds + expected_blinds

        checksum = ''
        if isinstance(max_nominal_rounds, int) and isinstance(checksum_total_rounds, int):
            checksum = (max_nominal_rounds == checksum_total_rounds)

        avg_temp_tues_may_aug, avg_heat_index_tues_may_aug = fetch_bridgeton_tuesday_weather_averages(season_int)

        results.append((
            season,
            weeks_scheduled,
            team_count,
            s['total_records'],
            max_nominal_rounds,
            rainout_weeks,
            expected_rounds,
            expected_blinds,
            extra_blinds,
            blind_perentage,
            rounds_count,
            s['blind_count'],
            checksum_total_rounds,
            checksum,
            avg_temp_tues_may_aug,
            avg_heat_index_tues_may_aug,
        ))

    # print and optionally write CSV
    print('Season,Weeks_Scheduled,Num_Teams,Total_Records,Max_Nominal_Rounds,Weeks_Cancelled_Due_To_Weather,Expected_Rounds,Expected_Blinds,Extra_Blinds,Blind_Perentage,Rounds_Count,Blind_Count,Checksum_Total_Rounds,Checksum,Avg_Temp_Tuesday_May_Aug_Bridgeton_MO,Avg_Heat_Index_Tuesday_May_Aug_Bridgeton_MO')
    for row in results:
        print(','.join(str(x) for x in row))

    if output_path:
        with open(output_path, 'w', newline='', encoding='utf-8') as out:
            w = csv.writer(out)
            w.writerow(['season_year','weeks_scheduled','num_teams','total_records','max_nominal_rounds','weeks_cancelled_due_to_weather','expected_rounds','expected_blinds','extra_blinds','blind_perentage','rounds_count','blind_count','checksum_total_rounds','checksum','avg_temp_tuesday_may_aug_bridgeton_mo','avg_heat_index_tuesday_may_aug_bridgeton_mo'])
            for row in results:
                w.writerow(row)
        print(f'Wrote results to {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.join(script_dir, '..', 'data', 'BerryHillScores_All_Latest.csv')
    default_rounds_input = os.path.join(script_dir, '..', 'data', 'BerryHillScores_Rounds_NoBlind.csv')
    default_output = os.path.join(script_dir, '..', 'data', 'season_rainouts_blinds.csv')

    parser = argparse.ArgumentParser(description='Calculate season rainouts and blinds')
    parser.add_argument('--input', '-i', default=default_input, help='Input CSV path')
    parser.add_argument('--rounds-input', default=default_rounds_input, help='Rounds-only no-blind CSV path')
    parser.add_argument('--output', '-o', default=default_output, help='Output CSV path')
    args = parser.parse_args()
    compute(args.input, args.output, args.rounds_input)
