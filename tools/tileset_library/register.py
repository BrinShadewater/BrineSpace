"""Register picked props from a scan into the library, or validate the live registry.

    python tools/tileset_library/register.py --scan scan.json --converted "C:/converted/Pack" \
        --set "Undercity" --domain "Ship interior" [--picks picks.json] [--sheet-domains map.json]
    python tools/tileset_library/register.py --validate

`picks.json` maps a sheet to the per-sheet indices chosen from the contact sheet:
{"13.png": [0, 1, 4], "tile-B-01.png": "all"}. Without it every scanned prop is taken.

A prop with a measured theme keeps it (foliage, screen glow, water, warm crate tones);
otherwise it takes its sheet's domain, else the pack's. That fallback is coarse on
purpose: the owner corrects with Move to category in the Studio.

Only referenced sheets are copied into the repo. Run merge.py next, then tone.py.
"""
import argparse, os, shutil, sys

import numpy as np
from PIL import Image

from common import (ART, LIB, PROPS, RES_ART, REPO, load_json, load_props, load_rgba, next_numbers,
                    save_json, set_geometry, sheet_of, slug, trim, OPAQUE)

KIND = {"Seating & tables": "Seating", "Storage": "Storage", "Screens & computers": "Screens",
        "Lab & science": "Lab", "Plants & growing": "Plants", "Power & reactor": "Power",
        "Industrial & workshop": "Industrial", "Water & marine": "Marine", "Medical": "Medical",
        "Food & kitchen": "Food", "Mining": "Mining", "Military & security": "Security",
        "Ship interior": "Interior", "Offworld surface": "Surface", "Shelter & survival": "Shelter",
        "Derelict & damaged": "Derelict"}


def tags(rgba):
    """Colour evidence for what a prop is, from its own pixels."""
    a = np.asarray(rgba, np.int16)
    m = a[..., 3] > 128
    if m.sum() < 60:
        return {}
    r, g, b = a[..., 0][m], a[..., 1][m], a[..., 2][m]
    n = float(m.sum())
    return {"foliage": float(((g > r + 14) & (g > b + 14) & (g > 45)).sum() / n),
            "screen": float(((b > 120) & (b > r + 45) & (g > r + 10)).sum() / n),
            "warm": float(((r > g + 12) & (g > b + 8) & (r > 60)).sum() / n),
            "water": float(((b > 90) & (b > r + 30) & (b >= g)).sum() / n)}


def categorise(t, w_tiles, h_tiles, fallback, neon=False):
    if t.get("foliage", 0) > 0.14: return "Plants & growing"
    # A pack lit in neon reads as water by colour alone; trust the sheet's domain there.
    if t.get("water", 0) > 0.30 and not neon: return "Water & marine"
    if t.get("screen", 0) > 0.06: return "Screens & computers"
    if t.get("warm", 0) > 0.22 and w_tiles <= 3 and h_tiles <= 3: return "Storage"
    return fallback


