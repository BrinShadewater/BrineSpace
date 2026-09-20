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

The mark files are owner data. This prints them before it touches anything.
"""
import argparse, collections

import numpy as np

from common import (LIB, PREFIX, PROPS, REPO, load_json, load_props, load_rgba, print_marks, refresh_variants,
                    save_json, save_png_atomic, sheet_of)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ids", help="JSON list of prop ids an agent has judged should go")
    ap.add_argument("--why", help="the reason, recorded in removed.json (required with --ids)")
    args = ap.parse_args()
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
        removed[k] = {"label": e["label"], "tileset": e["tileset"], "source": e["source"], "region": e["region"]}
        if args.why: removed[k]["why"] = args.why
    save_json(PROPS, [e for e in props if e["id"] not in going])
    save_json(LIB / "removed.json", removed, indent=1)
    if not args.ids:                       # an agent's removal leaves the owner's marks exactly as they were
        # Marks on the game's own installations are not ours to sweep: keep them as they are.
        foreign = [i for i in load_json(LIB / "retired.json", []) if not i.startswith(PREFIX)]
        save_json(LIB / "retired.json", foreign + [PREFIX + k for k in kept], indent=1)
    refresh_variants({e["id"] for e in props if e["id"] not in going})
    # an alias to a prop that no longer exists points at nothing; a layout using it draws nothing, as intended
    save_json(LIB / "merged.json", {k: v for k, v in alias.items() if v not in going}, indent=1)
    print(f"swept {len(going)} props on {len(by_sheet)} sheets; {len(props) - len(going)} remain. Commit the sheets, props.json and the mark files together.")


if __name__ == "__main__":
    main()
