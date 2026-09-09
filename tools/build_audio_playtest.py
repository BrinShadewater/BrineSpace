"""Freeze the current checkout and build an audio-focused Windows playtest.

Usage: python tools/build_audio_playtest.py OUTPUT_DIRECTORY
Existing output directories are rejected. Uses the installed Godot 4.6.1 template.
The normal title entry is retained; test adapters are confined to the frozen copy.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GODOT = 'C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe'
FIXTURES = {'audio':'test_suno_audio','space':'test_audio_space','title':'test_title_screen','systems':'test_station_systems','quit':'test_audio_quit'}

def digest(path):
    with path.open('rb') as handle: return hashlib.file_digest(handle,'sha256').hexdigest()

def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True,exist_ok=False)
    src = out/'source'
    src.mkdir()
    paths = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
    excluded = {'output','outputs','asset_backups','skills','.git','.godot','.codex','docs'}
    records = []
    for relative in sorted(set(paths)):
        if not relative or Path(relative).parts[0] in excluded: continue
        original = ROOT/relative
        if not original.is_file(): continue
        with original.open('rb') as handle:
            if handle.read(48).startswith(b'version https://git-lfs.github.com/spec/'):
                raise RuntimeError('Unmaterialized LFS file: '+relative)
        target = src/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(original,target)
        records.append({'path':relative,'sha256':digest(target),'bytes':target.stat().st_size})
    (out/'source-manifest.json').write_text(json.dumps(records,indent=2))
    print(f'Frozen {len(records)} files',flush=True)
    # Adapt only SceneTree access and evidence destinations; keep assertions intact.
    adapter = '''extends Node
var root: Window:
 get: return get_tree().root
var current_scene: Node:
 get: return get_tree().current_scene
 set(value): get_tree().current_scene=value
var process_frame: Signal:
 get: return get_tree().process_frame
func create_timer(seconds: float) -> SceneTreeTimer: return get_tree().create_timer(seconds)
func quit(code: int=0) -> void: get_tree().quit(code)
'''
    for label,name in FIXTURES.items():
        text = (src/f'tests/{name}.gd').read_text(encoding='utf-8')
        text = text.replace('extends SceneTree',adapter,1).replace('func _init()','func _ready()',1).replace('res://output/','user://audio-evidence/')
        text = '\n'.join('\t'+line.lstrip(' ') if line.startswith(' ') else line for line in text.split('\n'))
        (src/f'tests/audio_package_{label}.gd').write_text(text,encoding='utf-8')
    bridge = '''extends Node
func _ready() -> void:
 for arg in OS.get_cmdline_user_args():
  if arg.begins_with("--audio-check="):
   var label := arg.trim_prefix("--audio-check=")
   if label in ["audio","space","title","systems","quit"]: call_deferred("run_check",label)
func run_check(label: String) -> void:
 if get_tree().current_scene != null:
  get_tree().current_scene.queue_free()
  get_tree().current_scene = null
 await get_tree().process_frame
 var music = get_tree().root.get_node_or_null("StationMusic")
 if music != null: music.queue_free()
 await get_tree().create_timer(0.2).timeout
 DirAccess.make_dir_recursive_absolute("user://audio-evidence")
 get_tree().root.add_child(load("res://tests/audio_package_"+label+".gd").new())
'''
    (src/'tests/audio_package_bridge.gd').write_text(bridge,encoding='utf-8')
    project = src/'project.godot'
    config = project.read_text(encoding='utf-8')
    entry = 'AudioPackageCheck="*res://tests/audio_package_bridge.gd"'
    config = config.replace('[autoload]','[autoload]\n'+entry,1) if '[autoload]' in config else config+'\n[autoload]\n'+entry+'\n'
    project.write_text(config,encoding='utf-8')
    roots = ['res://'+r['path'] for r in records if Path(r['path']).suffix in ['.gd','.tscn','.tres'] and Path(r['path']).parts[0] not in ['tests','tools','addons']]
    roots += [f'res://tests/audio_package_{label}.gd' for label in FIXTURES]+['res://tests/audio_package_bridge.gd']
    template = (ROOT/'output/production-ten/export-tools/windows_debug_x86_64.exe').as_posix()
    preset = '[preset.0]\nname="Windows Audio Playtest"\nplatform="Windows Desktop"\nrunnable=true\nexport_filter="selected_resources"\nexport_files=PackedStringArray('+','.join(json.dumps(p) for p in roots)+')\ninclude_filter="*.png,*.json,*.ogg,NOTICE.md"\nexclude_filter="output/*,outputs/*,asset_backups/*,skills/*,.git/*"\nscript_export_mode=0\n\n[preset.0.options]\ncustom_template/debug='+json.dumps(template)+'\nbinary_format/embed_pck=false\nbinary_format/architecture="x86_64"\ntexture_format/s3tc_bptc=true\ncodesign/enable=false\napplication/modify_resources=false\n'
    (src/'export_presets.cfg').write_text(preset,encoding='utf-8')
    # Reuse import caches, then let the editor validate content hashes and rebuild changes.
    shutil.copytree(ROOT/'.godot/imported',src/'.godot/imported',dirs_exist_ok=True)
    for row in records:
        imported = ROOT/(row['path']+'.import')
        if imported.exists(): shutil.copy2(imported,src/(row['path']+'.import'))
    (out/'build').mkdir()
    for label,args in [('import',['--headless','--editor','--path',str(src),'--import','--quit']),('compile',['--headless','--path',str(src),'--script','res://scripts/main.gd','--check-only']),('export',['--headless','--path',str(src),'--export-debug','Windows Audio Playtest',str(out/'build/BrineSpace.exe')])]:
        with (out/(label+'.log')).open('w',encoding='utf-8') as log:
            result = subprocess.run([GODOT,*args],stdout=log,stderr=subprocess.STDOUT,timeout=900)
        errors = re.findall(r'^.*(?:SCRIPT ERROR:|ERROR:).*$',(out/(label+'.log')).read_text(errors='replace'),re.M)
        print(label,result.returncode,'errors',len(errors),flush=True)
        if result.returncode or errors: raise RuntimeError(label+' failed; inspect log')
    manifest = {p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in (out/'build').glob('*') if p.suffix in ['.exe','.pck']}
    (out/'package.json').write_text(json.dumps(manifest,indent=2))
    print('Package ready',flush=True)

if __name__ == '__main__': main()
