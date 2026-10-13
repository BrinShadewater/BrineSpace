"""Publish the focused native run and airlock captures beside the art review."""
from pathlib import Path
from shutil import copy2

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "output/marsh-animation-audit"
OUT = ROOT / "character/marsh-run-carry-review-v1"

for direction in ("south", "north", "east", "west"):
    folder = CAPTURES / "run-native" / direction
    paths = sorted(folder.glob("frame-[0-9][0-9][0-9].png"))
    if len(paths) != 60:
        raise ValueError(f"Expected 60 native run captures for {direction}, got {len(paths)}")
    frames = [Image.open(path).convert("RGB").crop((325, 100, 650, 340)) for path in paths]
    frames[0].save(OUT / f"native-run-{direction}.gif", save_all=True,
                   append_images=frames[1:], duration=40, loop=0, optimize=True)

copy2(CAPTURES / "native-cargo-drain-contact.png", OUT / "native-cargo-drain-contact.png")
pickup = CAPTURES / "native-swim-pickup-contact.png"
if pickup.exists():
    copy2(pickup, OUT / "native-swim-pickup-contact.png")
print("Published four native run loops and available native cargo contacts")
