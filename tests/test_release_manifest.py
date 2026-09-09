import importlib.util
from pathlib import Path
import tempfile, unittest
spec=importlib.util.spec_from_file_location('manifest',Path(__file__).resolve().parents[1]/'tools/build_release_manifest.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RuntimeAssets(unittest.TestCase):
    def test_manifest_frames_and_dynamic_imported_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
                'scenes/title_screen.tscn':'path="res://scripts/game.gd"',
                'scripts/game.gd':'const M="res://character/selected/manifest.json"\nconst BUTTONS="res://ui/buttons/"\nconst ROOT="res://"',
                'character/selected/manifest.json':'{"frameFiles":["frames/one.png"]}',
                'character/selected/frames/one.png':'PNG',
                'character/rejected/unused.png':'UNUSED',
                'ui/buttons/on.tres':'path="res://ui/on.png"',
                'ui/on.png':'PNG',
                'output/debug.png':'DEBUG',
            }
            for name,data in files.items():
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
            selected,_=m.collect(root)
            self.assertIn('character/selected/frames/one.png',selected)
            self.assertIn('ui/buttons/on.tres',selected)
            self.assertIn('ui/on.png',selected)
            self.assertNotIn('character/rejected/unused.png',selected)
            self.assertNotIn('output/debug.png',selected)
    def test_frozen_script_bindings_override_concurrent_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'root'; frozen=Path(directory)/'frozen'
            for base in [root,frozen]:(base/'scenes').mkdir(parents=True)
            (root/'project.godot').write_text('run/main_scene="res://scenes/title_screen.tscn"')
            (root/'scenes/title_screen.tscn').write_text('path="res://unfinished.png"')
            (frozen/'scenes/title_screen.tscn').write_text('path="res://accepted.png"')
            (root/'accepted.png').write_bytes(b'png')
            selected,_=m.collect(root,frozen)
            self.assertIn('accepted.png',selected)
if __name__=='__main__':unittest.main()
