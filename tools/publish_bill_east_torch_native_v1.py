"""Publish successful torch native evidence after the input freeze."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'tools/publish_bill_east_run_native_v2.py').read_text(encoding='utf-8')
s=s.replace('bill-east-run-master-native-v2','bill-east-torch-master-native-v2').replace('bill-east-run-master-v1','bill-east-torch-master-v1').replace('run pose','torch pose').replace('physical running route','physical torch job').replace('Native running comparison','Native torch comparison')
s=s.replace('2,931 saved-profile files',"{v['ownerNonLogCount']:,} saved-profile files")
s=s.replace("</p>'+''.join", "</p>\"+''.join").replace("html=html.replace('</html>','<h2>","html=html.replace('</html>',f\"<h2>")
exec(compile(s,str(__file__),'exec'))
page=R/'character/bill-east-torch-master-v1/index.html'
page.write_text(page.read_text(encoding='utf-8').replace('Selected torchning','Selected torch work'),encoding='utf-8')
