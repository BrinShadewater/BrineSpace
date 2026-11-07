"""Retained cargo-drain poses join the selected swim and dry carry clips."""
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"


def pixels(path):
    return Image.open(path).convert("RGBA").tobytes()


class CargoDrain(unittest.TestCase):
    def test_registered_endpoints_and_usable_frames(self):
        for direction in ("east", "west", "north", "south"):
            with self.subTest(direction=direction):
                folder = RUNTIME / "supplemental" / f"cargo-drain-{direction}"
                state = json.loads((folder / "manifest.json").read_text())["states"][0]
                frames = [folder / name for name in state["frameFiles"]]
                self.assertEqual(len(frames), 6)
                selected = ROOT / "character/marsh-cargo-drain-match-v1/frames" / f"cargo-drain-{direction}"
                for path in frames:
                    with Image.open(path) as frame:
                        self.assertEqual(frame.size, (224, 208))
                        self.assertLessEqual(set(frame.getchannel("A").tobytes()), {0, 255})
                        left, top, right, bottom = frame.getbbox()
                        self.assertTrue(0 < left and 0 < top and right < 224 and bottom < 208)
                for phase in range(1, 5):
                    self.assertEqual(pixels(frames[phase]), pixels(selected / f"{phase:03}.png"))
                swim = RUNTIME / f"supplemental/loaded-swim-{direction}/swim-carry-{direction}-000.png"
                self.assertEqual(pixels(frames[0]), pixels(swim))
                dry = Image.new("RGBA", (224, 208))
                with Image.open(RUNTIME / f"frames/bare/carry-{direction}/000.png") as carry:
                    dry.alpha_composite(carry.convert("RGBA"), (20, 0))
                self.assertEqual(pixels(frames[-1]), dry.tobytes())


if __name__ == "__main__":
    unittest.main()
