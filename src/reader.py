# src/reader.py
import struct
from .ccol_types import unpack_value

def read_ccol(input_ccol, needed_cols=None):
    """
    Read CCOL file into a dictionary.
    If needed_cols is provided, only those columns are read.
    """
    with open(input_ccol, "rb") as f:
        num_columns = struct.unpack("I", f.read(4))[0]
        schema = []
        for _ in range(num_columns):
            name_len = struct.unpack("I", f.read(4))[0]
            name = f.read(name_len).decode("utf-8")
            dtype_len = struct.unpack("I", f.read(4))[0]
            dtype = f.read(dtype_len).decode("utf-8")
            schema.append((name, dtype))

        # Filter schema if needed_cols is specified
        if needed_cols:
            schema = [col for col in schema if col[0] in needed_cols]

        data = {name: [] for name, _ in schema}
        while True:
            try:
                for name, dtype in schema:
                    value = unpack_value(f, dtype)
                    data[name].append(value)
            except Exception:
                break
        return data
