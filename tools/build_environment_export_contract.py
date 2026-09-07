"""Record exact environment bytes expected in a real editor export.

This contract validates packaging, not art approval. Existing source ledgers
are verified first; the contract never changes their recorded hashes.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image
from audit_environment_pack import inspect_pack

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / "assets/environment"
LEGACY_PACKS = {"seabed-v1", "wrecked-rooms-v1", "rock-blockers-v1"}


def discover_source_ledgers(environment):
    """Every raster pack must have provenance; new folders need no allowlist edit."""
    packs = set()
    for path in environment.rglob("*.png"):
        relative = path.relative_to(environment)
        if len(relative.parts) < 2:
            raise ValueError("Environment PNG must belong to a pack: " + str(path))
        packs.add(environment / relative.parts[0])
    ledgers = []
    for pack in sorted(packs):
        if pack.name in LEGACY_PACKS:
            continue  # Historical schemas retain their dedicated hash verification.
        ledger = pack / "source-ledger.json"
        if not ledger.is_file():
            ledger = pack / "manifest.json"
        if not ledger.is_file():
            raise ValueError("Environment pack has no source ledger: " + str(pack))
        ledgers.append(ledger)
    return ledgers


def main():
    def verify_recorded_hashes(node, pack):
        if isinstance(node, dict):
            file = node.get("file", node.get("source"))
            if node.get("sha256") and isinstance(file, str) and file.endswith(".png"):
                path = (pack / file).resolve()
                if not path.is_relative_to(pack.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest() != node["sha256"]:
                    raise ValueError("Legacy recorded source mismatch: " + str(path))
            for value in node.values():
                verify_recorded_hashes(value, pack)
        elif isinstance(node, list):
            for value in node:
                verify_recorded_hashes(value, pack)

    for name in sorted(LEGACY_PACKS):
        pack = ENV / name
        verify_recorded_hashes(json.loads((pack / "manifest.json").read_text(encoding="utf-8")), pack)
    for ledger in discover_source_ledgers(ENV):
        report = inspect_pack(ledger)
        recorded = {row["file"] for row in report["sources"]}
        unregistered = sorted(path.relative_to(ledger.parent).as_posix()
                              for path in ledger.parent.rglob("*.png")
                              if path.relative_to(ledger.parent).as_posix() not in recorded)
        if unregistered:
            raise ValueError("Unregistered environment sources in " + str(ledger.parent)
                             + ": " + ", ".join(unregistered))
    records = []
    for path in sorted(ENV.rglob("*.png")):
        data = path.read_bytes()
        if data.startswith(b"version https://git-lfs.github.com/spec/"):
            raise ValueError("Fetch LFS before export: " + str(path))
        with Image.open(path) as image:
            size = list(image.size)
        records.append({"path": "res://" + path.relative_to(ROOT).as_posix(),
                        "sha256": hashlib.sha256(data).hexdigest(), "size": size})
    contract = {"purpose": "Export-byte verification; not art acceptance", "files": records,
                "png_count": len(records), "pack_count": len({p.parent for p in ENV.rglob('*.png')})}
    destination = ENV / "export-contract.json"
    destination.write_text(json.dumps(contract, indent=2)+"\n", encoding="utf-8")
    print(f"Export contract: {len(records)} PNGs across {contract['pack_count']} packs")


if __name__ == "__main__":
    main()
