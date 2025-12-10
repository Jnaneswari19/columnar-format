# src/cli.py (snippet)
import argparse
from .csv_tools import csv_to_custom, custom_to_csv

def main():
    p = argparse.ArgumentParser("CCOL tools")
    sp = p.add_subparsers(dest="cmd", required=True)

    w = sp.add_parser("csv_to_custom")
    w.add_argument("input_csv")
    w.add_argument("output_ccol")

    r = sp.add_parser("custom_to_csv")
    r.add_argument("input_ccol")
    r.add_argument("output_csv")

    args = p.parse_args()
    if args.cmd == "csv_to_custom":
        csv_to_custom(args.input_csv, args.output_ccol)
    else:
        custom_to_csv(args.input_ccol, args.output_csv)

if __name__ == "__main__":
    main()
