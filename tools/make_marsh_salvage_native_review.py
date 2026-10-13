"""Collect three actual expedition salvage facings for the Marsh art review."""
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CAPTURES = ROOT / "output/marsh-animation-audit"
OUT = ROOT / "character/marsh-run-carry-review-v1/native-salvage-contact.png"
SAMPLES = (0.0, 0.23, 0.50, 0.77)


def main():
    board = Image.new("RGB", (300 * len(SAMPLES), 320 * 3), "#1b2429")
    draw = ImageDraw.Draw(board)
    for row, (rotation, direction) in enumerate(((0, "east"), (1, "south"), (2, "west"))):
        folder = CAPTURES / f"native-salvage-q{rotation}"
        report = json.loads((folder / "report.json").read_text())
        if report["failures"]:
            raise ValueError(f"Native salvage rotation {rotation} has failures")
        captures = [entry for entry in report["journeys"][0]["captures"]
                    if entry["phase"] == "salvage" and entry["direction"] == direction]
        if len(captures) < 12:
            raise ValueError(f"Too few native salvage captures for {direction}: {len(captures)}")
        for col, sample in enumerate(SAMPLES):
            entry = min(captures, key=lambda candidate: abs(candidate["elapsed"] - sample))
            image = Image.open(folder / entry["file"]).convert("RGB")
            crop = image.crop((485, 245, 665, 425)).resize((300, 300), Image.Resampling.NEAREST)
            x, y = col * 300, row * 320
            board.paste(crop, (x, y))
            draw.text((x + 5, y + 302), f"{direction} {entry['elapsed']:.2f}s", fill="white")
    board.save(OUT)
    print("Published native salvage east/south/west contact")


if __name__ == "__main__":
    main()
