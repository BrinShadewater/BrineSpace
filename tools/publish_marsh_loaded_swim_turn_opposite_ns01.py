"""Publish verified composed North/South player captures and finite APNGs."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_loaded_swim_turn_opposite_ew01.py').read_text().replace('opposite-ew','opposite-ns').replace("pair=='east-west'","pair=='north-south'")
count=len(json.loads((ROOT/'output/marsh-animation-audit/loaded-swim-turn-opposite-ns-native-01-2026-10-03/inputs-before.json').read_text()))
s=s.replace("('inputs',92)","('inputs',"+str(count)+")")
exec(compile(s,str(__file__),'exec'))
