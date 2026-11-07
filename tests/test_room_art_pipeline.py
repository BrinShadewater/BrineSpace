import importlib.util
import pathlib
import unittest
from PIL import Image, ImageDraw

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'tools' / 'room_art_pipeline.py'


class RoomArtPipelineTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('room_art_pipeline', SCRIPT)
        self.pipeline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.pipeline)

    def test_removes_only_edge_connected_light_background(self):
        source = Image.new('RGBA', (20, 20), (240, 240, 240, 255))
        draw = ImageDraw.Draw(source)
        draw.rectangle((4, 4, 15, 15), fill=(40, 50, 60, 255))
        draw.rectangle((8, 8, 11, 11), fill=(250, 250, 250, 255))
        cleaned = self.pipeline.clear_exterior(source)
        self.assertEqual(cleaned.getpixel((0, 0))[3], 0)
        self.assertEqual(cleaned.getpixel((9, 9)), (250, 250, 250, 255))
        self.assertEqual(source.getpixel((0, 0))[3], 255)

    def test_normalization_preserves_aspect_and_transparency(self):
        source = Image.new('RGBA', (40, 40))
        ImageDraw.Draw(source).rectangle((10, 5, 29, 34), fill=(50, 60, 70, 255))
        normalized = self.pipeline.normalize(source, size=64, margin=8)
        self.assertEqual(normalized.size, (64, 64))
        self.assertEqual(normalized.getbbox(), (16, 8, 48, 56))

    def test_empty_art_is_rejected(self):
        with self.assertRaises(ValueError):
            self.pipeline.normalize(Image.new('RGBA', (20, 20)))

    def test_explicit_gap_preserves_unselected_enclosed_light(self):
        source = Image.new('RGBA', (24, 24), (240, 240, 240, 255))
        draw = ImageDraw.Draw(source)
        draw.rectangle((2, 2, 21, 21), fill=(40, 50, 60, 255))
        draw.rectangle((5, 5, 8, 8), fill=(250, 250, 250, 255))
        draw.rectangle((14, 14, 17, 17), fill=(250, 250, 250, 255))
        cleaned = self.pipeline.clear_exterior(source, [(6, 6)])
        self.assertEqual(cleaned.getpixel((6, 6))[3], 0)
        self.assertEqual(cleaned.getpixel((15, 15)), source.getpixel((15, 15)))
        self.assertEqual(cleaned.getpixel((4, 4)), source.getpixel((4, 4)))
        with self.assertRaises(ValueError):
            self.pipeline.clear_exterior(source, [(4, 4)])
        with self.assertRaises(ValueError):
            self.pipeline.clear_exterior(source, [(24, 0)])


if __name__ == '__main__':
    unittest.main()
