#!/usr/bin/env python3
"""Art-free card-binding parity gate.

The 47 room card bindings live in three GDScript tables that must agree:
  - scripts/room_card_art.gd        const PATHS
  - scripts/grid_canvas.gd          room_texture_paths
  - scripts/grid_canvas.gd          room_texture_variant_paths (variant[0])
plus the identity list in scripts/room_database.gd.

tests/test_room_catalog_cards.gd proves the same agreement *and* decodes the
PNGs, but it cannot run in CI (checkout is lfs:false by design). This check
parses the tables as text, so it runs anywhere, including LFS-free CI. It
verifies binding agreement and that each referenced file exists (an LFS
pointer file satisfies existence); it does NOT establish art acceptance.

Run: python3 tests/test_card_binding_parity.py   (exits non-zero on mismatch)
Self-check: --self-test proves the comparison can fail (negative control).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_block(text: str, marker: str) -> str:
    """Return the {...} literal that starts at the first '{' after marker."""
    start = text.index(marker)
    open_brace = text.index("{", start)
    depth = 0
    for i in range(open_brace, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace : i + 1]
    raise ValueError("Unbalanced braces after %r" % marker)


def parse_string_dict(block: str) -> dict:
    """'id': 'res://path' entries of a GDScript dictionary literal."""
    return dict(re.findall(r'"([A-Za-z0-9_]+)"\s*:\s*"(res://[^"]+)"', block))


def parse_array_dict(block: str) -> dict:
    """'id': ['res://a', 'res://b'] entries; values are path lists."""
    result = {}
    for room_id, arr in re.findall(r'"([A-Za-z0-9_]+)"\s*:\s*\[([^\]]*)\]', block):
        result[room_id] = re.findall(r'"(res://[^"]+)"', arr)
    return result


def compare(db_ids, cards, grid, variants, existing=None):
    """Return a list of mismatch descriptions (empty means parity holds)."""
    errors = []
    if set(cards) != set(db_ids):
        missing = sorted(set(db_ids) - set(cards))
        extra = sorted(set(cards) - set(db_ids))
        errors.append(f"PATHS vs database identities: missing={missing} extra={extra}")
    if cards != grid:
        keys = sorted(set(cards) ^ set(grid)) or sorted(
            k for k in cards if grid.get(k) != cards[k]
        )
        errors.append(f"room_texture_paths disagrees with PATHS at: {keys}")
    for room_id, paths in variants.items():
        if not paths:
            errors.append(f"room_texture_variant_paths[{room_id}] is empty")
        elif room_id in cards and paths[0] != cards[room_id]:
            errors.append(
                f"variant[0] for {room_id} is {paths[0]}, PATHS has {cards[room_id]}"
            )
    if existing is not None:
        for label, table in (("PATHS", cards), ("grid", grid)):
            for room_id, path in table.items():
                if path not in existing:
                    errors.append(f"{label}[{room_id}] references missing file {path}")
        for room_id, paths in variants.items():
            for path in paths:
                if path not in existing:
                    errors.append(f"variant[{room_id}] references missing file {path}")
    return errors


def load_tables():
    cards_src = (ROOT / "scripts/room_card_art.gd").read_text(encoding="utf-8")
    grid_src = (ROOT / "scripts/grid_canvas.gd").read_text(encoding="utf-8")
    db_src = (ROOT / "scripts/room_database.gd").read_text(encoding="utf-8")
    cards = parse_string_dict(extract_block(cards_src, "PATHS"))
    grid = parse_string_dict(extract_block(grid_src, "room_texture_paths"))
    variants = parse_array_dict(extract_block(grid_src, "room_texture_variant_paths"))
    db_ids = sorted(set(re.findall(r'"id"\s*:\s*"([a-z0-9_]+)"', db_src)))
    referenced = set()
    for table in (cards, grid):
        referenced.update(table.values())
    for paths in variants.values():
        referenced.update(paths)
    existing = {p for p in referenced if (ROOT / p[len("res://") :]).is_file()}
    return db_ids, cards, grid, variants, existing


def self_test() -> int:
    """Negative control: a gate that cannot fail proves nothing."""
    db = ["a", "b"]
    good = {"a": "res://x.png", "b": "res://y.png"}
    assert compare(db, good, dict(good), {"a": ["res://x.png"]}) == []
    bad_grid = dict(good, a="res://z.png")
    assert compare(db, good, bad_grid, {}), "grid drift must be detected"
    assert compare(db, dict(good, c="res://c.png"), dict(good), {}), (
        "identity drift must be detected"
    )
    assert compare(db, good, dict(good), {"a": ["res://wrong.png"]}), (
        "variant[0] drift must be detected"
    )
    print("CARD BINDING PARITY SELF-TEST PASS: all injected drifts detected")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    db_ids, cards, grid, variants, existing = load_tables()
    sane = len(cards) >= 40 and len(db_ids) >= 40
    errors = [] if sane else [
        f"Parser sanity: only {len(cards)} PATHS / {len(db_ids)} identities parsed"
    ]
    errors += compare(db_ids, cards, grid, variants, existing)
    for line in errors:
        print(f"ERROR: {line}")
    if not errors:
        print(
            "CARD BINDING PARITY PASS: %d identities, PATHS/grid/variant agreement, "
            "%d referenced files present (text-level; not art acceptance)"
            % (len(cards), len(existing))
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
