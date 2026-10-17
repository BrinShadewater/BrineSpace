from pathlib import Path
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
s=(R/'tests/test_veld_idle_north_original_master_v1.gd').read_text().replace('veld-idle-north-original-master-v1','veld-carry-north-original-master-v1').replace('veld-north-idle-scratch','veld-north-carry-original-scratch').replace('VELD ORIGINAL NORTH MASTER IDLE','VELD ORIGINAL NORTH CARRY FAMILY')
s='\n'.join(line for line in s.split('\n') if 'Unchanged action body' not in line)
(R/'tests/test_veld_carry_north_original_master_v1.gd').write_text(s)
(R/'tests/test_veld_carry_north_original_master_v1.gd.uid').write_text('uid://cvldcarrynorthorig1\n')
s=(R/'tools/run_veld_idle_north_original_master_v1.py').read_text().replace('veld-idle-north-original-master-v1','veld-carry-north-original-master-v1').replace('test_veld_idle_north_original_master_v1.gd','test_veld_carry_north_original_master_v1.gd').replace('veld-north-idle-scratch','veld-north-carry-original-scratch')
start=s.index('paths.update([P/');end=s.index('\ndef inputs():',start)
s=s[:start]+"paths.update(P.glob('raw-*.png'));paths.update(P.glob('prompt-*.txt'));paths.add(P/'register_source.py')"+s[end:]
s=s.replace('North original-guided prepared-master idle with four breathing poses, six North states/both gears, explicit-modulo elapsed source clocks and exact idle/cargo/action source joins.','North original-guided carry, derived start/stop and latest pickup/unload/idle six states paired. Explicit-modulo loop clocks, exact held/gait/rest aliases. Older turn joins remain open.')
(R/'tools/run_veld_carry_north_original_master_v1.py').write_text(s)
