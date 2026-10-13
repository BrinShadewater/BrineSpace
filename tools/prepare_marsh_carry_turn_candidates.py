"""Preview all dry carry turns with endpoints matching the new carry loops.

Interior poses remain the currently installed authored turns; this is an
endpoint-join study, not a claim that their identity is fully revised.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"
NEW_CARRY = ROOT / "character/marsh-carry-match-v1/frames"
OUT = ROOT / "character/marsh-carry-chain-v1/turns"


def build() -> dict:
    catalog = json.loads((RUNTIME / "catalog.json").read_text())
    records = []
    for relative in catalog["body"]:
        if not relative.startswith("supplemental/carry-turn-"):
            continue
        manifest = RUNTIME / relative
        data = json.loads(manifest.read_text())
        for state in data["states"]:
            key = state["id"]
            parts = key.split("-")
            if len(parts) != 4 or parts[:2] != ["carry", "turn"]:
                raise ValueError(f"Unexpected turn key {key}")
            origin, destination = parts[2:]
            folder = OUT / key
            folder.mkdir(parents=True, exist_ok=True)
            files = []
            for i, item in enumerate(state["frameFiles"]):
                if i == 0:
                    source = NEW_CARRY / origin / "000.png"
                elif i == len(state["frameFiles"]) - 1:
                    source = NEW_CARRY / destination / "000.png"
                else:
                    source = (manifest.parent / item).resolve()
                target = folder / f"{i:03}.png"
                shutil.copyfile(source, target)
                files.append(target)
            contact = Image.new("RGB", (184 * len(files), 210), (33, 39, 44))
            draw = ImageDraw.Draw(contact)
            for i, path in enumerate(files):
                frame = Image.open(path).convert("RGBA")
                contact.paste(frame, (184 * i, 0), frame)
                draw.text((184 * i + 4, 188), str(i), fill="white")
            contact.save(folder / "contact.png")
            records.append({"id": key, "frames": len(files), "origin": origin,
                            "destination": destination,
                            "interior": "current selected turn art",
                            "endpoints": "new carry frame zero",
                            "status": "candidate_not_installed"})
    if len(records) != 12:
        raise ValueError(f"Expected twelve directed carry turns, got {len(records)}")
    result = {"states": records, "status": "endpoint_candidate_not_installed"}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(len(build()["states"]), "directed turn candidates")
