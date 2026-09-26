import importlib.util
from pathlib import Path
import tempfile, unittest
spec=importlib.util.spec_from_file_location('manifest',Path(__file__).resolve().parents[1]/'tools/build_release_manifest.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RuntimeAssets(unittest.TestCase):
    def test_branforth_locker_authoring_exclusion_is_narrow(self):
        base='character/chief-engineer-branforth-v2'
        authoring=base+'/sources/locker-identity-2026-09-22'
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
                'scenes/title_screen.tscn':'path="res://scripts/player.gd"',
                'scripts/player.gd':f'const ROOT="res://{base}/"\nconst NEEDED="res://{authoring}/needed.png"\nconst TOOLS="res://{authoring}/tool-%s.png"',
                base+'/frames/live.png':'PNG',
                base+'/sources/other-live.png':'PNG',
                authoring+'/needed.png':'PNG',
                authoring+'/tool-east.png':'PNG',
                authoring+'/generated-source.png':'UNUSED',
                authoring+'/registration.json':'{"source":"res://unneeded.png"}',
                'unneeded.png':'UNUSED',
            }
            for name,data in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(data)
            selected,_=m.collect(root)
            for name in ['frames/live.png','sources/other-live.png']:
                self.assertIn(base+'/'+name,selected)
            for name in ['needed.png','tool-east.png']:
                self.assertIn(authoring+'/'+name,selected)
            for name in ['generated-source.png','registration.json']:
                self.assertNotIn(authoring+'/'+name,selected)
            self.assertNotIn('unneeded.png',selected)

    def test_bill_authoring_scan_omits_sources_but_explicit_dependencies_win(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
                'scenes/title_screen.tscn':'path="res://scripts/player.gd"',
                'scripts/player.gd':'const ROOT="res://character/major-bill-v3/"\nconst PACK="res://character/major-bill-v3/packs/manifest.json"\nconst TOOL="res://character/major-bill-v3/sources/tool-%s.png"',
                'character/major-bill-v3/packs/manifest.json':json.dumps({'frameFiles':['../frames/live.png','../sources/needed.png','../sources/runtime.json']}),
                'character/major-bill-v3/frames/live.png':'PNG',
                'character/major-bill-v3/sources/needed.png':'PNG',
                'character/major-bill-v3/sources/tool-east.png':'PNG',
                'character/major-bill-v3/sources/runtime.json':json.dumps({'frame':'nested/also-needed.png'}),
                'character/major-bill-v3/sources/nested/also-needed.png':'PNG',
                'character/major-bill-v3/sources/rejected.png':'UNUSED',
                'character/major-bill-v3/sources/authoring.json':json.dumps({'reference':'res://unneeded.png'}),
                'unneeded.png':'UNUSED',
            }
            for name,data in files.items():
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
            selected,_=m.collect(root)
            for name in ['frames/live.png','sources/needed.png','sources/runtime.json','sources/nested/also-needed.png','sources/tool-east.png']:
                self.assertIn('character/major-bill-v3/'+name,selected)
            self.assertNotIn('character/major-bill-v3/sources/rejected.png',selected)
            self.assertNotIn('character/major-bill-v3/sources/authoring.json',selected)
            self.assertNotIn('unneeded.png',selected)

    def test_json_labels_cannot_hide_following_asset_paths(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
                'scenes/title_screen.tscn':'path="res://props.json"',
                'props.json':json.dumps([
                    {'title':"Worker's rack",'source':'res://rack.png'},
                    {'title':'Label with "quotes"','source':'res://truck.png'},
                ]),
                'rack.png':'PNG','truck.png':'PNG',
            }
            for name,data in files.items():
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
            selected,_=m.collect(root)
            self.assertIn('rack.png',selected)
            self.assertIn('truck.png',selected)

    def test_named_preset_preserves_other_platforms_and_options(self):
        windows='[preset.3]\nname="Windows Game"\nexport_filter="all_resources"\ninclude_filter="*.png"\nexclude_filter=""\n\n[preset.3.options]\ncustom_template/release="windows.exe"\n'
        mac='[preset.7]\nname="macOS Game"\nexport_filter="all_resources"\nexport_files=PackedStringArray("old")\ninclude_filter="*.png"\nexclude_filter=""\n\n[preset.7.options]\napplication/bundle_identifier="com.shadewater.brinespace"\n'
        result=m.update_preset(windows+mac,['res://scenes/title_screen.tscn'],'macOS Game')
        self.assertTrue(result.startswith(windows))
        self.assertEqual(result.split('[preset.7.options]')[1],mac.split('[preset.7.options]')[1])
        self.assertIn('export_files=PackedStringArray("res://scenes/title_screen.tscn")',result)
        self.assertNotIn('PackedStringArray("old")',result)
        self.assertIn('export_filter="selected_resources"',result)

    def test_missing_or_duplicate_preset_is_rejected(self):
        with self.assertRaises(ValueError): m.update_preset('[preset.0]\nname="Other"\n',[])
        duplicate='[preset.0]\nname="Windows Game"\n[preset.2]\nname="Windows Game"\n'
        with self.assertRaises(ValueError): m.update_preset(duplicate,[])

    def test_formatted_legacy_bindings_and_explicit_machines(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"',
                'scenes/title_screen.tscn':'path="res://scripts/room.gd"',
                'scripts/room.gd':'var path="res://legacy/retired/pack/pump-%s.png" % facing\nconst MACHINE="res://legacy/default/machine.png"',
                'legacy/retired/pack/pump-left.png':'PNG',
                'legacy/retired/pack/pump-right.png':'PNG',
                'legacy/default/machine.png':'PNG',
                'legacy/retired/pack/rejected.png':'UNUSED',
            }
            for name,data in files.items():
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
            selected,_=m.collect(root)
            for name in ['legacy/retired/pack/pump-left.png','legacy/retired/pack/pump-right.png','legacy/default/machine.png']:
                self.assertIn(name,selected)
            self.assertNotIn('legacy/retired/pack/rejected.png',selected)

    def test_manifest_frames_and_dynamic_imported_controls(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            files={
                'project.godot':'run/main_scene="res://scenes/title_screen.tscn"\n[autoload]\nReport="*res://scripts/report.gd"',
                'scripts/report.gd':'const ICON="res://ui/report.png"',
                'ui/report.png':'PNG',
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
            self.assertIn('scripts/report.gd',selected)
            self.assertIn('ui/report.png',selected)
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
