# src/ccol_types.py
# Define CCOL-specific type mappings

import struct

# Map schema type names to struct format codes
TYPE_FORMATS = {
    "int32": "i",
    "float64": "d",
    "string": None  # handled separately
}

def pack_value(value, dtype):
    if dtype == "string":
        encoded = value.encode("utf-8")
        length = len(encoded)
        return struct.pack("I", length) + encoded
    else:
        fmt = TYPE_FORMATS[dtype]
        return struct.pack(fmt, value)

def unpack_value(f, dtype):
    if dtype == "string":
        length_bytes = f.read(4)
        length = struct.unpack("I", length_bytes)[0]
        return f.read(length).decode("utf-8")
    else:
        fmt = TYPE_FORMATS[dtype]
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, f.read(size))[0]
