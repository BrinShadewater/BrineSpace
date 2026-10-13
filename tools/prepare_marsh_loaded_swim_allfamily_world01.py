"""Normal dispatched q0 with all sixteen private loaded-water states."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_loaded_swim_northfamily_world01.gd').read_text()
for a,b in [('northfamily','allfamily'),('opposite-ew-01-unselected/family-manifest.json','opposite-ns-01-unselected/family-manifest.json'),('Private four loaded loops/six North-route water turns (ten states) overrides; old other clips including WestSouth. q0 actual EastWest uses new composed source. No claim all staged states witnessed.','Private four loaded loops/twelve water turns (sixteen states) overrides; old pickup/drain/unload. q0 actual EastWest and WestSouth use new source. No claim all staged states witnessed.'),('MARSH NORTH WATER FAMILY','MARSH ALL WATER FAMILY')]:s=s.replace(a,b)
p=ROOT/'tools/review_marsh_loaded_swim_allfamily_world01.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dc7m3pqn8vh5\n')
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_northfamily_world01.py').read_text().replace('northfamily','allfamily')
(ROOT/'tools/fingerprint_marsh_loaded_swim_allfamily_world01.py').write_text(f)
print('Normal q0 fixture prepared; sixteen staged states loaded, actual keys will establish witnessed scope.')