def validate(props):
    """The registration contract, checked against the sheets themselves."""
    problems, masks, ids = [], {}, set()
    for e in props:
        where = f"{e.get('id')} ({e.get('label')})"
        if e["id"] in ids: problems.append(f"{where}: duplicate id")
        ids.add(e["id"])
        path = REPO / sheet_of(e)
        if not path.exists():
            problems.append(f"{where}: missing sheet {sheet_of(e)}"); continue
        if path not in masks:
            masks[path] = load_rgba(path)[..., 3] >= OPAQUE
        mask = masks[path]
        x, y, w, h = [int(v) for v in e["region"]]
        if w <= 0 or h <= 0 or y + h > mask.shape[0] or x + w > mask.shape[1]:
            problems.append(f"{where}: region outside its sheet"); continue
        if trim(mask, x, y, w, h) != (x, y, w, h):
            problems.append(f"{where}: region is not trimmed to its opaque art")
        want = [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]
        if [[int(p[0]), int(p[1])] for p in e["pieces"][0]] != want:
            problems.append(f"{where}: pieces are not the absolute sheet rectangle of the region")
        if float(e["display_width"]) != float(w):
            problems.append(f"{where}: display_width is not the region width")
        f = e.get("footprint")
        if not f or any(v < 0 or v > 1 for v in f) or f[0] + f[2] > 1.0001 or f[1] + f[3] > 1.0001:
            problems.append(f"{where}: footprint missing or outside the rect")
        if e.get("category") not in KIND:
            problems.append(f"{where}: unknown category {e.get('category')!r}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--validate", action="store_true", help="check the live registry against the contract and exit")
    ap.add_argument("--scan"); ap.add_argument("--converted")
    ap.add_argument("--set", dest="set_name", help="in-universe set name shown in the Studio")
    ap.add_argument("--domain", help="category for props with no measured theme")
    ap.add_argument("--picks"); ap.add_argument("--sheet-domains")
    ap.add_argument("--neon", action="store_true", help="pack is neon-lit: do not read blue as water")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    props = load_props()
    if args.validate:
        problems = validate(props)
        for p in problems[:40]: print("  " + p)
        print(f"{len(props)} props checked, {len(problems)} problem(s)")
        sys.exit(1 if problems else 0)

    for need in ("scan", "converted", "set_name", "domain"):
        if not getattr(args, need): ap.error(f"--{need.replace('_name', '')} is required")
    if args.domain not in KIND: ap.error(f"--domain must be one of: {', '.join(KIND)}")
    root = args.converted.replace("\\", "/").rstrip("/") + "/"
    items = load_json(args.scan)
    picks = load_json(args.picks) if args.picks else None
    sheet_domains = load_json(args.sheet_domains, {}) if args.sheet_domains else {}
    by = {}
    for e in items: by.setdefault(e["sheet"], []).append(e)
    chosen = []
    for sheet, es in by.items():
        want = "all" if picks is None else picks.get(sheet, picks.get(os.path.basename(sheet), []))
        chosen += es if want == "all" else [es[i] for i in want if i < len(es)]
    have = {e["id"] for e in props}
    clash = [e["id"] for e in chosen if e["id"] in have]
    if clash: sys.exit(f"ids already registered (choose another --code when scanning): {clash[:5]}")

    folder = slug(args.set_name)
    numbers, out, sheets = next_numbers(props), [], {}
    for e in chosen:
        if e["sheet"] not in sheets:
            sheets[e["sheet"]] = np.asarray(Image.open(root + e["sheet"]).convert("RGBA"))
        rgba = sheets[e["sheet"]]; mask = rgba[..., 3] >= OPAQUE; t = e["tile"]
        box = trim(mask, e["col"] * t, e["row"] * t, e["w"] * t, e["h"] * t)
        if box is None: continue
        x, y, w, h = box
        fallback = sheet_domains.get(os.path.basename(e["sheet"]), args.domain)
        category = categorise(tags(rgba[y:y + h, x:x + w]), e["w"], e["h"], fallback, args.neon)
        kind = KIND[category]; numbers[kind] = numbers.get(kind, 0) + 1
        entry = {"id": e["id"], "label": f"{kind} {numbers[kind]:03d}", "category": category,
                 "tileset": args.set_name, "source": f"{RES_ART}{folder}/{e['sheet']}",
                 "method": "Grid-aligned tileset region; raster unchanged"}
        out.append(set_geometry(entry, mask, x, y, w, h))

    print(f"{len(out)} of {len(items)} scanned props -> set {args.set_name!r} in assets/new-tilesets/{folder}/")
    for category in sorted({e["category"] for e in out}):
        print(f"   {sum(1 for e in out if e['category'] == category):>4}  {category}")
    if args.dry_run:
        print("dry run: nothing written"); return
    for sheet in sheets:                                   # referenced sheets only
        dst = ART / folder / sheet
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root + sheet, dst)
    save_json(PROPS, props + out)
    print(f"registry now {len(props) + len(out)} props; copied {len(sheets)} sheets. Next: merge.py, then tone.py.")


if __name__ == "__main__":
    main()
