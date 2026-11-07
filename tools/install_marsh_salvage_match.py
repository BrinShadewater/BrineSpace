"""Install selected Marsh salvage action and its underwater pickup start."""
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-salvage-match-v1"
DIRECTIONS = ("south", "north", "east", "west")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(backup=False):
    targets = {}
    for direction in DIRECTIONS:
        for phase in range(6):
            relative = f"character/marsh-v2/frames/bare/salvage-{direction}/{phase:03}.png"
            targets[ROOT / relative] = BASE / "frames" / f"salvage-{direction}" / f"{phase:03}.png"
        pickup_target = ROOT / f"character/marsh-v2/supplemental/loaded-swim-{direction}/swim-pickup-{direction}-000.png"
        pickup_source = ROOT / "character/marsh-swim-pickup-match-v1/frames" / f"swim-pickup-{direction}" / "000.png"
        targets[pickup_target] = pickup_source
    if backup:
        baseline = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
        corrections = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
        for target, source in targets.items():
            relative = target.relative_to(ROOT).as_posix()
            expected = corrections.get(relative, {}).get("after", baseline[relative]["sha256"])
            if sha(target) != expected:
                raise ValueError("Current frame differs from locked baseline: " + relative)
            if not source.exists():
                raise FileNotFoundError(source)
            saved = (ROOT / "character/marsh-swim-pickup-match-v1/installation-backup" / relative
                     if "swim-pickup-" in relative else BASE / "installation-backup" / relative)
            if saved.exists():
                if "swim-pickup-" not in relative or sha(saved) != sha(target):
                    raise ValueError("Unexpected existing backup: " + relative)
            elif "swim-pickup-" in relative:
                raise ValueError("Missing preserved pickup start backup: " + relative)
    records = {}
    for target, source in targets.items():
        relative = target.relative_to(ROOT).as_posix()
        previous = sha(target)
        if backup and "swim-pickup-" not in relative:
            saved = BASE / "installation-backup" / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
        shutil.copy2(source, target)
        records[relative] = {"before": previous, "after": sha(target),
                             "reason": "selected Marsh salvage and underwater pickup start identity"}
    if backup:
        (BASE / "colour-lock.json").write_text(json.dumps(records, indent=2) + "\n")
        (BASE / "installation.json").write_text(json.dumps({"status": "installed_source",
            "frameCount": len(records), "frames": records,
            "preservedTimingAndManifest": True}, indent=2) + "\n")
    return records


if __name__ == "__main__":
    print("Installed", len(install(backup=True)), "salvage and pickup-start frames")
