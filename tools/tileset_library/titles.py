"""Give library props real names, a set at a time.

    python tools/tileset_library/titles.py sheet "Wet Lab" --out C:/tmp/wetlab     # numbered pages to look at
    python tools/tileset_library/titles.py apply C:/tmp/wetlab-titles.json [--dry-run]

Labels are "<Kind> NNN", so search cannot find "locker". A title is what the prop is,
written by someone who looked at it. The pages number every prop in the set; the titles
file maps those numbers (or ids) to a title, optionally with a corrected category:

    {"set": "Wet Lab", "titles": {"0": "Fume hoods, pair", "171": ["Potted palm", "Plants & growing"]}}

Looking is the point. The colour-tag categories filed an eyewash station and an exit sign
under Plants and test-tube racks under Screens; a title pass is where that gets fixed.

Rules: the owner's own rename (names.json) always wins over a title. A repeated title
gets a number ("Alcohol pads box 2"), which also shows the owner where the duplicates
are. A changed category renumbers the label within its new kind; ids never change.
"""
import argparse, sys

from PIL import Image, ImageDraw

from common import PROPS, load_json, load_props, next_numbers, save_json, sheet_of
from register import KIND

PER_PAGE, COLS, CELL = 48, 8, 150


def ordered(props, set_name):
    chosen = [e for e in props if e["tileset"] == set_name]
    chosen.sort(key=lambda e: (e["category"], e["label"]))
    return chosen


def sheet(set_name, out):
    chosen = ordered(load_props(), set_name)
    if not chosen: sys.exit(f"no props in set {set_name!r}")
    cache = {}
    pages = (len(chosen) + PER_PAGE - 1) // PER_PAGE
    for page in range(pages):
        chunk = chosen[page * PER_PAGE:(page + 1) * PER_PAGE]
        img = Image.new("RGBA", (COLS * CELL + 20, ((len(chunk) + COLS - 1) // COLS) * (CELL + 18) + 16), (150, 160, 150, 255))
        d = ImageDraw.Draw(img)
        for k, e in enumerate(chunk):
            path = sheet_of(e)
            if path not in cache: cache[path] = Image.open(path).convert("RGBA")
            x, y, w, h = [int(v) for v in e["region"]]
            c = cache[path].crop((x, y, x + w, y + h)); s = min((CELL - 12) / c.width, (CELL - 12) / c.height, 3.0)
            c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.NEAREST)
            cx, cy = 10 + (k % COLS) * CELL, 8 + (k // COLS) * (CELL + 18)
            img.alpha_composite(c, (cx + (CELL - c.width) // 2, cy + (CELL - c.height) // 2))
            d.text((cx + 3, cy + CELL), f"{page * PER_PAGE + k}  {e['label']}", fill=(20, 20, 20, 255))
        img.save(f"{out}-{page}.png")
    # The numbers mean nothing once labels change, so pin them to ids.
    save_json(f"{out}-index.json", [e["id"] for e in chosen])
    print(f"{len(chosen)} props in {set_name!r} -> {pages} page(s) at {out}-N.png; numbers are pinned to ids in {out}-index.json "
          f"(name it as \"index\" in the titles file).")


def apply(path, dry_run):
    spec = load_json(path)
    props = load_props()
    by_id = {e["id"]: e for e in props}
    chosen = [by_id[i] for i in load_json(spec["index"]) if i in by_id] if spec.get("index") else ordered(props, spec["set"])
    numbers = next_numbers(props)
    used = {}
    for e in props:
        if e.get("title") and e["tileset"] != spec["set"]:
            used[e["title"].lower()] = used.get(e["title"].lower(), 0) + 1
    titled = moved = 0
    for key, value in spec["titles"].items():
        e = chosen[int(key)] if str(key).isdigit() else by_id.get(key)
        if e is None: sys.exit(f"unknown prop {key!r}")
        title, category = (value, None) if isinstance(value, str) else (value[0], value[1])
        title = " ".join(title.split())
        if category and category not in KIND: sys.exit(f"{key}: unknown category {category!r}")
        base = title.lower(); used[base] = used.get(base, 0) + 1
        e["title"] = title if used[base] == 1 else f"{title} {used[base]}"
        titled += 1
        if category and category != e["category"]:
            e["category"] = category
            kind = KIND[category]; numbers[kind] = numbers.get(kind, 0) + 1
            e["label"] = f"{kind} {numbers[kind]:03d}"; moved += 1
    missing = [e["label"] for e in chosen if not e.get("title")]
    print(f"{spec['set']}: {titled} titled, {moved} re-filed, {len(missing)} still untitled" + (f" ({missing[:5]}…)" if missing else ""))
    if dry_run:
        print("dry run: nothing written"); return
    save_json(PROPS, props)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="action", required=True)
    s = sub.add_parser("sheet"); s.add_argument("set_name"); s.add_argument("--out", required=True)
    a = sub.add_parser("apply"); a.add_argument("titles"); a.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.action == "sheet": sheet(args.set_name, args.out)
    else: apply(args.titles, args.dry_run)


if __name__ == "__main__":
    main()
