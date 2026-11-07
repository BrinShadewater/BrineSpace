"""Install selected Marsh underwater pickup poses with exact loaded-swim exits."""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-swim-pickup-match-v1"
RUNTIME = ROOT / "character/marsh-v2/supplemental"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(backup=False):
    targets = {}
    for direction in ("south", "north", "east", "west"):
        for phase in range(5):
            target = RUNTIME / f"loaded-swim-{direction}/swim-pickup-{direction}-{phase:03}.png"
            source = BASE / "frames" / f"swim-pickup-{direction}" / f"{phase:03}.png"
            targets[target] = source
        exit_source = BASE / "frames" / f"swim-pickup-{direction}" / "005.png"
        exit_runtime = RUNTIME / f"loaded-swim-{direction}/swim-carry-{direction}-000.png"
        if sha(exit_source) != sha(exit_runtime):
            raise ValueError("Selected pickup endpoint differs from loaded swim: " + direction)
        start_source = BASE / "frames" / f"swim-pickup-{direction}" / "000.png"
        salvage = Image.new("RGBA", (224, 208))
        with Image.open(ROOT / f"character/marsh-salvage-match-v1/frames/salvage-{direction}/000.png") as frame:
            salvage.alpha_composite(frame.convert("RGBA"), (20, 0))
        with Image.open(start_source) as frame:
            if frame.convert("RGBA").tobytes() != salvage.tobytes():
                raise ValueError("Selected pickup start differs from selected salvage: " + direction)
    if backup:
        baseline = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
        corrections = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
        for target, source in targets.items():
            relative = target.relative_to(ROOT).as_posix()
            expected = corrections.get(relative, {}).get("after", baseline[relative]["sha256"])
            if sha(target) != expected:
                raise ValueError("Current pickup frame differs from locked baseline: " + relative)
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
                             "reason": "selected Marsh underwater cargo pickup identity"}
    for direction in ("south", "north", "east", "west"):
        path = RUNTIME / f"loaded-swim-{direction}/provenance.json"
        if backup:
            saved = BASE / "installation-backup" / path.relative_to(ROOT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
        data = json.loads(path.read_text())
        data["selectedPickupOverride"] = {
            "source": f"character/marsh-swim-pickup-match-v1/frames/swim-pickup-{direction}/",
            "frames": [0, 1, 2, 3, 4],
            "start": "Exact active salvage frame zero",
            "exit": "Exact active swim-carry frame zero",
        }
        path.write_text(json.dumps(data, indent=2) + "\n")
    if backup:
        (BASE / "colour-lock.json").write_text(json.dumps(records, indent=2) + "\n")
        (BASE / "installation.json").write_text(json.dumps({"status": "installed_source",
            "frameCount": len(records), "frames": records,
            "preservedTimingAndManifest": True}, indent=2) + "\n")
    return records


if __name__ == "__main__":
    print("Installed", len(install(backup=True)), "underwater pickup frames")
