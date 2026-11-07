"""Stage South player-only review using the actual current selected idle."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'character/marsh-loaded-swim-material-v1/sources/south-loop-01.request.json').read_text())
s=(ROOT/'tools/prepare_marsh_loaded_swim_west_native01_generated.py').read_text()
for a,b in [('west-loop-01','south-loop-01'),('swim-carry-west','swim-carry-south'),('loaded-swim-west-native-01','loaded-swim-south-native-01'),('character/marsh-v2/frames/bare/idle-west/000.png',r['selectedIdleMaster']['path']),('WholeWest01','WholeSouth01'),('West master','South master'),('SWIM WEST01','SWIM SOUTH01'),('"west"','"south"'),('review_marsh_loaded_swim_west01.gd','review_marsh_loaded_swim_south01.gd'),('uid://cnwq2txp6ge','uid://bq3kv7h5ps9m'),('marsh-loaded-swim-east-material02-unselected','marsh-loaded-swim-south-material01-unselected'),('four whole02 figures','four whole South01 figures')]:s=s.replace(a,b)
p=ROOT/'tools/prepare_marsh_loaded_swim_south_native01_generated.py';p.write_text(s);exec(compile(s,str(p),'exec'))
