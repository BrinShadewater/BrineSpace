"""Install reviewed Marsh cargo-drain middle poses without changing clip timing."""
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-cargo-drain-match-v1"
RUNTIME = ROOT / "character/marsh-v2"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(backup=False):
    targets = {}
    for direction in ("south", "north", "east", "west"):
        for phase in range(1, 5):
            name = f"cargo-drain-{direction}-{phase:03}.png"
            target = RUNTIME / "supplemental" / f"cargo-drain-{direction}" / name
            source = BASE / "frames" / f"cargo-drain-{direction}" / f"{phase:03}.png"
            targets[target] = source
    if backup:
        baseline = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
        corrections = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
        for target, source in targets.items():
            relative = target.relative_to(ROOT).as_posix()
            expected = corrections.get(relative, {}).get("after", baseline[relative]["sha256"])
            if sha(target) != expected:
                raise ValueError("Current drain frame differs from locked baseline: " + relative)
            if not source.exists():
                raise FileNotFoundError(source)
            saved = BASE / "installation-backup" / relative
            if saved.exists():
                raise ValueError("Backup already exists: " + str(saved))
    records = {}
    for target, source in targets.items():
        relative = target.relative_to(ROOT).as_posix()
        previous = sha(target)
        if backup:
            saved = BASE / "installation-backup" / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
        shutil.copy2(source, target)
        records[relative] = {"before": previous, "after": sha(target),
                             "reason": "selected Marsh water-to-dry cargo rise"}
    for direction in ("south", "north", "east", "west"):
        path = RUNTIME / "supplemental" / f"cargo-drain-{direction}" / "provenance.json"
        if backup:
            saved = BASE / "installation-backup" / path.relative_to(ROOT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
        data = json.loads(path.read_text())
        data["selectedMiddleOverride"] = {
            "source": f"character/marsh-cargo-drain-match-v1/frames/cargo-drain-{direction}/",
            "frames": [1, 2, 3, 4],
            "endpoints": "Exact current loaded swim and selected dry carry frame zero",
        }
        path.write_text(json.dumps(data, indent=2) + "\n")
    if backup:
        (BASE / "colour-lock.json").write_text(json.dumps(records, indent=2) + "\n")
        (BASE / "installation.json").write_text(json.dumps({"status": "installed_source",
            "frameCount": len(records), "frames": records,
            "preservedTimingAndManifest": True}, indent=2) + "\n")
    return records


if __name__ == "__main__":
    print("Installed", len(install(backup=True)), "cargo-drain middle frames")
