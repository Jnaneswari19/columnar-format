# src/writer.py (snippet)
import zlib, struct

def encode_int32(col):
    return b"".join(struct.pack("<i", int(v)) for v in col)

def encode_float64(col):
    return b"".join(struct.pack("<d", float(v)) for v in col)

def encode_strings(col):
    buf = bytearray()
    ends = []
    total = 0
    for s in col:
        b = s.encode("utf-8")
        buf.extend(b)
        total += len(b)
        ends.append(total)
    offsets = b"".join(struct.pack("<I", x) for x in ends)
    return bytes(buf), offsets

def compress_block(raw_bytes, level=6):
    return zlib.compress(raw_bytes, level)

def write_columns(fh, schema, columns_data, header_meta):
    # columns_data: dict {name: list(values)}
    for name, typ in schema:
        if typ == "int32":
            raw = encode_int32(columns_data[name])
        elif typ == "float64":
            raw = encode_float64(columns_data[name])
        elif typ == "string":
            strings_bytes, offsets_bytes = encode_strings(columns_data[name])
            comp_strings = compress_block(strings_bytes)
            comp_offsets = compress_block(offsets_bytes)
            off_strings = fh.tell()
            fh.write(comp_strings)
            off_offsets = fh.tell()
            fh.write(comp_offsets)
            header_meta[name] = {
                "type": "string",
                "strings_offset": off_strings,
                "strings_comp_size": len(comp_strings),
                "strings_raw_size": len(strings_bytes),
                "offsets_offset": off_offsets,
                "offsets_comp_size": len(comp_offsets),
                "offsets_raw_size": len(offsets_bytes),
            }
            continue
        else:
            raise ValueError(f"Unknown type {typ}")

        comp = compress_block(raw)
        offset = fh.tell()
        fh.write(comp)
        header_meta[name] = {
            "type": typ,
            "offset": offset,
            "comp_size": len(comp),
            "raw_size": len(raw),
        }
