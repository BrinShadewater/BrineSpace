"""Correct the fixture's prescribed clock coordinate ruler; retain failed V1 evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/review_bill_east_run_master_native_v1.gd').read_text(encoding='utf-8').replace('bill-east-run-master-native-v1/','bill-east-run-master-native-v2/')
source=source.replace('grid.human_animation_last_position=actor.foot/grid._cell_size()','grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size()')
source=source.replace('"actual retained run source selected at prescribed phase"','"actual retained run source selected at phase %d / elapsed %.4f"%[slot,grid.human_animation_phase]')
(R/'tools/review_bill_east_run_master_native_v2.gd').write_text(source,encoding='utf-8')
runner=(R/'tools/run_bill_east_run_master_native_v1.py').read_text(encoding='utf-8').replace('native_v1','native_v2').replace('native-v1','native-v2')
(R/'tools/run_bill_east_run_master_native_v2.py').write_text(runner,encoding='utf-8')
print('V2 uses the same actual position getter as the retained renderer. Failed V1 retained.')
