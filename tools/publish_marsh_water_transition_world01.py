"""Publish exact source/native pairs from the combined normal q0 route."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_loaded_swim_allfamily_world01.py').read_text()
# Resolve the wrapper to its actual publishing implementation.
s=(ROOT/'tools/publish_marsh_loaded_swim_northfamily_world01.py').read_text().replace('northfamily','allfamily').replace('opposite-ew-01-unselected/family-manifest.json','opposite-ns-01-unselected/family-manifest.json')
s=s.replace("B=ROOT/'character/marsh-loaded-swim-turn-material-v1';A=ROOT/'output/marsh-animation-audit/loaded-swim-allfamily-world-01-2026-10-03';O=B/'allfamily-world-01-review'", "B=ROOT/'character/marsh-water-transition-material-v1';A=ROOT/'output/marsh-animation-audit/water-transition-world-01-2026-10-03';O=B/'transition-world-01-review'")
s=s.replace("[B/'opposite-ns-01-unselected/family-manifest.json']", "[ROOT/n for n in read(B/'combined01-cross-review/manifest-list.json')['manifests']]")
s=s.replace('private North-turn family','private staged cargo banks')
exec(compile(s,str(__file__),'exec'))
