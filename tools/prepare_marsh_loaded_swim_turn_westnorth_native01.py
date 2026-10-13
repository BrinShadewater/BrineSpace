"""Prepare independently authored rearLEFT directed player review."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/prepare_marsh_loaded_swim_turn_eastnorth_native02.py').read_text()
for a,b in [('east-north-02','west-north-01'),('east-north','west-north'),('north-east','north-west'),('eastnorth-native-02','westnorth-native-01'),('eastnorth02.gd','westnorth01.gd'),('EASTNORTH02','WESTNORTH01'),('uid://bn7p2gh4m6sk','uid://cx7mj2h8p4vn'),('2026-10-02','2026-10-03')]:s=s.replace(a,b)
p=ROOT/'tools/prepare_marsh_loaded_swim_turn_westnorth_native01_generated.py';p.write_text(s);exec(compile(s,str(p),'exec'))
f=(ROOT/'tools/fingerprint_marsh_loaded_swim_turn_eastnorth02.py').read_text().replace('east-north-02','west-north-01').replace('marsh_loaded_swim_turn_eastnorth','marsh_loaded_swim_turn_westnorth')
(ROOT/'tools/fingerprint_marsh_loaded_swim_turn_westnorth01.py').write_text(f)
