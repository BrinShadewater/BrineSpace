"""Exercise the changed complete bank with the corrected native coordinate fixture."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/review_bill_east_run_master_native_v2.gd').read_text(encoding='utf-8').replace('native-v2/','native-v3/').replace('bill-east-run-master-v1/manifest.json','bill-east-run-master-v2/manifest.json')
(R/'tools/review_bill_east_run_master_native_v3.gd').write_text(source,encoding='utf-8')
runner=(R/'tools/run_bill_east_run_master_native_v2.py').read_text(encoding='utf-8').replace('native_v2','native_v3').replace('native-v2','native-v3').replace('character/bill-east-run-master-v1','character/bill-east-run-master-v2')
runner=runner.replace('from run_bill_east_walk_join_native_v3 import','from run_bill_east_walk_join_native_v2 import')
(R/'tools/run_bill_east_run_master_native_v3.py').write_text(runner,encoding='utf-8')
print('Prepared six-phase native check for arm revision.')
