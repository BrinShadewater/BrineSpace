"""Selected Marsh dry carry turns reproduce the reviewed sources and join exactly."""
import json
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "character/marsh-v2"
SELECTED = ROOT / "character/marsh-carry-chain-v1/turns-matched"


def pixels(path):
    return Image.open(path).convert("RGBA").tobytes()


class CarryTurns(unittest.TestCase):
    def test_reproduction_and_joins(self):
        catalog = json.loads((RUNTIME / "catalog.json").read_text())
        states = {}
        for relative in catalog["body"]:
            if not relative.startswith("supplemental/carry-turn-"):
                continue
            manifest = RUNTIME / relative
            for state in json.loads(manifest.read_text())["states"]:
                name = state["id"]
                runtime = [manifest.parent / f for f in state["frameFiles"]]
                selected = sorted((SELECTED / name).glob("[0-9][0-9][0-9].png"))
                self.assertEqual(len(runtime), len(selected), name)
                for actual, source in zip(runtime, selected):
                    self.assertEqual(pixels(actual), pixels(source), name)
                    with Image.open(actual) as frame:
                        self.assertLessEqual(set(frame.getchannel("A").tobytes()), {0, 255})
                origin, destination = name.removeprefix("carry-turn-").split("-")
                self.assertEqual(pixels(runtime[0]), pixels(RUNTIME / f"frames/bare/carry-{origin}/000.png"), name)
                self.assertEqual(pixels(runtime[-1]), pixels(RUNTIME / f"frames/bare/carry-{destination}/000.png"), name)
                states[name] = runtime
        self.assertEqual(len(states), 12)
        for name, row in states.items():
            origin, destination = name.removeprefix("carry-turn-").split("-")
            reverse = states[f"carry-turn-{destination}-{origin}"]
            self.assertEqual([pixels(f) for f in row], [pixels(f) for f in reversed(reverse)], name)


if __name__ == "__main__":
    unittest.main()
