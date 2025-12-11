import time
import csv
from src.reader import read_ccol

def test_performance():
    input_csv = "data/sample.csv"
    input_ccol = "data/sample.ccol"

    # Measure CSV parse time
    start = time.time()
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        ages = [row["id"] for row in reader]  # Example column
    csv_time = time.time() - start

    # Measure CCOL selective read time
    start = time.time()
    data = read_ccol(input_ccol, needed_cols=["id"])
    ccol_time = time.time() - start

    print(f"CSV parse time: {csv_time:.4f}s")
    print(f"CCOL selective read time: {ccol_time:.4f}s")

if __name__ == "__main__":
    test_performance()
