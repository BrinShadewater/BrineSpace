"""Reuse whole packing geometry for independently authored own-West source."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/pack_marsh_loaded_swim_turn_eastnorth02.py').read_text()
for a,b in [('east-north-02','west-north-01'),('east-north','west-north'),('north-east','north-west'),('eastnorth02','westnorth01'),('exact East02','exact West01'),('exec-de3c97d0-0d3a-46b7-9553-835d82bf45c5','exec-0dd0f7c4-7c73-4ab3-be0e-f72ab9b4b91e')]:s=s.replace(a,b)
p=ROOT/'tools/pack_marsh_loaded_swim_turn_westnorth01.py';p.write_text(s);exec(compile(s,str(p),'exec'))
