import argparse
import csv
import os
import sys
import unicodedata


def filter_scores(input_path: str, output_path: str) -> int:
    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}")
        return 2

    with open(input_path, newline='', encoding='utf-8') as inf:
        reader = csv.DictReader(inf)
        fieldnames = reader.fieldnames
        if not fieldnames:
            print("Input CSV has no header")
            return 3

        filtered_rows = []

        def normalize_text(s: str) -> str:
            if not s:
                return ''
            s = unicodedata.normalize('NFKD', s)
            # map common confusable characters to ASCII equivalents
            s = s.replace('\u0392', 'B').replace('\u03B2', 'b')
            # remove non-ASCII to avoid visually-similar unicode letters
            s = ''.join(ch for ch in s if ord(ch) < 128)
            return s.strip().casefold()

        for row in reader:
            row_type = normalize_text(row.get('row_type') or '')
            display_name = normalize_text(row.get('display_name') or '')
            if row_type == 'round' and display_name != 'blind':
                filtered_rows.append(row)

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        for r in filtered_rows:
            writer.writerow(r)

    print(f"Wrote {len(filtered_rows)} rows to {output_path}")
    return 0


def default_paths():
    here = os.path.dirname(__file__)
    data_dir = os.path.normpath(os.path.join(here, '..', 'data'))
    default_input = os.path.join(data_dir, 'BerryHillScores_All_Latest.csv')
    default_output = os.path.join(data_dir, 'BerryHillScores_Rounds_NoBlind.csv')
    return default_input, default_output


def main(argv=None):
    parser = argparse.ArgumentParser(description='Filter BerryHill scores: keep only row_type=round and display_name != Blind')
    inp_def, out_def = default_paths()
    parser.add_argument('input', nargs='?', default=inp_def, help='Path to input CSV (default: %(default)s)')
    parser.add_argument('output', nargs='?', default=out_def, help='Path to output CSV (default: %(default)s)')
    args = parser.parse_args(argv)

    return filter_scores(args.input, args.output)


if __name__ == '__main__':
    sys.exit(main())
