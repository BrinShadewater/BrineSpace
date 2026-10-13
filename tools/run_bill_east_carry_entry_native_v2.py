from pathlib import Path
import os,json,subprocess,time,hashlib
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1];D=R/'output/bill-east-carry-entry-native-v2';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def current_inputs():
 result=inputs()
 for folder in ["bill-east-carry-master-v1","bill-east-cargo-handoffs-master-v1"]:
  for p in (R/"character"/folder).rglob("*"):
   if p.is_file():result[str(p)]=sha(p)
 for p in (R/'character/bill-east-carry-entry-master-v1').rglob('*'):
  if p.is_file():result[str(p)]=sha(p)
 review=json.loads((R/'character/bill-east-carry-entry-master-v1/review.json').read_text())
 for path in review['protectedInputs']:result[str(R/path)]=sha(R/path)
 for name in ['prepare_bill_east_carry_entry_master_v1.py','build_bill_east_carry_entry_master_v1.py','prepare_bill_east_carry_entry_native_v1.py','review_bill_east_carry_entry_native_v2.gd','review_bill_east_carry_entry_native_v2.gd.uid','run_bill_east_carry_entry_native_v2.py']:result[str(R/'tools'/name)]=sha(R/'tools'/name)
 return result
before=owner();frozen=current_inputs();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir();start=time.monotonic()
with (D/'engine.log').open('w',encoding='utf-8') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--script','res://tools/review_bill_east_carry_entry_native_v2.gd','--resolution','1600x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
after=owner();current=current_inputs();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];source_changes=[p for p in frozen.keys()|current.keys() if frozen.get(p)!=current.get(p)]
report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8');clean=not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
ok=r.returncode==0 and report.get('failures')==0 and len(report.get('captures',[]))==7 and len(report.get('records',[]))>=60 and not changes and not source_changes and clean
v=dict(passed=ok,engineExit=r.returncode,engineLogClean=clean,seconds=round(time.monotonic()-start,2),checks=report.get('checks'),failures=report.get('failures'),captures=len(report.get('captures',[])),inputCount=len(frozen),inputChanges=source_changes,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA'],normalAdmission=False)
for name,data in [('validation',v),('inputs-before',frozen),('inputs-after',current),('owner-before',before),('owner-after',after)]:(D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(v));print(log[-2400:] if not ok else '');raise SystemExit(0 if ok else 1)
