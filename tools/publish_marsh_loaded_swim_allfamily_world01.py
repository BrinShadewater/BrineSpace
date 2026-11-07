"""Publish exact-source pairs from the sixteen-state private q0 journey."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/publish_marsh_loaded_swim_northfamily_world01.py').read_text().replace('northfamily','allfamily').replace('opposite-ew-01-unselected/family-manifest.json','opposite-ns-01-unselected/family-manifest.json').replace('private North-turn family','private complete turn coverage')
exec(compile(s,str(__file__),'exec'))
