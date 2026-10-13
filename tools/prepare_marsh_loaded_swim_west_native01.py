"""Own-West staged player/native fixture, preserving six timing slots."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_loaded_swim_native02.py').read_text().replace('east-loop-02','west-loop-01').replace('swim-carry-east','swim-carry-west').replace('loaded-swim-east-native-02','loaded-swim-west-native-01').replace('idle-east','idle-west').replace('Whole02','WholeWest01').replace('East master','West master').replace('SWIM02','SWIM WEST01').replace('"east"','"west"')
s=s.replace('review_marsh_loaded_swim_material02.gd','review_marsh_loaded_swim_west01.gd').replace('uid://dv9swimeastmat13','uid://cnwq2txp6ge')
# Fixture raw-image reads follow the runtime PNG-buffer loading route.
s=s.replace('func _init():call_deferred("run")','func image_file(path:String) -> Image:\n\tvar result:=Image.new();result.load_png_from_buffer(FileAccess.get_file_as_bytes(path));return result\nfunc _init():call_deferred("run")')
s=s.replace('Image.load_from_file(', 'image_file(')
(ROOT/'tools/prepare_marsh_loaded_swim_west_native01_generated.py').write_text(s)
exec(compile(s,str(ROOT/'tools/prepare_marsh_loaded_swim_west_native01_generated.py'),'exec'))
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_material02.py').read_text().replace('review_marsh_loaded_swim_material02.gd','review_marsh_loaded_swim_west01.gd')
f=f.replace("records={p.relative_to(ROOT).as_posix()", "paths += [ROOT/'tools'/n for n in ['prepare_marsh_loaded_swim_west01.py','retain_pack_marsh_loaded_swim_west01.py','pack_marsh_loaded_swim_west01.py','prepare_marsh_loaded_swim_west_native01.py','prepare_marsh_loaded_swim_west_native01_generated.py','fingerprint_marsh_loaded_swim_west01.py']]\nrequest=json.loads((B/'sources/west-loop-01.request.json').read_text());paths+=[ROOT/q['path'] for q in request['orderedReferences']+request['sourceFrames']]\npaths += [p for p in (B/'sources').glob('west-*') if p.suffix in ['.png','.json','.txt']]\npaths += list((B/'west-loop-01-unselected').glob('*'))\nrecords={p.relative_to(ROOT).as_posix()")
(ROOT/'tools/fingerprint_marsh_loaded_swim_west01.py').write_text(f)
