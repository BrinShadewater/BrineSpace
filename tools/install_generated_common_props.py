"""Install the owner's September 26 generated common props, preserving existing entries.

Uses calibrated PNGs unchanged, with matte plants and refined counters replacing
their earlier candidates. Run without --install to audit/review the selection.
Review boards are presentation composites; source artwork is never rewritten.
"""
from pathlib import Path
import argparse
import hashlib
import json

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "rooms/station-props-v2/props.json"
OUT = ROOT / "output/generated-common-install-2026-09-27"
PACKS = [
    "common-props-calibrated-2026-09-26", "plants-matte-2026-09-26",
    "common-surfaces-2026-09-26", "common-storage-2026-09-26",
    "common-everyday-2026-09-26", "wall-counters-2026-09-26",
    "dressed-counters-2026-09-26", "study-counters-2026-09-26",
    "room-counters-2026-09-26", "tables-seating-2026-09-26",
    "directional-lounge-2026-09-26", "lounge-variations-2026-09-26",
    "corner-counters-refined-2026-09-26", "remaining-corners-refined-2026-09-26",
    "metal-corner-variants-refined-2026-09-26",
    "servers-comms-shelves-2026-09-26", "submarine-utilities-2026-09-26",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection():
    selected = {}
    for pack in PACKS:
        folder = ROOT / "assets" / pack
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8-sig"))
        rows = manifest["assets"] if isinstance(manifest, dict) else manifest
        for row in rows:
            path = folder / "game-size" / (row["id"] + ".png")
            assert digest(path) == row["export_sha256"], f"Source changed: {path}"
            with Image.open(path) as image:
                assert image.mode == "RGBA" and list(image.size) == row["canvas"], path
                assert image.getchannel("A").getextrema() == (0, 255), path
            if row["id"] in selected:
                assert pack == "plants-matte-2026-09-26", row["id"]
            selected[row["id"]] = dict(row, path=path, pack=pack)
    assert len(selected) == 112
    return selected


def registration(key, row):
    w, h = row["canvas"]
    # Floor-contact rectangles, normalized to the full calibrated canvas. Foliage
    # and cabinet height must not block walking across their full projected art.
    boxes = [[0.06, 0.45, 0.88, 0.51]]
    corner = key.startswith("corner-") or key.startswith("metal-")
    if "plant" in key:
        boxes = [[0.30, 0.77, 0.40, 0.19]]
        if "tall" in key:
            boxes = [[0.32, 0.85, 0.36, 0.11]]
        elif "trough" in key:
            boxes = [[0.08, 0.65, 0.84, 0.31]]
    elif key.startswith("seat-") or key in ("common-chair-v2", "common-folding-stool"):
        boxes = [[0.15, 0.53, 0.70, 0.43]]
    elif key.startswith("surface-") or "table" in key or key.startswith("dining-"):
        boxes = [[0.06, 0.30, 0.88, 0.66]]
    elif key.startswith("lounge-") or key == "common-couch-v2":
        boxes = [[0.06, 0.30, 0.88, 0.66]]
    elif "bookcase" in key or "locker" in key or "shel" in key or "rack" in key or "cubb" in key:
        boxes = [[0.06, 0.72, 0.88, 0.24]]
    if corner:
        east = key.endswith("-east") or key == "corner-sink-refined"
        boxes = [[0.04, 0.25, 0.92, 0.23], [0.72 if east else 0.04, 0.48, 0.24, 0.48]]
    label = key.removeprefix("common-").removesuffix("-v2").replace("-", " ").title()
    label = label.replace("Seat ", "").replace("Surface ", "")
    labels = {
        "corner-wood-refined": "Corner Wood Storage West",
        "corner-sink-refined": "Corner Sink Counter East",
        "plant-succulent": "Plant Succulent (Tabletop)",
    }
    entry = {
        "id": "sp-generated-" + key,
        "label": labels.get(key, label),
        "category": "common",
        "source": "res://" + row["path"].relative_to(ROOT).as_posix(),
        "region": [0, 0, w, h],
        "pieces": [[[0, 0], [w, 0], [w, h], [0, h]]],
        "footprint": boxes[0],
        "collision_boxes": boxes,
        "display_width": row["suggested_display_width"],
        "wall_contact": [],
        "default_rooms": [],
    }
    if corner:
        entry["corner"] = "east" if east else "west"
    if key == "common-comms-panel":
        entry["wall_attachment"] = True
        entry["collision_boxes"] = []
        entry["footprint"] = [0, 0, 0, 0]
        entry["label"] = "Wall Comms Panel"
    return entry


def review_boards(rows, entries):
    items = list(rows.items())
    for page, start in enumerate(range(0, len(items), 20)):
        page_items = items[start:start + 20]
        cell_w = max(375, max(row["canvas"][0] for _, row in page_items)+16)
        cell_h = max(300, max(row["canvas"][1] for _, row in page_items)+34)
        sheet = Image.new("RGB", (cell_w*4, cell_h*5), "#25343d")
        draw = ImageDraw.Draw(sheet)
        for n, (key, row) in enumerate(page_items):
            x, y = (n % 4) * cell_w, (n // 4) * cell_h
            im = Image.open(row["path"])
            # Native PNG pixels, never enlarged. Tall rows fit the 300px cell.
            sheet.paste(im, (x + (cell_w-im.width)//2, y+5), im)
            draw.text((x+8, y+cell_h-26), key, fill="white")
        sheet.save(OUT / f"selection-{page+1}.jpg", quality=92)
    audit = [dict(id=e["id"], source=e["source"], sha256=r["export_sha256"],
                  display_width=e["display_width"], pack=r["pack"])
             for e, r in zip(entries, rows.values())]
    (OUT / "selection.json").write_text(json.dumps(audit, indent=2)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    selected = selection()
    entries = [registration(k, r) for k, r in selected.items()]
    review_boards(selected, entries)
    original = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing = {e["id"]: e for e in original}
    for entry in entries:
        if entry["id"] in existing:
            assert existing[entry["id"]] == entry, f"Existing registration differs: {entry['id']}"
    added = [e for e in entries if e["id"] not in existing]
    if args.install and added:
        # Keep all unrelated catalog entries and formatting unchanged.
        before = CATALOG.read_text(encoding="utf-8")
        backup = OUT / "catalog-before.json"
        if not backup.exists():
            backup.write_text(before, encoding="utf-8")
        pos = before.rfind("]")
        suffix = ",\n" + ",\n".join(" " + json.dumps(e, indent=1).replace("\n", "\n ") for e in added) + "\n]"
        after = before[:pos].rstrip() + suffix + "\n"
        parsed = json.loads(after)
        assert parsed[:len(original)] == original
        CATALOG.write_text(after, encoding="utf-8")
    print(f"{len(entries)} selected, {len(added)} {'installed' if args.install else 'new'}; catalog {len(original)+len(added)}. Review: {OUT}")


if __name__ == "__main__":
    main()
