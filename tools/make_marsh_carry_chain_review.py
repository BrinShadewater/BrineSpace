"""Render the installed Marsh carry transitions for owner review."""
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"
OUT = ROOT / "character/marsh-run-carry-review-v1"


def review(name, paths, durations):
    frames = []
    for path in paths:
        sprite = Image.open(path).convert("RGBA")
        board = Image.new("RGB", (224, 220), "#21272c")
        board.paste(sprite, ((224 - sprite.width) // 2, 12), sprite)
        ImageDraw.Draw(board).text((8, 198), name, fill="#eef2ec")
        frames.append(board)
    frames[0].save(OUT / (name + ".gif"), save_all=True,
                   append_images=frames[1:], duration=durations, loop=0)


for direction in ("south", "north", "east", "west"):
    for action, duration in (("pickup", [180, 180, 180, 600]),
                             ("unload", [180, 180, 180, 600])):
        name = f"{action}-{direction}"
        paths = [RUNTIME / "frames/bare" / name / f"{i:03}.png" for i in range(4)]
        review(name, paths, duration)

for pair in ("east-north", "west-north", "east-south", "west-south",
             "east-west", "north-south"):
    name = "carry-turn-" + pair
    folder = RUNTIME / "supplemental" / name
    paths = sorted(folder.glob(name + "-[0-9][0-9][0-9].png"))
    review(name, paths, [120] * (len(paths) - 1) + [600])
