from pathlib import Path
import re
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'tests/test_veld_cargo_turns_master_family.gd').read_text(encoding='utf-8')
s=s.replace('candidate-v7/','north-west-candidate-v4/').replace('veld-cargo-turns-master-family-v7-native-r3/','veld-cargo-turns-north-west-v4-native/')
s=s.replace('south-west','north-west').replace('west-south','west-north')
# Preserve all four baseline quarters; only the reviewed pair changes.
s=s.replace('baseline.load_manifest("res://character/veld-carry-turn-north-west-consistent-v1/bare-manifest.json",true)','baseline.load_manifest("res://character/veld-carry-turn-south-west-consistent-v1/bare-manifest.json",true)')
s=s.replace('VELD MASTER SOUTH WEST TURNS','VELD MASTER NORTH WEST TURNS')
assert len(set(re.findall(r'baseline.load_manifest\("([^"]+)"',s)))==3
gd=R/'tests/test_veld_cargo_turns_north_west_master.gd';gd.write_text(s,encoding='utf-8');gd.with_suffix('.gd.uid').write_text('uid://d0evctnw1\n',encoding='utf-8')
w=(R/'tools/run_veld_cargo_turns_master_family.py').read_text(encoding='utf-8')
w=w.replace('veld-cargo-turns-master-family-v7-native-r3','veld-cargo-turns-north-west-v4-native')
w=w.replace('test_veld_cargo_turns_master_family','test_veld_cargo_turns_north_west_master').replace('candidate-v7','north-west-candidate-v4')
w=w.replace('veld-carry-turn-south-west-consistent-v1','veld-carry-turn-north-west-consistent-v1')
w=w.replace("['north-east','east-south','north-west']","['north-east','east-south','south-west']")
w=w.replace('helmet-west-south-025-native.png','helmet-west-north-025-native.png').replace('South-West/West-South/both gears','North-West/West-North/both gears')
(R/'tools/run_veld_cargo_turns_north_west_master.py').write_text(w,encoding='utf-8')
print('Prepared North-West paired native fixture/UID/isolated runner; original clocks/full appended baseline library.')
