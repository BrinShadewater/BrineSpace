import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('mac_export', Path(__file__).resolve().parents[1] / 'tools/export_macos.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TemplateSelection(unittest.TestCase):
    def test_selected_custom_template_not_hardcoded_default(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'export_presets.cfg').write_text('[preset.8]\nname="macOS Game"\nplatform="macOS"\n[preset.8.options]\ncustom_template/release="res://alternate/template.zip"\n')
            self.assertEqual(m.selected_template(root), (root / 'alternate/template.zip').resolve())

    def test_missing_explicit_template_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'export_presets.cfg').write_text('[preset.8]\nname="macOS Game"\nplatform="macOS"\n[preset.8.options]\n')
            with self.assertRaises(RuntimeError):
                m.selected_template(root)


if __name__ == '__main__':
    unittest.main()
