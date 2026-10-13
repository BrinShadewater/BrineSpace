"""Selected Marsh salvage action joins active idle and underwater pickup."""
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BARE = ROOT / "character/marsh-v2/frames/bare"
SELECTED = ROOT / "character/marsh-salvage-match-v1/frames"
LOADED = ROOT / "character/marsh-v2/supplemental"


def pixels(path):
    with Image.open(path) as image:
        return image.convert("RGBA").tobytes()


class SalvageMatch(unittest.TestCase):
    def test_selected_action_and_pickup_join(self):
        for direction in ("south", "north", "east", "west"):
            with self.subTest(direction=direction):
                idle = BARE / f"idle-{direction}/000.png"
                for phase in range(6):
                    runtime = BARE / f"salvage-{direction}/{phase:03}.png"
                    selected = SELECTED / f"salvage-{direction}/{phase:03}.png"
                    self.assertEqual(pixels(runtime), pixels(selected))
                    with Image.open(runtime) as image:
                        self.assertEqual(image.size, (184, 184))
                        self.assertLessEqual(set(image.getchannel("A").tobytes()), {0, 255})
                self.assertEqual(pixels(idle), pixels(BARE / f"salvage-{direction}/000.png"))
                self.assertEqual(pixels(idle), pixels(BARE / f"salvage-{direction}/005.png"))
                pickup = LOADED / f"loaded-swim-{direction}/swim-pickup-{direction}-000.png"
                with Image.open(pickup) as image:
                    actual = image.convert("RGBA")
                expected = Image.new("RGBA", (224, 208))
                with Image.open(idle) as image:
                    expected.alpha_composite(image.convert("RGBA"), (20, 0))
                self.assertEqual(actual.tobytes(), expected.tobytes())


if __name__ == "__main__":
    unittest.main()
