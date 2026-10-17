from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
test=(R/'tests/test_veld_cargo_west_master_family.gd').read_text().replace('west','east').replace('WEST','EAST')
(R/'tests/test_veld_cargo_east_master_family.gd').write_text(test,encoding='utf-8')
(R/'tests/test_veld_cargo_east_master_family.gd.uid').write_text('uid://cp5dewl7vn2cg\n',encoding='utf-8')
runner=(R/'tools/run_veld_cargo_west_master_family.py').read_text().replace('west','east')
(R/'tools/run_veld_cargo_east_master_family.py').write_text(runner,encoding='utf-8')
print('Prepared finite paired East action player review with scratch profile isolation.')
