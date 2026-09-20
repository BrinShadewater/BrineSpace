"""Remove the props the owner marked for removal in the Studio.

    python tools/tileset_library/sweep.py --dry-run
    python tools/tileset_library/sweep.py
    python tools/tileset_library/sweep.py --ids ids.json --why "warships: excluded category"

The Studio only marks; nothing is deleted until this runs. For each mark it removes the
registration, blanks the art on its sheet (written atomically), and logs what went to
removed.json so a later merge cannot resurrect it. A prop that is also starred is the
owner's call: it is left alone and reported.

With --ids an agent removes props it has looked at and judged to be outside what the
owner wants (the exclusion list: vehicles, ships, mechs, weapons...). That path needs a
--why, records it in removed.json, and never reads or writes the owner's retired marks;
a starred prop is still left alone.

Removal can be undone:

    python tools/tileset_library/sweep.py --restore ads-310 hs-330 [--category "Derelict & damaged"]

brings props back from removed.json: the art is read out of the sheet's git history
(the newest version in which the box held the most art) and pasted only where the sheet
is empty now, so a neighbour is never painted over; the registration is rebuilt from the
log. `--show removed.png --set Undercity` draws what was removed without restoring it.

The mark files are owner data. This prints them before it touches anything.
"""
import argparse, collections, io, subprocess

from PIL import Image

import numpy as np

from common import (LIB, OPAQUE, PREFIX, PROPS, REPO, load_json, load_props, load_rgba, next_numbers, print_marks,
                    refresh_variants, save_json, save_png_atomic, set_geometry, sheet_of, trim)
from register import KIND


def _remove(going, props, alias, reasons):
    """Drop registrations, blank their art, log them, and keep variants and aliases honest."""
    by_sheet = collections.defaultdict(list)
    for e in going.values(): by_sheet[sheet_of(e)].append(e)
    staying = collections.defaultdict(list)
    for e in props:
        if e["id"] not in going: staying[sheet_of(e)].append([int(v) for v in e["region"]])
    for sheet, entries in by_sheet.items():
        A = load_rgba(REPO / sheet).copy()
        # Boxes overlap where props sit close. Blanking a whole box took slivers out
        # of five neighbours the owner had kept; blank only what no kept prop covers.
        protect = np.zeros(A.shape[:2], bool)
        for x, y, w, h in staying[sheet]: protect[y:y + h, x:x + w] = True
        for e in entries:
            x, y, w, h = [int(v) for v in e["region"]]
            wipe = np.zeros(A.shape[:2], bool); wipe[y:y + h, x:x + w] = True
            A[wipe & ~protect] = 0
        save_png_atomic(REPO / sheet, A)
    removed = load_json(LIB / "removed.json", {})
    for k, e in going.items():
        removed[k] = {"label": e["label"], "tileset": e["tileset"], "source": e["source"], "region": e["region"],
                      "category": e["category"]}
        if e.get("title"): removed[k]["title"] = e["title"]
        if reasons.get(k): removed[k]["why"] = reasons[k]
    save_json(PROPS, [e for e in props if e["id"] not in going])
    save_json(LIB / "removed.json", removed, indent=1)
    refresh_variants({e["id"] for e in props if e["id"] not in going})
    # an alias to a prop that no longer exists points at nothing; a layout using it draws nothing, as intended
    save_json(LIB / "merged.json", {k: v for k, v in alias.items() if v not in going}, indent=1)


def remove_ids(reasons):
    """Remove props a reviewer judged excluded: {id: why}. Starred props are never removed,
    and the owner's retired marks are neither read nor written."""
    alias = load_json(LIB / "merged.json", {})
    # Anything the owner has starred, renamed or moved is theirs. A reviewer removed a
    # zombie crewman as a "humanoid figure" that the owner had deliberately refiled.
    touched = set()
    for name in ("favourites", "names", "categories"):
        for key in load_json(LIB / f"{name}.json", {}) or []:
            k = key.replace(PREFIX, ""); touched.add(alias.get(k, k))
    props = load_props(); by_id = {e["id"]: e for e in props}
    going = {k: by_id[k] for k in reasons if k in by_id and k not in touched}
    kept = [k for k in reasons if k in touched]
    if kept: print(f"   kept because the owner starred, renamed or moved them: {kept}")
    if going: _remove(going, props, alias, reasons)
    return len(going)


_history = {}


def sheet_history(sheet):
    """Every committed version of a sheet, newest first, following the folder renames."""
    if sheet not in _history:
        def git(*a, **k): return subprocess.run(["git", *a], cwd=REPO, capture_output=True, **k).stdout
        log = git("log", "--follow", "--format=#%H", "--name-only", "--", sheet).decode().split()
        versions, commit = [], None
        for token in log:
            if token.startswith("#"): commit = token[1:]; continue
            blob = git("cat-file", "-p", f"{commit}:{token}")
            if blob.startswith(b"version https://git-lfs"): blob = git("lfs", "smudge", input=blob)
            try: versions.append(np.asarray(Image.open(io.BytesIO(blob)).convert("RGBA")))
            except Exception: pass
        _history[sheet] = versions
    return _history[sheet]


def removed_art(entry):
    """The art a removed prop had: from the newest version of its sheet where its box held the most."""
    x, y, w, h = [int(v) for v in entry["region"]]
    best = None
    for A in sheet_history(entry["source"].replace("res://", "")):
        if A.shape[0] < y + h or A.shape[1] < x + w: continue
        n = int((A[y:y + h, x:x + w, 3] >= OPAQUE).sum())
        if best is None or n > best[0]: best = (n, A[y:y + h, x:x + w])
    return None if best is None or best[0] == 0 else best[1]


