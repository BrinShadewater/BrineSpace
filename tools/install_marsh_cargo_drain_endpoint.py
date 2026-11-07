"""Join the retained cargo drain to Marsh's selected dry carry frame."""
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "character/marsh-carry-chain-v1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(backup=False):
    baseline = json.loads((ROOT / "character/palette-standard-v1/mapping.json").read_text())["files"]
    correction = json.loads((ROOT / "character/veld-consistency-v1/mapping.json").read_text())
    records = {}
    for direction in ("south", "north", "east", "west"):
        target = ROOT / f"character/marsh-v2/supplemental/cargo-drain-{direction}/cargo-drain-{direction}-005.png"
        carry = ROOT / f"character/marsh-v2/frames/bare/carry-{direction}/000.png"
        relative = target.relative_to(ROOT).as_posix()
        prior = sha(target)
        expected = correction.get(relative, {}).get("after", baseline[relative]["sha256"])
        if backup and prior != expected:
            raise ValueError("Cargo drain endpoint differs from locked baseline: " + relative)
        with Image.open(carry) as source:
            frame = Image.new("RGBA", (224, 208))
            frame.alpha_composite(source.convert("RGBA"), (20, 0))
        if backup:
            saved = BASE / "installation-backup" / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            if saved.exists():
                raise ValueError("Backup already exists: " + str(saved))
            shutil.copy2(target, saved)
        frame.save(target)
        records[relative] = {"before": prior, "after": sha(target),
                             "reason": "exact selected dry carry endpoint after cargo drainage"}
    if backup:
        (BASE / "cargo-drain-endpoint-colour-lock.json").write_text(json.dumps(records, indent=2) + "\n")
    return records


if __name__ == "__main__":
    print("Installed", len(install(backup=True)), "cargo drain endpoints")
