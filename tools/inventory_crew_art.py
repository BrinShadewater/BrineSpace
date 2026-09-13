"""Freeze native effective crew pixels and metadata before a full art migration.

Reads the current loader block instead of maintaining a second list of overlays.
The dump is evidence, not authored source art. Never overwrite an existing baseline.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', default='C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe')
    parser.add_argument('--output', type=Path, default=ROOT/'output/crew-replacement-2026-09-12/runtime-baseline')
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination.exists():
        raise SystemExit('Baseline already exists; select a new output directory.')
    destination.relative_to(ROOT)
    source = ROOT/'scripts/grid_canvas.gd'
    code = source.read_text(encoding='utf-8')
    if '\t_load_replacement_crew_animations()' in code:
        block = '\tgrid._load_replacement_crew_animations()\n'
    else:
        start = code.index('\tveld_player.load_manifest(')
        end = code.index('\thuman_sprite =', start)
        block = code[start:end]
    for name in ['veld_player', 'branforth_player', 'marsh_player']:
        block = block.replace(name, 'grid.'+name)
    for name in ['_load_water_pilots', '_load_dry_helmet_pilots', '_load_helmet_transitions']:
        block = block.replace(name+'(', 'grid.'+name+'(')
    block = block.replace('CrewSpritePlayer.new()', 'load("res://scripts/crew_sprite_player.gd").new()')
    destination.mkdir(parents=True)
    script = '''extends SceneTree
var destination := %s
func _init() -> void: call_deferred("run")
func run() -> void:
\tif DisplayServer.get_name()=="headless":
\t\tpush_error("Native renderer required for immutable pixel baseline")
\t\tquit(2)
\t\treturn
\tvar grid = load("res://scripts/grid_canvas.gd").new()
%s
\tfor actor in ["veld","branforth","marsh"]:
\t\tvar player = grid.get(actor+"_player")
\t\tvar inventory := {"actor":actor,"states":[],"equipment":[],"strides":player.strides}
\t\tfor variant in ["bare","diving-helmet"]:
\t\t\tvar rows: Dictionary = player.frames if variant=="bare" else player.equipment_frames.get(variant,{})
\t\t\tfor key in rows:
\t\t\t\tvar entry := {"id":key,"timing":player.timing.get(key,{}),"frames":[]}
\t\t\t\tfor i in range(rows[key].size()):
\t\t\t\t\tvar texture: Texture2D = rows[key][i]
\t\t\t\t\tvar path: String = actor+"/"+variant+"/"+str(key)+"/%%03d.png"%%i
\t\t\t\t\tDirAccess.make_dir_recursive_absolute(destination.path_join(path).get_base_dir())
\t\t\t\t\tvar error := texture.get_image().save_png(destination.path_join(path))
\t\t\t\t\tif error!=OK: quit(1); return
\t\t\t\t\tvar metadata := {}
\t\t\t\t\tfor name in texture.get_meta_list():
\t\t\t\t\t\tvar value = texture.get_meta(name)
\t\t\t\t\t\tmetadata[name] = [value.x,value.y] if value is Vector2 else value
\t\t\t\t\tentry.frames.append({"file":path,"size":[texture.get_width(),texture.get_height()],"meta":metadata})
\t\t\t\tinventory["states" if variant=="bare" else "equipment"].append(entry)
\t\tvar file := FileAccess.open(destination.path_join(actor+".json"),FileAccess.WRITE)
\t\tfile.store_string(JSON.stringify(inventory,"  "))
\t\tfile.close()
\tgrid.free()
\tprint("CREW BASELINE PASS")
\tquit()
''' % (json.dumps(destination.as_posix()), block)
    fixture = destination/'capture.gd'
    fixture.write_text(script, encoding='utf-8')
    with (destination/'capture.log').open('w', encoding='utf-8') as log:
        result = subprocess.run([args.godot, '--path', str(ROOT), '--windowed', '--resolution', '640x360', '--script', str(fixture)], stdout=log, stderr=subprocess.STDOUT, timeout=180)
    logtext = (destination/'capture.log').read_text(encoding='utf-8')
    if result.returncode or 'CREW BASELINE PASS' not in logtext or 'SCRIPT ERROR' in logtext:
        raise SystemExit('Capture failed; inspect '+str(destination/'capture.log'))
    summary = {'loaderSha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'characters':{}}
    for actor in ['veld','branforth','marsh']:
        inventory = json.loads((destination/(actor+'.json')).read_text())
        for family in ['states','equipment']:
            for entry in inventory[family]:
                for frame in entry['frames']:
                    frame['sha256'] = hashlib.sha256((destination/frame['file']).read_bytes()).hexdigest()
        (destination/(actor+'.json')).write_text(json.dumps(inventory,indent=2)+'\n')
        summary['characters'][actor] = {family:{'states':len(inventory[family]),'frames':sum(len(row['frames']) for row in inventory[family])} for family in ['states','equipment']}
    (destination/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()

