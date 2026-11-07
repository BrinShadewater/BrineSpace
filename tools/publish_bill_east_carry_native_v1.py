"""Publish carry evidence after the native input freeze completes."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/publish_bill_east_run_native_v2.py').read_text(encoding='utf-8')
s=s.replace('bill-east-run-master-native-v2','bill-east-carry-master-native-v1').replace('bill-east-run-master-v1','bill-east-carry-master-v1')
s=s.replace("v['checks']==75", "v['checks']==90").replace("v['captures']==16", "v['captures']==20")
s=s.replace('range(4)','range(5)').replace('page<3','page<4').replace('run pose','carry pose')
s=s.replace('75 checks','90 checks').replace('All six poses','All eight poses').replace('physical running route','physical carrying route').replace('Native running comparison','Native carrying comparison').replace('comparisonPages=4','comparisonPages=5')
exec(compile(s,str(__file__),'exec'))
page=R/'character/bill-east-carry-master-v1/index.html'
page.write_text(page.read_text(encoding='utf-8').replace('Selected carryning','Selected carrying'),encoding='utf-8')
