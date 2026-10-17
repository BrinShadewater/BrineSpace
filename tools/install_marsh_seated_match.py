"""Install selected Marsh seated action frames."""
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-seated-match-v1"
DIRECTIONS = ("south", "north", "east", "west")
COUNTS = {"sit-down": 4, "sit-idle": 2, "read-seated": 3, "sit-rise": 4}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected(action, direction, phase):
    return BASE / "frames" / f"{action}-{direction}" / f"{phase:03}.png"


def install(backup=False):
    targets = {}
    for direction in DIRECTIONS:
        for action, count in COUNTS.items():
            for phase in range(count):
                target = ROOT / f"character/marsh-v2/frames/bare/{action}-{direction}/{phase:03}.png"
                targets[target] = selected(action, direction, phase)
    if backup:
        baseline = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
        corrections = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
        for target, source in targets.items():
            relative = target.relative_to(ROOT).as_posix()
            expected = corrections.get(relative, {}).get("after", baseline[relative]["sha256"])
            if sha(target) != expected:
                raise ValueError("Current action differs from locked baseline: " + relative)
            if not source.exists():
                raise FileNotFoundError(source)
            if (BASE / "installation-backup" / relative).exists():
                raise ValueError("Backup already exists: " + relative)
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
                             "source": source.relative_to(ROOT).as_posix(),
                             "reason": "selected Marsh seated action identity with fixed anatomical scale"}
    if backup:
        (BASE / "colour-lock.json").write_text(json.dumps(records, indent=2) + "\n")
        (BASE / "installation.json").write_text(json.dumps({"status": "installed_source",
            "frameCount": len(records), "frames": records, "preservedTimingAndManifest": True,
            "newlyAuthoredInteriorPoses": 28, "selectedChainFrames": 52}, indent=2) + "\n")
    return records


if __name__ == "__main__":
    print("Installed", len(install(backup=True)), "seated action frames")
