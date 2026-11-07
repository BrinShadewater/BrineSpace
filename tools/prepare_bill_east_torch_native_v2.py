"""Correct startup dispatch; retain failed V1 fixture and evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_torch_master_native_v1.gd').read_text(encoding='utf-8')
s=s.replace('call_deferred("weld")','call_deferred("run")').replace('bill-east-torch-master-native-v1/','bill-east-torch-master-native-v2/')
(R/'tools/review_bill_east_torch_master_native_v2.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_bill_east_torch_master_native_v1.py').read_text(encoding='utf-8')
s=s.replace('torch_master_native_v1','torch_master_native_v2').replace('torch_native_v1','torch_native_v2').replace('torch-master-native-v1','torch-master-native-v2')
(R/'tools/run_bill_east_torch_master_native_v2.py').write_text(s,encoding='utf-8')
print('V2 startup fixed; V1 failure retained.')
