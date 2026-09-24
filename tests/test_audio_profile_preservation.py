"""The original-batch rebuild must preserve newer music and pairing metadata."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from polish_suno_audio import update_gain_profile


class ProfilePreservation(unittest.TestCase):
    def test_partial_rebuild_preserves_new_batch_and_brightness(self):
        original = (ROOT / 'scripts/station_audio_mix.gd').read_text()
        changed = update_gain_profile(original, {'res://assets/audio/suno-v1/moonlit_canyon_01.ogg': -2.0})
        self.assertIn('"res://assets/audio/suno-v1/moonlit_canyon_01.ogg": -2.0,', changed)
        for line in original.splitlines():
            if 'res://assets/audio/tracks-v1/' in line:
                self.assertIn(line, changed)
        self.assertEqual(original.split('const BRIGHTNESS_HZ', 1)[1], changed.split('const BRIGHTNESS_HZ', 1)[1])

    def test_unknown_profile_fails_instead_of_replacing(self):
        with self.assertRaises(ValueError):
            update_gain_profile('extends RefCounted\n', {})


if __name__ == '__main__':
    unittest.main()
