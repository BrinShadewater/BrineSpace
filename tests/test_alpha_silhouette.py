import hashlib
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

from tools.register_alpha_silhouette import register


class AlphaRegistrationTests(unittest.TestCase):
    def test_holes_and_faint_glow_are_excluded_without_raster_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.png"
            image = Image.new("RGBA", (20, 20), (80, 80, 80, 48))
            draw = ImageDraw.Draw(image)
            draw.rectangle((3, 3, 16, 16), fill=(200, 200, 200, 255))
            draw.rectangle((6, 6, 8, 10), fill=(0, 0, 0, 0))
            draw.rectangle((12, 8, 13, 12), fill=(0, 0, 0, 0))
            image.save(path)
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            result = register(path, min_area=0, simplify=0)
            shapes = [Polygon(piece) for piece in result["pieces"]]
            solid = unary_union(shapes)
            self.assertTrue(all(shape.is_valid and not shape.interiors for shape in shapes))
            self.assertAlmostEqual(solid.area, 14 * 14 - 3 * 5 - 2 * 5)
            self.assertFalse(solid.covers(Point(7, 8)))
            self.assertFalse(solid.covers(Point(12.5, 10)))
            self.assertFalse(solid.covers(Point(1, 1)))
            self.assertTrue(solid.covers(Point(4, 4)))
            self.assertEqual(before, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_opaque_rgb_is_not_misrepresented_as_alpha(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "opaque.png"
            Image.new("RGB", (4, 4), "white").save(path)
            with self.assertRaisesRegex(ValueError, "no alpha channel"):
                register(path)

    def test_fully_opaque_rgba_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "opaque-rgba.png"
            Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(path)
            with self.assertRaisesRegex(ValueError, "No exterior alpha"):
                register(path)


if __name__ == "__main__":
    unittest.main()
