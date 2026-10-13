"""Install the reviewed dry Marsh carry chain without rebuilding unrelated art.

All target PNGs are guarded against the current palette lock. The first install
backs up exact local bytes; canonical rebuilds call install_turns(backup=False)
after the historical turn builders have emitted their source-based defaults.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"
CHAIN = ROOT / "character/marsh-carry-chain-v1"
CARRY = ROOT / "character/marsh-carry-match-v1/frames"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def turn_targets() -> tuple[dict[Path, Path], list[Path]]:
    catalog = json.loads((RUNTIME / "catalog.json").read_text())
    targets = {}
    provenance = []
    for relative in catalog["body"]:
        if not relative.startswith("supplemental/carry-turn-"):
            continue
        manifest = RUNTIME / relative
        data = json.loads(manifest.read_text())
        provenance.append(manifest.parent / "provenance.json")
        for state in data["states"]:
            selected = CHAIN / "turns-matched" / state["id"]
            if len(state["frameFiles"]) != len(list(selected.glob("[0-9][0-9][0-9].png"))):
                raise ValueError("Turn count mismatch: " + state["id"])
            for i, item in enumerate(state["frameFiles"]):
                target = (manifest.parent / item).resolve()
                source = selected / f"{i:03}.png"
                if target in targets:
                    raise ValueError("Duplicate turn target: " + str(target))
                targets[target] = source
    if len(provenance) != 6 or len(targets) != 76:
        raise ValueError(f"Expected six turn manifests and 76 frames, got {len(provenance)} and {len(targets)}")
    return targets, provenance


def install_turns(backup: bool = False) -> list[dict]:
    targets, provenance = turn_targets()
    records = []
    for target, source in sorted(targets.items()):
        if backup:
            saved = CHAIN / "installation-backup" / target.relative_to(ROOT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            if saved.exists():
                raise ValueError("Backup already exists: " + str(saved))
            shutil.copy2(target, saved)
        records.append({"target": target.relative_to(ROOT).as_posix(),
                        "beforeSha256": digest(target), "selectedSha256": digest(source)})
        shutil.copy2(source, target)
    for path in provenance:
        data = json.loads(path.read_text()) if path.exists() else {}
        if backup:
            saved = CHAIN / "installation-backup" / path.relative_to(ROOT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            if saved.exists():
                raise ValueError("Backup already exists: " + str(saved))
            shutil.copy2(path, saved)
        data["selectedOverride"] = {
            "revision": "marsh-carry-chain-v1",
            "source": "character/marsh-carry-chain-v1/turns-matched/",
            "meaning": "The historical source fields above describe the superseded turn interiors; current runtime PNGs come from the matched carry chain.",
        }
        path.write_text(json.dumps(data, indent=2) + "\n")
    return records


def install_full() -> dict:
    base = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
    corrections = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
    targets = {}
    for direction in ("south", "north", "east", "west"):
        for i in range(4):
            targets[RUNTIME / "frames/bare" / f"carry-{direction}" / f"{i:03}.png"] = CARRY / direction / f"{i:03}.png"
        for action in ("pickup", "unload", "cargo-unload"):
            for i in range(4):
                key = f"{action}-{direction}"
                targets[RUNTIME / "frames/bare" / key / f"{i:03}.png"] = CHAIN / "frames" / key / f"{i:03}.png"
    turns, _ = turn_targets()
    targets.update(turns)
    if len(targets) != 140:
        raise ValueError("Expected 140 dry carry runtime frames")
    for target, source in targets.items():
        relative = target.relative_to(ROOT).as_posix()
        expected = corrections.get(relative, {}).get("after", base[relative]["sha256"])
        if digest(target) != expected:
            raise ValueError("Current art differs from locked baseline: " + relative)
        if not source.exists():
            raise FileNotFoundError(source)
    records = []
    for target, source in sorted(targets.items()):
        if target in turns:
            continue
        saved = CHAIN / "installation-backup" / target.relative_to(ROOT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        if saved.exists():
            raise ValueError("Backup already exists: " + str(saved))
        shutil.copy2(target, saved)
        records.append({"target": target.relative_to(ROOT).as_posix(),
                        "beforeSha256": digest(target), "selectedSha256": digest(source)})
        shutil.copy2(source, target)
    records.extend(install_turns(backup=True))
    colour_lock = {
        entry["target"]: {"before": entry["beforeSha256"], "after": entry["selectedSha256"],
                          "reason": "selected Marsh dry carry identity and connected motion"}
        for entry in records
    }
    (CHAIN / "colour-lock.json").write_text(json.dumps(colour_lock, indent=2) + "\n")
    result = {"status": "installed_source", "frameCount": len(records), "frames": records,
              "preservedTimingAndManifests": True}
    (CHAIN / "installation.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print("Installed", install_full()["frameCount"], "dry carry frames")
