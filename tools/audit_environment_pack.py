"""Verify an environment source ledger without refreshing its hashes or selections.

The ledger uses pack-relative source paths. The optional runtime registry is a
GDScript const SOURCES dictionary of string IDs to filenames (JSON syntax).
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image


def inspect_pack(ledger_path):
    ledger_path = Path(ledger_path).resolve()
    pack = ledger_path.parent
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    rows, selected_map, seen = [], {}, set()
    for asset in ledger["assets"]:
        identity = asset["id"]
        if identity in seen:
            raise ValueError(f"Duplicate identity: {identity}")
        seen.add(identity)
        selected = asset["selected_source"]
        files = [version["file"] for version in asset["versions"]]
        if len(files) != len(set(files)) or files.count(selected) != 1:
            raise ValueError(f"Selection must identify one recorded version: {identity}")
        selected_map[identity] = selected
        for version in asset["versions"]:
            source = (pack / version["file"]).resolve()
            if not source.is_relative_to(pack):
                raise ValueError(f"Source outside pack: {source}")
            data = source.read_bytes()
            if data.startswith(b"version https://git-lfs.github.com/spec/"):
                raise ValueError(f"Fetch Git LFS source before audit: {source.name}")
            digest = hashlib.sha256(data).hexdigest()
            if digest != version["sha256"]:
                raise ValueError(f"Source hash mismatch: {source.name}")
            with Image.open(source) as original:
                alpha = original.convert("RGBA").getchannel("A")
                counts = alpha.histogram()
                if version["file"] == selected and asset["kind"] in ("prop", "effect"):
                    if not counts[0] or not alpha.getbbox():
                        raise ValueError(f"Selected prop needs visible content and transparency: {source.name}")
                    if asset["kind"] == "effect" and not sum(counts[1:255]):
                        raise ValueError(f"Water effect requires partial-alpha pixels: {source.name}")
                rows.append({"id": identity, "file": version["file"], "sha256": digest,
                             "selected": version["file"] == selected,
                             "native_size": list(original.size), "mode": original.mode,
                             "transparent_pixels": counts[0],
                             "partial_alpha_pixels": sum(counts[1:255]),
                             "visible_bounds": alpha.getbbox(),
                             "stage": asset["stage"], "processing": "none"})
    registry = ledger.get("runtime_registry")
    if registry:
        path = (pack / registry).resolve()
        if not path.is_relative_to(pack):
            raise ValueError("Runtime registry outside pack")
        match = re.search(r"const SOURCES := (\{.*?\})", path.read_text(encoding="utf-8"), re.S)
        if not match or json.loads(match[1]) != selected_map:
            raise ValueError("Runtime source registry differs from selected ledger sources")
    recorded = {r["file"] for r in rows}
    unregistered = sorted(p.name for p in pack.glob("*.png") if p.name not in recorded)
    return {"identity_count": len(seen), "source_count": len(rows), "sources": rows,
            "unregistered_candidates": unregistered,
            "visual_acceptance": "not inferred by audit", "runtime_acceptance": "not inferred by audit"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output", type=Path, help="New JSON report; existing reports are never overwritten")
    args = parser.parse_args()
    report = inspect_pack(args.ledger)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(f'{report["identity_count"]} identities / {report["source_count"]} sources verified; '
          f'{len(report["unregistered_candidates"])} unregistered candidates; no art acceptance inferred')
