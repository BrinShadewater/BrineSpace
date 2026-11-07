"""Selected underwater pickup joins frozen salvage and loaded swim exactly."""
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"
SELECTED = ROOT / "character/marsh-swim-pickup-match-v1/frames"


def pixels(path):
    return Image.open(path).convert("RGBA").tobytes()


class LoadedSwim(unittest.TestCase):
    def test_selected_pickup_and_joins(self):
        for direction in ("east", "west", "north", "south"):
            with self.subTest(direction=direction):
                folder = RUNTIME / "supplemental" / f"loaded-swim-{direction}"
                manifest = json.loads((folder / "manifest.json").read_text())
                states = {state["id"]: state for state in manifest["states"]}
                pickup = [folder / name for name in states[f"swim-pickup-{direction}"]["frameFiles"]]
                carry = [folder / name for name in states[f"swim-carry-{direction}"]["frameFiles"]]
                self.assertEqual(len(pickup), 6)
                self.assertEqual(len(carry), 6)
                for phase, path in enumerate(pickup):
                    self.assertEqual(pixels(path), pixels(SELECTED / f"swim-pickup-{direction}" / f"{phase:03}.png"))
                    with Image.open(path) as frame:
                        self.assertEqual(frame.size, (224, 208))
                        self.assertLessEqual(set(frame.getchannel("A").tobytes()), {0, 255})
                salvage = Image.new("RGBA", (224, 208))
                with Image.open(RUNTIME / f"frames/bare/salvage-{direction}/000.png") as frame:
                    salvage.alpha_composite(frame.convert("RGBA"), (20, 0))
                self.assertEqual(pixels(pickup[0]), salvage.tobytes())
                self.assertEqual(pixels(pickup[-1]), pixels(carry[0]))
                self.assertEqual(pixels(carry[4]), pixels(carry[2]))
                self.assertEqual(pixels(carry[5]), pixels(carry[1]))


if __name__ == "__main__":
    unittest.main()
