from pathlib import Path
import re
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_cargo_turns_north_east_master.gd').read_text(encoding='utf-8')
s=s.replace('north-east-candidate-v5','east-south-candidate-v3').replace('veld-cargo-turns-north-east-v5-native','veld-cargo-turns-east-south-v3-native')
s=s.replace('north-east','east-south').replace('east-north','south-east')
s=s.replace('baseline.load_manifest("res://character/veld-carry-turn-east-south-consistent-v1/bare-manifest.json",true)','baseline.load_manifest("res://character/veld-carry-turn-north-east-consistent-v1/bare-manifest.json",true)')
s=s.replace('VELD MASTER NORTH EAST TURNS','VELD MASTER EAST SOUTH TURNS')
assert len(set(re.findall(r'baseline.load_manifest\("([^"]+)"',s)))==3
gd=R/'tests/test_veld_cargo_turns_east_south_master.gd';gd.write_text(s,encoding='utf-8');gd.with_suffix('.gd.uid').write_text('uid://d0evctes1\n',encoding='utf-8')
w=(R/'tools/run_veld_cargo_turns_north_east_master.py').read_text(encoding='utf-8')
w=w.replace('north-east-candidate-v5','east-south-candidate-v3').replace('veld-cargo-turns-north-east-v5-native','veld-cargo-turns-east-south-v3-native')
w=w.replace('test_veld_cargo_turns_north_east_master','test_veld_cargo_turns_east_south_master')
w=w.replace('veld-carry-turn-north-east-consistent-v1','veld-carry-turn-east-south-consistent-v1')
w=w.replace("['north-west','east-south','south-west']","['north-west','north-east','south-west']")
w=w.replace('helmet-east-north-025-native.png','helmet-south-east-025-native.png').replace('North-East/East-North/both gears','East-South/South-East/both gears')
(R/'tools/run_veld_cargo_turns_east_south_master.py').write_text(w,encoding='utf-8')
print('Prepared independent East-South paired fixture/UID/full baseline/isolated runner')
