# src/cli.py
import argparse
import csv
from .writer import write_ccol
from .reader import read_ccol

def csv_to_custom(input_csv, output_ccol, schema):
    """Convert CSV to CCOL format using the given schema."""
    write_ccol(input_csv, output_ccol, schema)
    print(f"✅ Converted {input_csv} → {output_ccol}")

def custom_to_csv(input_ccol, output_csv):
    """Convert CCOL back to CSV format."""
    data = read_ccol(input_ccol)
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        # Write header row
        writer.writerow(data.keys())
        # Write rows
        rows = zip(*data.values())
        for row in rows:
            writer.writerow(row)
    print(f"✅ Converted {input_ccol} → {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="CCOL CLI Tools")
    subparsers = parser.add_subparsers(dest="command")


    # CSV → CCOL
    parser_write = subparsers.add_parser("csv_to_custom", help="Convert CSV to CCOL")
    parser_write.add_argument("input_csv", help="Input CSV file")
    parser_write.add_argument("output_ccol", help="Output CCOL file")

    # CCOL → CSV
    parser_read = subparsers.add_parser("custom_to_csv", help="Convert CCOL to CSV")
    parser_read.add_argument("input_ccol", help="Input CCOL file")
    parser_read.add_argument("output_csv", help="Output CSV file")

    args = parser.parse_args()

    if args.command == "csv_to_custom":
        # Match schema to your CSV header: id,price,name
        schema = [
            ("id", "int32"),
            ("price", "float64"),
            ("name", "string")
        ]
        csv_to_custom(args.input_csv, args.output_ccol, schema)

    elif args.command == "custom_to_csv":
        custom_to_csv(args.input_ccol, args.output_csv)

if __name__ == "__main__":
    main()
