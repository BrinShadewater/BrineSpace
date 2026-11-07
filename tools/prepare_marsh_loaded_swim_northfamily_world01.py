"""Normal q0 expedition with four loops/six North-route water turns staged privately."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_loaded_swim_west_world01.gd').read_text()
s=s.replace('loaded-swim-west-world-01-2026-10-02','loaded-swim-northfamily-world-01-2026-10-03')
old='player.load_manifest("res://character/marsh-loaded-swim-material-v1/east-loop-02-unselected/manifest.json",true)\n\tplayer.load_manifest("res://character/marsh-loaded-swim-material-v1/west-loop-01-unselected/manifest.json",true)'
assert old in s
s=s.replace(old,'player.load_manifest("res://character/marsh-loaded-swim-turn-material-v1/opposite-ew-01-unselected/family-manifest.json",true)')
s=s.replace('Private East02 and West01 loaded-swim source overrides, old other clips.','Private four loaded loops/six North-route water turns (ten states) overrides; old other clips including WestSouth. q0 actual EastWest uses new composed source. No claim all staged states witnessed.')
s=s.replace('MARSH LOADED SWIM WORLD02','MARSH NORTH WATER FAMILY WORLD01')
p=ROOT/'tools/review_marsh_loaded_swim_northfamily_world01.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://cq4pn7km2v6s\n')
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_west_world01.py').read_text()
for a,b in [('prepare_marsh_loaded_swim_west_world01.py','prepare_marsh_loaded_swim_northfamily_world01.py'),('review_marsh_loaded_swim_west_world01.gd','review_marsh_loaded_swim_northfamily_world01.gd'),('fingerprint_marsh_loaded_swim_west_world01.py','fingerprint_marsh_loaded_swim_northfamily_world01.py')]:f=f.replace(a,b)
needle='data={p.relative_to(ROOT).as_posix()';assert needle in f
extra='''turn_root=ROOT/'character/marsh-loaded-swim-turn-material-v1'
for p in turn_root.rglob('*'):
    if p.is_file() and p.suffix in ['.png','.json','.txt']:paths.append(p)
paths += [ROOT/'tools'/n for n in ['prepare_marsh_loaded_swim_northfamily_world01.py','review_marsh_loaded_swim_northfamily_world01.gd','review_marsh_loaded_swim_northfamily_world01.gd.uid','fingerprint_marsh_loaded_swim_northfamily_world01.py']]
'''
f=f.replace(needle,extra+needle)
(ROOT/'tools/fingerprint_marsh_loaded_swim_northfamily_world01.py').write_text(f)
print('Actual normal q0 dispatched route fixture ready; private ten-state override, other states old.')