def restore(ids, category=None):
    removed = load_json(LIB / "removed.json", {}); props = load_props(); have = {e["id"] for e in props}
    labels = {e["label"] for e in props}; kinds = {v: k for k, v in KIND.items()}
    sheets, back = {}, []
    for k in ids:
        log = removed.get(k)
        if log is None or k in have: print(f"   {k}: not in removed.json, left alone"); continue
        art = removed_art(log)
        if art is None: print(f"   {k}: no art found in the sheet's history, left alone"); continue
        sheet = log["source"].replace("res://", "")
        A = sheets[sheet] if sheet in sheets else load_rgba(REPO / sheet).copy(); sheets[sheet] = A
        x, y, w, h = [int(v) for v in log["region"]]
        box = A[y:y + h, x:x + w]; empty = box[..., 3] < OPAQUE     # never paint over a neighbour
        box[empty] = art[empty]
        kind = log["label"].rpartition(" ")[0]
        e = {"id": k, "label": log["label"], "tileset": log["tileset"], "source": log["source"],
             "category": category or log.get("category") or kinds.get(kind, "Derelict & damaged"),
             "method": "Grid-aligned tileset region; raster unchanged"}
        if log.get("title"): e["title"] = log["title"]
        if e["label"] in labels: e["label"] = f"{kind} {next_numbers(props).get(kind, 0) + 1:03d}"
        set_geometry(e, A[..., 3] >= OPAQUE, *trim(A[..., 3] >= OPAQUE, x, y, w, h))
        props.append(e); labels.add(e["label"]); back.append(k); del removed[k]
        print(f"   {k}: restored as {e['label']} in {e['category']}")
    for sheet, A in sheets.items(): save_png_atomic(REPO / sheet, A)
    if back:
        save_json(PROPS, props); save_json(LIB / "removed.json", removed, indent=1)
    return back


def show(path, tileset=None, match=None):
    """Draw removed props on one page, numbered by id, so the owner can choose what comes back."""
    from PIL import ImageDraw
    removed = load_json(LIB / "removed.json", {})
    picks = [(k, v) for k, v in removed.items() if (not tileset or v["tileset"] == tileset)
             and (not match or match.lower() in (v.get("why", "") + v.get("title", "")).lower())]
    cells = [(k, v, removed_art(v)) for k, v in picks]; cells = [c for c in cells if c[2] is not None]
    width, pad, x, y, row, places = 1800, 14, 14, 14, 0, []
    for k, v, art in cells:
        s = 2 if max(art.shape[:2]) < 200 else 1
        w, h = art.shape[1] * s, art.shape[0] * s
        if x + w + pad > width: x, y, row = pad, y + row + 30, 0
        places.append((k, art, s, x, y)); x += max(w, 70) + pad; row = max(row, h)
    page = Image.new("RGBA", (width, y + row + 40), (92, 96, 104, 255)); draw = ImageDraw.Draw(page)
    for k, art, s, px, py in places:
        tile = Image.fromarray(art, "RGBA").resize((art.shape[1] * s, art.shape[0] * s), Image.NEAREST)
        page.alpha_composite(tile, (px, py)); draw.text((px, py + tile.size[1] + 2), k, fill=(255, 255, 255, 255))
    page.save(path); print(f"{len(places)} removed props drawn to {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ids", help="JSON list of prop ids an agent has judged should go")
    ap.add_argument("--why", help="the reason, recorded in removed.json (required with --ids)")
    ap.add_argument("--restore", nargs="+", metavar="ID", help="undo a removal: bring these props back")
    ap.add_argument("--category", help="with --restore: file them here instead of where they were")
    ap.add_argument("--show", metavar="PNG", help="draw removed props to a page instead of doing anything")
    ap.add_argument("--set", help="with --show: only this set"); ap.add_argument("--match", help="with --show: text in the reason or title")
    args = ap.parse_args()
    if args.show: show(args.show, args.set, args.match); return
    if args.restore:
        print(f"restored {len(restore(args.restore, args.category))} props. Commit the sheets, props.json and removed.json together."); return
    if args.ids and not args.why: ap.error("--ids needs --why")
    print("owner marks:"); print_marks()
    alias = load_json(LIB / "merged.json", {})
    marked = load_json(args.ids) if args.ids else load_json(LIB / "retired.json", [])
    retired = [alias.get(k, k) for k in (i.replace(PREFIX, "") for i in marked if i.startswith(PREFIX) or args.ids)]
    starred = {alias.get(k, k) for k in (i.replace(PREFIX, "") for i in load_json(LIB / "favourites.json", []))}
    props = load_props(); by_id = {e["id"]: e for e in props}
    kept = [k for k in retired if k in starred]
    going = {k: by_id[k] for k in dict.fromkeys(retired) if k not in starred and k in by_id}
    gone_already = [k for k in retired if k not in starred and k not in by_id]
    print(f"to remove: {len(going)} | kept because also starred: {kept} | already gone: {len(gone_already)}")
    for k, e in list(going.items())[:12]: print(f"   {k}  {e['label']} · {e['tileset']}")
    if args.dry_run or not going:
        print("dry run: nothing written" if args.dry_run else "nothing to sweep"); return

    _remove(going, props, alias, {k: args.why for k in going} if args.why else {})
    if not args.ids:                       # an agent's removal leaves the owner's marks exactly as they were
        # Marks on the game's own installations are not ours to sweep: keep them as they are.
        foreign = [i for i in load_json(LIB / "retired.json", []) if not i.startswith(PREFIX)]
        save_json(LIB / "retired.json", foreign + [PREFIX + k for k in kept], indent=1)
    print(f"swept {len(going)} props on {len({sheet_of(e) for e in going.values()})} sheets; {len(props) - len(going)} remain. Commit the sheets, props.json and the mark files together.")


if __name__ == "__main__":
    main()
