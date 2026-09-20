"""Shared pieces for the tileset library tools.

The contract these helpers encode is written up in
skills/brinespace-room-pipeline/references/tileset-library.md. Read that first.
"""
import io, json, os, re
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
LIB = REPO / "rooms" / "tileset-library"
ART = REPO / "assets" / "new-tilesets"
PROPS = LIB / "props.json"
RES_ART = "res://assets/new-tilesets/"

# The owner's Studio decisions. Tracked, but between commits they are newer than
# HEAD: read them, remap them, write them back. Never restore them from git.
MARKS = ("favourites", "retired", "names", "categories")

LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)
OPAQUE = 24          # alpha at or above this counts as art
PREFIX = "library/tileset-"


def load_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(io.open(path, encoding="utf-8").read())


def save_json(path, data, indent=None):
    """Write beside the target, then swap it in. Opening the registry for writing
    truncates it first, and Windows refuses the open while the Studio or the Godot
    editor is reading the file: two intakes failed that way, and a failure after the
    truncate would have destroyed the registry. The swap is retried for a few seconds."""
    import time
    tmp = str(path) + ".tmp"
    with io.open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=indent))
    for attempt in range(12):
        try:
            os.replace(tmp, path); return
        except OSError:
            time.sleep(0.5)
    os.replace(tmp, path)


def load_props():
    return load_json(PROPS, [])


def sheet_of(entry):
    """Repo-relative path of the sheet an entry is cut from."""
    return entry["source"].replace("res://", "")


def load_rgba(path):
    return np.asarray(Image.open(path).convert("RGBA"))


def save_png_atomic(path, array):
    """Write beside the target, then replace: a half-written sheet is never loaded."""
    tmp = str(path) + ".tmp.png"
    Image.fromarray(np.asarray(array).astype(np.uint8), "RGBA").save(tmp)
    os.replace(tmp, path)


def luminance(rgb):
    return (np.asarray(rgb, np.float32) / 255.0) @ LUMA


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def trim(mask, x, y, w, h):
    """Shrink a box to the opaque art inside it. None when there is none."""
    m = mask[y:y + h, x:x + w]
    if not m.any():
        return None
    ys, xs = np.where(m)
    return x + int(xs.min()), y + int(ys.min()), int(xs.max() - xs.min()) + 1, int(ys.max() - ys.min()) + 1


def footprint(mask, x, y, w, h):
    """Floor footprint as fractions of the rect: the opaque bounds of the bottom band.

    The equipment shadow shades this instead of the whole art box, so a cut-out
    sprite does not sit on a dark rectangular mat."""
    m = mask[y:y + h, x:x + w]
    band = max(6, int(round(h * 0.22)))
    rows, off = m[h - band:, :], h - band
    if not rows.any():
        rows, off = m, 0
    ys, xs = np.where(rows)
    fy0, fy1 = off + int(ys.min()), off + int(ys.max()) + 1
    return [round(int(xs.min()) / w, 4), round(fy0 / h, 4),
            round((int(xs.max()) + 1 - int(xs.min())) / w, 4), round((fy1 - fy0) / h, 4)]


def set_geometry(entry, mask, x, y, w, h):
    """Region, absolute pieces, width and footprint for a box already trimmed."""
    entry["region"] = [float(x), float(y), float(w), float(h)]
    # Absolute sheet coordinates: the drawer subtracts a pivot of region centre-bottom.
    entry["pieces"] = [[[x, y], [x + w, y], [x + w, y + h], [x, y + h]]]
    entry["display_width"] = float(w)          # one sheet pixel is one room unit
    entry["footprint"] = footprint(mask, x, y, w, h)
    return entry


def next_numbers(props):
    """Highest label number in use for each kind word ("Storage 041" -> Storage: 41)."""
    seen = {}
    for e in props:
        kind, _, num = e["label"].rpartition(" ")
        if num.isdigit():
            seen[kind] = max(seen.get(kind, 0), int(num))
    return seen


def refresh_variants(valid_ids, alias=None):
    """Keep variants.json to props that exist: follow merges, drop the swept, and drop
    any family left with fewer than two members."""
    path = LIB / "variants.json"
    data = load_json(path)
    if not data:
        return 0
    alias = alias or {}
    groups, before = [], sum(len(g) for g in data.get("groups", []))
    for family in data.get("groups", []):
        members = []
        for pid in family:
            pid = alias.get(pid, pid)
            if pid in valid_ids and pid not in members:
                members.append(pid)
        if len(members) > 1:
            groups.append(members)
    save_json(path, {"groups": groups})
    return before - sum(len(g) for g in groups)


def print_marks():
    """Show the owner's marks before anything rewrites them."""
    for name in MARKS:
        data = load_json(LIB / f"{name}.json", [] if name in ("favourites", "retired") else {})
        print(f"  {name}: {len(data)} -> {json.dumps(data)[:300]}")


def remap_marks(alias):
    """Follow absorbed ids to their survivors in every mark file. Returns counts."""
    def fix(key):
        k = key.replace(PREFIX, "")
        return PREFIX + alias.get(k, k)
    changed = {}
    for name in MARKS:
        path = LIB / f"{name}.json"
        data = load_json(path)
        if data is None:
            continue
        if isinstance(data, list):
            new = []
            for key in data:
                if fix(key) not in new:
                    new.append(fix(key))
        else:
            new = {fix(k): v for k, v in data.items()}
        changed[name] = sum(1 for k in data if fix(k) != k)
        save_json(path, new, indent=1)
    return changed
