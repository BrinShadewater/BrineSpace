"""Split a prop that is really two objects, the same way the Studio's Split button does.

    python tools/tileset_library/split.py <prop-id> [<prop-id> ...] [--dry-run]

Cuts at the emptiest line through the middle of the art, on whichever axis is emptier,
and refuses when no such line is at least half empty. The prop keeps its id as the first
part, so placed copies still resolve; the second part gets the id plus a letter, the next
label number of its kind, and the first part's title with "(second)" so the owner can
see the pair and rename it. Both parts are trimmed and given floor footprints.

A split can be undone: `split.py --undo <prop-id>` joins the parts back into the first
one (give either part's id). The second part's id becomes an alias of the first in
merged.json, so a placed copy of it still draws, and the owner's marks follow it.

There is no automatic splitting of the library: most tall boxes with a pinched middle
are single objects (hydrants, bunk beds, sinks). Someone must have looked.
"""
import argparse

import numpy as np

from common import LIB, OPAQUE, free_id, PROPS, load_json, remap_marks, refresh_variants, REPO, load_props, load_rgba, next_numbers, save_json, set_geometry, sheet_of, trim


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
    second = dict(e); second["id"] = free_id(pid, by_id)
    kind = e["label"].rpartition(" ")[0]
    second["label"] = f"{kind} {next_numbers(props).get(kind, 0) + 1:03d}"
    if e.get("title"): second["title"] = e["title"] + " (second)"
    set_geometry(e, mask, *parts[0]); set_geometry(second, mask, *parts[1])
    props.append(second)
    if own and write: save_json(PROPS, props)
    return True


def parts_of(pid, by_id):
    """The first part's id and the ids split from it, given any of them."""
    base = pid[:-1] if pid[-1] in "bcdefgh" and pid[:-1] in by_id else pid
    return base, [base + c for c in "bcdefghijklmnopqrstuvwxyz" if base + c in by_id]


def rejoin(pid, props):
    by_id = {e["id"]: e for e in props}
    base, seconds = parts_of(pid, by_id)
    if base not in by_id or not seconds: return False
    first = by_id[base]
    if any(by_id[k]["source"] != first["source"] for k in seconds): return False
    boxes = [[int(v) for v in by_id[k]["region"]] for k in [base] + seconds]
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[0] + b[2] for b in boxes), max(b[1] + b[3] for b in boxes)
    mask = load_rgba(REPO / sheet_of(first))[..., 3] >= OPAQUE
    set_geometry(first, mask, *trim(mask, x0, y0, x1 - x0, y1 - y0))
    props[:] = [e for e in props if e["id"] not in seconds]
    alias = load_json(LIB / "merged.json", {})
    for k in seconds: alias[k] = base
    for k, v in alias.items():                      # an older alias to a part now points at the whole
        if v in seconds: alias[k] = base
    save_json(LIB / "merged.json", alias, indent=1)
    remap_marks({k: base for k in seconds}); refresh_variants({e["id"] for e in props}, alias)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="+"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--undo", action="store_true", help="join the parts of a split prop back together")
    args = ap.parse_args()
    props = load_props()
    if args.undo and args.dry_run: ap.error('--undo writes as it goes; there is no dry run')
    if args.undo:
        for pid in args.ids: print(f"   {pid}: {'rejoined' if rejoin(pid, props) else 'not a split prop, left alone'}")
        save_json(PROPS, props); return
    for pid in args.ids:
        print(f"   {pid}: {'split' if split_prop(pid, props) else 'no clear seam, left alone'}")
    if not args.dry_run: save_json(PROPS, props)


if __name__ == "__main__":
    main()
