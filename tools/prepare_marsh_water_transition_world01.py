"""Join current private cargo banks for one normal dispatched world review."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1';O=B/'combined01-cross-review';O.mkdir(exist_ok=True)
manifests=['character/marsh-loaded-swim-turn-material-v1/opposite-ns-01-unselected/family-manifest.json','character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json','character/marsh-cargo-held-material-v1/side02-cross-review/family-manifest.json']
manifests +=[f"character/marsh-{side}-carry-material-v1/candidate-{'03' if side in ('east','west') else '01'}/manifest.json" for side in ['east','west','north','south']]
manifests +=['character/marsh-water-transition-material-v1/pickup-east-02-unselected/manifest.json','character/marsh-water-transition-material-v1/drain-north-01-unselected/manifest.json']
# Loading each original manifest preserves its own pivot/frame dimensions.
source=(ROOT/'tools/review_marsh_loaded_swim_allfamily_world01.gd').read_text()
source=source.replace('loaded-swim-allfamily-world-01','water-transition-world-01')
old='player.load_manifest("res://character/marsh-loaded-swim-turn-material-v1/opposite-ns-01-unselected/family-manifest.json",true)'
source=source.replace(old,'\n\t'.join('player.load_manifest("res://'+n+'",true)' for n in manifests))
source=source.replace('or key.begins_with("unload-")','or key.begins_with("unload-") or key.begins_with("carry-")')
source=source.replace('Private four loaded loops/twelve water turns (sixteen states) overrides; old pickup/drain/unload. q0 actual EastWest and WestSouth use new source. No claim all staged states witnessed.','Private sixteen water states plus dry carry/turn/held banks and pickupEast02/drainNorth01; original per-manifest metadata retained. Other pickup/drain directions remain old. Actual keys establish witnessed scope, not all staged states.')
source=source.replace('MARSH ALL WATER FAMILY WORLD01','MARSH WATER TRANSITION WORLD01')
p=ROOT/'tools/review_marsh_water_transition_world01.gd';p.write_text(source);p.with_suffix('.gd.uid').write_text('uid://ce5k7pm2nv4r\n')
(O/'manifest-list.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'manifests':manifests,'operations':'Private ordered original manifests, no conflating184/p92 dry metadata with224/p112 water metadata. Exact whole endpoints normalized only inside transition bank. Actual route witness distinct from loaded coverage.'},indent=2)+'\n')
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_allfamily_world01.py').read_text()
for a,b in [('prepare_marsh_loaded_swim_allfamily_world01.py','prepare_marsh_water_transition_world01.py'),('review_marsh_loaded_swim_allfamily_world01.gd','review_marsh_water_transition_world01.gd'),('fingerprint_marsh_loaded_swim_allfamily_world01.py','fingerprint_marsh_water_transition_world01.py')]:f=f.replace(a,b)
f=f.replace('data={p.relative_to(ROOT).as_posix()',"for p in (ROOT/'character/marsh-water-transition-material-v1').rglob('*'):\n    if p.is_file() and p.suffix in ['.png','.json','.txt']:paths.append(p)\ndata={p.relative_to(ROOT).as_posix()")
(ROOT/'tools/fingerprint_marsh_water_transition_world01.py').write_text(f)
print('Combined private original-metadata q0 gate prepared; added actual dry carry/turn capture coverage.')
