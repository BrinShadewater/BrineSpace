"""Art-free guard for authored room layouts (rooms/full-wall-v1/default-layouts.json).

RoomLayoutStore reads layouts by string keys and silently ignores any key it does
not understand, so a renamed asset, a typo'd prefix or an orphaned copy just
disappears from the game. This catches those before they ship.

  python tests/test_layout_keys.py               # check the authored defaults
  python tests/test_layout_keys.py --user FILE   # also check a copy of user://room_layouts.json (read-only)
  python tests/test_layout_keys.py --self-test   # prove the checks fire
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOMS = ROOT / "rooms/full-wall-v1"
# Prefixes read by room_layout_store.gd, room_asset_library.gd and room_layout_editor.gd.
PREFIXES = {"size", "flip", "hidden", "order", "copy", "source", "library", "decor", "variant",
            "variant_extent", "portable", "lighting", "locked", "group",
            # Editor layers: floor tiles/finishes (floor_tile_tools.gd) and light/riser prop ids.
            "tile", "floor", "light", "riser"}
POINT_PREFIXES = {"copy", "library", "decor", "light", "riser"}


def is_point(value):
    return value is None or (isinstance(value, list) and len(value) == 2
                             and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value))


def library_ids():
    ids = {"library/" + p.stem for p in (ROOMS / "registrations").glob("*.json")}
    for entry in json.loads((ROOMS / "common-assets.json").read_text(encoding="utf-8")):
        ids.add("library/common-" + entry["id"])
    return ids


def check(layouts, assets, libraries, label):
    errors = []
    for layout_key, entries in layouts.items():
        where = f"{label}: {layout_key}"
        match = re.fullmatch(r"(.+)/([0-3])", layout_key)
        if not match:
            errors.append(f"{where}: layout key is not <asset>/<quarter 0-3>")
        elif match.group(1) not in assets and not re.fullmatch(r"room-\d+", match.group(1)):
            errors.append(f"{where}: asset is not in editor-catalog.json")
        if not isinstance(entries, dict):
            errors.append(f"{where}: layout is not an object"); continue
        for key, value in entries.items():
            if key.startswith("__"):
                continue
            prefix = key.split("/", 1)[0] if "/" in key else ""
            if prefix and prefix not in PREFIXES:
                errors.append(f"{where}: unknown key prefix '{prefix}/' in '{key}'")
                continue
            if (not prefix or prefix in POINT_PREFIXES) and not is_point(value):
                errors.append(f"{where}: '{key}' must be null or [x, y], got {json.dumps(value)[:40]}")
            if prefix == "flip" and not (isinstance(value, list) and len(value) == 2 and all(isinstance(v, bool) for v in value)):
                errors.append(f"{where}: '{key}' must be [bool, bool]")
            if prefix == "library" and key.split("#")[0] not in libraries:
                errors.append(f"{where}: '{key}' names no registration or common asset")
            if prefix == "copy" and "source/" + key not in entries:
                errors.append(f"{where}: '{key}' has no 'source/{key}'")
            if prefix == "source" and key[len("source/"):] not in entries:
                errors.append(f"{where}: '{key}' is orphaned (its copy is gone)")
    return errors


def load_layouts(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("layouts"), dict):
        raise SystemExit(f"{path}: not a version-1 layouts file (the game would ignore it entirely)")
    return data["layouts"]


def self_test(assets, libraries):
    asset = sorted(assets)[0]
    library = sorted(libraries)[0]
    good = {f"{asset}/0": {"a": [1, 2], "flip/a": [True, False], "copy/a#2": [0, 0], "source/copy/a#2": "a",
                           library + "#2": None, "__free_placement": True}}
    assert check(good, assets, libraries, "self") == [], check(good, assets, libraries, "self")
    bad = {f"{asset}/4": {}, "no-such-asset/0": {}, f"{asset}/1": {
        "szie/a": [1, 1], "a": "left", "flip/a": [1, 0], "library/missing": [0, 0],
        "copy/b#2": [0, 0], "source/copy/c#2": "c"}}
    found = check(bad, assets, libraries, "self")
    for needle in ["quarter", "editor-catalog", "'szie/'", "'a' must be", "'flip/a'", "library/missing",
                   "'copy/b#2' has no", "'source/copy/c#2' is orphaned"]:
        assert any(needle in e for e in found), f"self-test: no error mentioning {needle}"
    print(f"self-test: {len(found)} planted faults all detected")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--user", help="read-only path to a copy of user://room_layouts.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    assets = {entry["asset"] for entry in json.loads((ROOMS / "editor-catalog.json").read_text(encoding="utf-8"))}
    libraries = library_ids()
    if args.self_test:
        self_test(assets, libraries); return 0
    layouts = load_layouts(ROOMS / "default-layouts.json")
    errors = check(layouts, assets, libraries, "default-layouts.json")
    if args.user:
        errors += check(load_layouts(args.user), assets, libraries, Path(args.user).name)
    for error in errors:
        print("FAIL", error)
    print(f"{len(layouts)} authored layouts checked, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
