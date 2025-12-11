# src/writer.py
import csv
import struct
from .ccol_types import pack_value
 # our helper functions

def write_ccol(input_csv, output_ccol, schema):
    """
    Convert a CSV file into CCOL binary format.
    - input_csv: path to CSV file
    - output_ccol: path to output CCOL file
    - schema: list of (column_name, dtype) tuples
    """
    with open(input_csv, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        with open(output_ccol, "wb") as f:
            # Write header: number of columns
            f.write(struct.pack("I", len(schema)))

            # Write schema (column names + types)
            for name, dtype in schema:
                name_bytes = name.encode("utf-8")
                f.write(struct.pack("I", len(name_bytes)))
                f.write(name_bytes)

                dtype_bytes = dtype.encode("utf-8")
                f.write(struct.pack("I", len(dtype_bytes)))
                f.write(dtype_bytes)

            # Write rows
            for row in reader:
                for name, dtype in schema:
                    value = row[name]   # must match CSV header
                    if dtype == "int32":
                        value = int(value)
                    elif dtype == "float64":
                        value = float(value)
                    packed = pack_value(value, dtype)
                    f.write(packed)

if __name__ == "__main__":
    # Match schema to your CSV header: id,price,name
    schema = [
        ("id", "int32"),
        ("price", "float64"),
        ("name", "string")
    ]
    write_ccol("data/sample.csv", "data/sample.ccol", schema)
    print("✅ CCOL file written successfully to data/sample.ccol")
