"""Reuse the source-review publisher for the changed arm bank and its native run."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'tools/publish_bill_east_run_native_v2.py').read_text(encoding='utf-8').replace('bill-east-run-master-native-v2','bill-east-run-master-native-v3').replace('bill-east-run-master-v1','bill-east-run-master-v2')
exec(compile(source,str(R/'tools/publish_bill_east_run_native_v2.py'),'exec'))
D=R/'character/bill-east-run-master-v2';p=D/'index.html';html=p.read_text(encoding='utf-8')
html=html.replace('Selected running','Reported arm').replace('id="old" src="selected-1.png"','id="old" src="../bill-east-run-master-v1/candidate-1.png"')
html=html.replace("['old','selected']","['old','../bill-east-run-master-v1/candidate']")
html=html.replace("'../bill-run-head-locked-v1/frames/run-east/000.png'","'../bill-east-run-master-v1/frames/000.png'")
p.write_text(html,encoding='utf-8')
print('Reported V1 arm and repaired V2 arm are compared directly in playback.')
