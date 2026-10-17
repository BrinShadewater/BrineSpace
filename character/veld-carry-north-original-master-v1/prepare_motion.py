from pathlib import Path
R=Path(__file__).resolve().parents[2]
s=(R/'tools/run_veld_carry_north_original_master_v1.py').read_text()
s=s.replace("O=R/'output/veld-carry-north-original-master-v1'","O=R/'output/veld-north-original-motion-v1'").replace('test_veld_carry_north_original_master_v1.gd','test_veld_north_original_motion_v1.gd').replace('veld-north-carry-original-scratch','veld-north-motion-scratch')
s=s.replace('North original-guided carry, derived start/stop and latest pickup/unload/idle six states paired. Explicit-modulo loop clocks, exact held/gait/rest aliases. Older turn joins remain open. No controller/world/save/case lifetime acceptance.','Prescribed continuous physical speed/position trace through paired North start/carry/stop, actual distance-driven sprite player and simulation finite clocks. No VeldNpc/station/controller/collision/props/save acceptance.')
(R/'tools/run_veld_north_original_motion_v1.py').write_text(s)
