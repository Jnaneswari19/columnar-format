import csv
import struct
import zlib

def encode_int32(values):
    return b"".join(struct.pack("<i", int(v)) for v in values)

def encode_float64(values):
    return b"".join(struct.pack("<d", float(v)) for v in values)

def encode_strings(values):
    buf = bytearray()
    ends = []
    total = 0
    for s in values:
        b = s.encode("utf-8")
        buf.extend(b)
        total += len(b)
        ends.append(total)
    offsets = b"".join(struct.pack("<I", x) for x in ends)
    return bytes(buf), offsets

def compress_block(raw_bytes, level=6):
    return zlib.compress(raw_bytes, level)

def write_ccol(csv_file, ccol_file, schema):
    """
    schema = [("id", "int32"), ("value", "float64"), ("name", "string")]
    """
    # Read CSV into columns
    columns = {name: [] for name, _ in schema}
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for name, _ in schema:
                columns[name].append(row[name])

    header_meta = {}

    with open(ccol_file, "wb") as fh:
        # Write magic + header basics
        fh.write(b"CCOL")                 # Magic number
        fh.write(struct.pack("<B", 1))    # Version
        fh.write(struct.pack("<B", 0))    # Endianness (0 = little)
        fh.write(struct.pack("<Q", len(next(iter(columns.values())))))  # Row count
        fh.write(struct.pack("<I", len(schema)))  # Column count

        # Placeholder for schema + metadata (you can expand later)
        # For now, just record metadata in a dict

        # Write column blocks
        for name, typ in schema:
            if typ == "int32":
                raw = encode_int32(columns[name])
                comp = compress_block(raw)
                offset = fh.tell()
                fh.write(comp)
                header_meta[name] = {
                    "type": typ,
                    "offset": offset,
                    "comp_size": len(comp),
                    "raw_size": len(raw),
                }
            elif typ == "float64":
                raw = encode_float64(columns[name])
                comp = compress_block(raw)
                offset = fh.tell()
                fh.write(comp)
                header_meta[name] = {
                    "type": typ,
                    "offset": offset,
                    "comp_size": len(comp),
                    "raw_size": len(raw),
                }
            elif typ == "string":
                strings_raw, offsets_raw = encode_strings(columns[name])
                comp_strings = compress_block(strings_raw)
                comp_offsets = compress_block(offsets_raw)

                off_strings = fh.tell()
                fh.write(comp_strings)
                off_offsets = fh.tell()
                fh.write(comp_offsets)

                header_meta[name] = {
                    "type": typ,
                    "strings_offset": off_strings,
                    "strings_comp_size": len(comp_strings),
                    "strings_raw_size": len(strings_raw),
                    "offsets_offset": off_offsets,
                    "offsets_comp_size": len(comp_offsets),
                    "offsets_raw_size": len(offsets_raw),
                }

        # TODO: Write schema + metadata into header (currently stored in header_meta dict)
        # This will be needed for the reader to parse correctly.
