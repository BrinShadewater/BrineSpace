"""Stage all six torch source phases in the existing furnished-room fixture."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_run_master_native_v2.gd').read_text(encoding='utf-8')
s=s.replace('bill-east-run-master-native-v2','bill-east-torch-master-native-v1').replace('bill-east-run-master-v1','bill-east-torch-master-v1').replace('run-east','weld-east').replace('"run"','"weld"').replace('run pose','torch pose').replace('candidate run','candidate torch').replace('selected run','selected torch').replace('retained run','retained torch').replace('original run timing','original torch timing').replace('BILL RUN','BILL TORCH').replace('candidate run poses','candidate torch poses').replace('physical running','physical torch job')
(R/'tools/review_bill_east_torch_master_native_v1.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_bill_east_run_master_native_v3.py').read_text(encoding='utf-8')
s=s.replace('bill-east-run-master-native-v3','bill-east-torch-master-native-v1').replace('bill-east-run-master-v2','bill-east-torch-master-v1').replace('prepare_bill_east_run_native_v3','prepare_bill_east_torch_native_v1').replace('review_bill_east_run_master_native_v3','review_bill_east_torch_master_native_v1').replace('run_bill_east_run_master_native_v3','run_bill_east_torch_master_native_v1')
(R/'tools/run_bill_east_torch_master_native_v1.py').write_text(s,encoding='utf-8')
print('Six selected/candidate torch poses and idle endpoints prepared.')
