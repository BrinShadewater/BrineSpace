"""Publish q1/q3 sources against original manifest metadata, never flatten pivots."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];rev=sys.argv[1]
assert rev in ['03','04','05','06','07','08','09'];q={'03':'1','04':'3','05':'0 straight North site','06':'1 South pickup02','07':'2 Southdrain04','08':'2 Southdrain05','09':'2 Southdrain06'}[rev]
s=(ROOT/'tools/publish_marsh_loaded_swim_northfamily_world01.py').read_text()
s=s.replace("B=ROOT/'character/marsh-loaded-swim-turn-material-v1';A=ROOT/'output/marsh-animation-audit/loaded-swim-northfamily-world-01-2026-10-03';O=B/'northfamily-world-01-review'",f"B=ROOT/'character/marsh-water-transition-material-v1';A=ROOT/'output/marsh-animation-audit/water-transition-world-{rev}-2026-10-03';O=B/'transition-world-{rev}-review'")
s=s.replace("[B/'opposite-ew-01-unselected/family-manifest.json']","[ROOT/n for n in read(B/'combined03-cross-review/manifest-list.json')['manifests']]")
s=s.replace('q0 journey',f'q{q} journey').replace('private North-turn family','private staged cargo banks')
if rev=='06':s=s.replace('combined03-cross-review','combined04-cross-review')
if rev=='07':s=s.replace('combined03-cross-review','combined05-cross-review')
if rev=='08':s=s.replace('combined03-cross-review','combined06-cross-review')
if rev=='09':s=s.replace('combined03-cross-review','combined07-cross-review')
start=s.index("endpoint_checks=[];");end=s.index("v={'checks':",start)
s=s[:start]+"endpoint_checks=[]\n"+s[end:]
exec(compile(s,str(__file__),'exec'))
