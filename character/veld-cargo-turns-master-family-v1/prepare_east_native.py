from pathlib import Path
import re
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_cargo_turns_north_west_master.gd').read_text(encoding='utf-8')
s=s.replace('north-west-candidate-v4','north-east-candidate-v5').replace('veld-cargo-turns-north-west-v4-native','veld-cargo-turns-north-east-v5-native')
s=s.replace('north-west','north-east').replace('west-north','east-north')
s=s.replace('baseline.load_manifest("res://character/veld-carry-turn-north-east-consistent-v1/bare-manifest.json")','baseline.load_manifest("res://character/veld-carry-turn-north-west-consistent-v1/bare-manifest.json")')
s=s.replace('VELD MASTER NORTH WEST TURNS','VELD MASTER NORTH EAST TURNS')
assert len(set(re.findall(r'baseline.load_manifest\("([^"]+)"',s)))==3
gd=R/'tests/test_veld_cargo_turns_north_east_master.gd';gd.write_text(s,encoding='utf-8');gd.with_suffix('.gd.uid').write_text('uid://d0evctne1\n',encoding='utf-8')
w=(R/'tools/run_veld_cargo_turns_north_west_master.py').read_text(encoding='utf-8')
w=w.replace('north-west-candidate-v4','north-east-candidate-v5').replace('veld-cargo-turns-north-west-v4-native','veld-cargo-turns-north-east-v5-native')
w=w.replace('test_veld_cargo_turns_north_west_master','test_veld_cargo_turns_north_east_master')
w=w.replace('veld-carry-turn-north-west-consistent-v1','veld-carry-turn-north-east-consistent-v1')
w=w.replace("['north-east','east-south','south-west']","['north-west','east-south','south-west']")
w=w.replace('helmet-west-north-025-native.png','helmet-east-north-025-native.png').replace('North-West/West-North/both gears','North-East/East-North/both gears')
(R/'tools/run_veld_cargo_turns_north_east_master.py').write_text(w,encoding='utf-8')
print('Prepared independent North-East native fixture with full four-quarter baseline')
