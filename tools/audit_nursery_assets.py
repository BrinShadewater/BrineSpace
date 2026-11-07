"""Read-only registration audit. Does not establish visual acceptance."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def audit():
    recipe = json.loads((ROOT / "rooms/modular/nursery-room.json").read_text())
    enabled = {}
    for resource in recipe["asset_roots"]:
        folder = ROOT / resource.removeprefix("res://")
        records = json.loads((folder / "registration.json").read_text())["assets"]
        for name, record in records.items():
            if not record.get("enabled_in_pilot"):
                continue
            path = folder / record["file"]
            assert path.resolve().is_relative_to(ROOT), path
            with Image.open(path) as source:
                source.load()
                assert list(source.size) == record["native_size"], (name, "native size")
                x0, y0, x1, y1 = record["bounds"]
                assert 0 <= x0 < x1 <= source.width, (name, "x bounds")
                assert 0 <= y0 < y1 <= source.height, (name, "y bounds")
            if record.get("clean_sha256"):
                assert hashlib.sha256(path.read_bytes()).hexdigest() == record["clean_sha256"], (name, "hash")
            assert name not in enabled, (name, "duplicate registration")
            enabled[name] = path
    for q in range(4):
        assert f"microscope_{q}" in enabled, (q, "missing directional microscope")
    for name in ["growth", "reservoir", "cartridge", "enamel", "floor"]:
        assert name in enabled, (name, "missing component")
    card = ROOT / "rooms/modular/nursery-card.png"
    provenance = json.loads(card.with_suffix(".provenance.json").read_text())
    assert hashlib.sha256(card.read_bytes()).hexdigest().upper() == provenance["sha256"].upper()
    print(f"ASSET AUDIT PASS: {len(enabled)} enabled registrations, native dimensions, bounds, recorded clean hashes, directional coverage and card provenance")
    for name, path in enabled.items():
        print(f"  {name}: {path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    audit()
