# src/reader.py (snippet)
import zlib, struct

def read_block(fh, offset, comp_size):
    fh.seek(offset)
    return zlib.decompress(fh.read(comp_size))

def decode_int32(raw):
    out = []
    for i in range(0, len(raw), 4):
        out.append(struct.unpack("<i", raw[i:i+4])[0])
    return out

def decode_float64(raw):
    out = []
    for i in range(0, len(raw), 8):
        out.append(struct.unpack("<d", raw[i:i+8])[0])
    return out

def decode_strings(strings_raw, offsets_raw):
    ends = [struct.unpack("<I", offsets_raw[i:i+4])[0] for i in range(0, len(offsets_raw), 4)]
    out = []
    start = 0
    for end in ends:
        out.append(strings_raw[start:end].decode("utf-8"))
        start = end
    return out

def read_columns(fh, header, needed_cols=None):
    needed = set(needed_cols) if needed_cols else set(header["schema_names"])
    result = {}
    for name in needed:
        meta = header["columns"][name]
        if meta["type"] == "string":
            s_raw = read_block(fh, meta["strings_offset"], meta["strings_comp_size"])
            o_raw = read_block(fh, meta["offsets_offset"], meta["offsets_comp_size"])
            result[name] = decode_strings(s_raw, o_raw)
        elif meta["type"] == "int32":
            raw = read_block(fh, meta["offset"], meta["comp_size"])
            result[name] = decode_int32(raw)
        elif meta["type"] == "float64":
            raw = read_block(fh, meta["offset"], meta["comp_size"])
            result[name] = decode_float64(raw)
        else:
            raise ValueError(f"Unknown type {meta['type']}")
    return result
