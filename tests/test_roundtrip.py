# tests/test_roundtrip.py
import csv
from src.writer import write_ccol
from src.reader import read_ccol

def test_roundtrip(tmp_path):
    # Prepare sample CSV
    csv_file = tmp_path / "sample.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "price", "name"])
        writer.writerow([1, 10.5, "apple"])
        writer.writerow([2, 20.0, "banana"])

    # Convert CSV → CCOL
    ccol_file = tmp_path / "sample.ccol"
    schema = [("id", "int32"), ("price", "float64"), ("name", "string")]
    write_ccol(str(csv_file), str(ccol_file), schema)

    # Convert CCOL → data dictionary
    data = read_ccol(str(ccol_file))

    # Assertions
    assert data["id"] == [1, 2]
    assert data["price"] == [10.5, 20.0]
    assert data["name"] == ["apple", "banana"]
