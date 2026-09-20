"""Split a prop that is really two objects, the same way the Studio's Split button does.

    python tools/tileset_library/split.py <prop-id> [<prop-id> ...] [--dry-run]

Cuts at the emptiest line through the middle of the art, on whichever axis is emptier,
and refuses when no such line is at least half empty. The prop keeps its id as the first
part, so placed copies still resolve; the second part gets the id plus a letter, the next
label number of its kind, and the first part's title with "(second)" so the owner can
see the pair and rename it. Both parts are trimmed and given floor footprints.

There is no automatic splitting of the library: most tall boxes with a pinched middle
are single objects (hydrants, bunk beds, sinks). Someone must have looked.
"""
import argparse

import numpy as np

from common import OPAQUE, PROPS, REPO, load_props, load_rgba, next_numbers, save_json, set_geometry, sheet_of, trim


def seam(mask):
    """(axis, position) of the emptiest line through the middle, or None."""
    h, w = mask.shape
    best = None
    for axis, counts, span, length in (("row", mask.sum(1), w, h), ("col", mask.sum(0), h, w)):
        if length < 24: continue
        for i in range(int(length * 0.25), int(length * 0.75)):
            ratio = counts[i] / float(span); centred = abs(i - length * 0.5) / length
            if best is None or ratio < best[0] - 1e-4 or (abs(ratio - best[0]) <= 1e-4 and centred < best[1]):
                best = (ratio, centred, axis, i)
    if best is None or best[0] > 0.5: return None
    return best[2], best[3]


def split_prop(pid, props=None, write=True):
    own = props is None
    props = load_props() if own else props
    by_id = {e["id"]: e for e in props}
    e = by_id.get(pid)
    if e is None: return False
    mask = load_rgba(REPO / sheet_of(e))[..., 3] >= OPAQUE
    x, y, w, h = [int(v) for v in e["region"]]
    found = seam(mask[y:y + h, x:x + w])
    if found is None: return False
    axis, at = found
    boxes = [(x, y, w, at), (x, y + at, w, h - at)] if axis == "row" else [(x, y, at, h), (x + at, y, w - at, h)]
    parts = [trim(mask, *b) for b in boxes]
    if any(p is None or p[2] < 6 or p[3] < 6 for p in parts): return False
    suffix = "b"
    while pid + suffix in by_id: suffix = chr(ord(suffix) + 1)
    second = dict(e); second["id"] = pid + suffix
    kind = e["label"].rpartition(" ")[0]
    second["label"] = f"{kind} {next_numbers(props).get(kind, 0) + 1:03d}"
    if e.get("title"): second["title"] = e["title"] + " (second)"
    set_geometry(e, mask, *parts[0]); set_geometry(second, mask, *parts[1])
    props.append(second)
    if own and write: save_json(PROPS, props)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="+"); ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    props = load_props()
    for pid in args.ids:
        print(f"   {pid}: {'split' if split_prop(pid, props) else 'no clear seam, left alone'}")
    if not args.dry_run: save_json(PROPS, props)


if __name__ == "__main__":
    main()
