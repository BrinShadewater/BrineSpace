"""Keep multiword torch action names intact; retain interrupted V1 evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/review_bill_east_family_native_v1.gd').read_text(encoding='utf-8')
s=s.replace('var state:String=key.get_slice("-",0)','var state:String=key.trim_suffix("-east")').replace('bill-east-family-native-v1/','bill-east-family-native-v2/')
(R/'tools/review_bill_east_family_native_v2.gd').write_text(s,encoding='utf-8')
s=(R/'tools/run_bill_east_family_native_v1.py').read_text(encoding='utf-8').replace('family_native_v1','family_native_v2').replace('family-native-v1','family-native-v2')
(R/'tools/run_bill_east_family_native_v2.py').write_text(s,encoding='utf-8')
print('V2 preserves torch-draw/torch-stow state names. No artwork changes.')
