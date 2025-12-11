def main():
    parser = argparse.ArgumentParser(description="CCOL CLI Tools")
    subparsers = parser.add_subparsers(dest="command")  # no 'required' in Python 3.6

    # CSV → CCOL
    parser_write = subparsers.add_parser("csv_to_custom", help="Convert CSV to CCOL")
    parser_write.add_argument("input_csv", help="Input CSV file")
    parser_write.add_argument("output_ccol", help="Output CCOL file")

    # CCOL → CSV
    parser_read = subparsers.add_parser("custom_to_csv", help="Convert CCOL to CSV")
    parser_read.add_argument("input_ccol", help="Input CCOL file")
    parser_read.add_argument("output_csv", help="Output CSV file")

    args = parser.parse_args()

    if args.command is None:   # manual check for Python 3.6
        parser.print_help()
        return

    if args.command == "csv_to_custom":
        schema = [("id", "int32"), ("value", "float64"), ("name", "string")]
        csv_to_custom(args.input_csv, args.output_ccol, schema)
    elif args.command == "custom_to_csv":
        custom_to_csv(args.input_ccol, args.output_csv)
