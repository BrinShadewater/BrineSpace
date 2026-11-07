"""Publish verified native front quarters and byte-exact finite holds."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
side=sys.argv[1];assert side in ('east','west')
pair=side+'-south'
audit=ROOT/f'output/marsh-animation-audit/loaded-swim-turn-{side}south-native-01-2026-10-03'
s=(ROOT/'tools/publish_marsh_loaded_swim_turn_westnorth01.py').read_text()
for a,b in [('west-north-01',pair+'-01'),('westnorth-native-01',side+'south-native-01'),("pair=='east-north'","pair=='"+pair+"'"),("('inputs',52)","('inputs',"+str(len(json.loads((audit/'inputs-before.json').read_text())))+")")]:s=s.replace(a,b)
exec(compile(s,str(__file__),'exec'))
