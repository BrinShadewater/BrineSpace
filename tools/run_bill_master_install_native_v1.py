"""Native actual-job review with isolated profile and before/after fingerprints."""
from pathlib import Path
import os,json,subprocess,time,hashlib,sys
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1]
D=R/'output/bill-master-install-native-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def current_inputs():
 result=inputs()
 for folder in ['bill-east-carry-master-v1','bill-east-torch-master-v1','bill-east-torch-handoffs-master-v1','bill-east-cargo-handoffs-master-v1','bill-east-run-master-v2','bill-east-carry-entry-master-v1','bill-carry-turn-east-seams-v1']:
  for p in (R/'character'/folder).rglob('*'):
   if p.is_file():result[str(p)]=sha(p)
 for p in [R/'tools/prepare_bill_master_install_native_v1.py',R/'tools/review_bill_master_install_native_v1.gd',R/'tools/review_bill_master_install_native_v1.gd.uid',Path(__file__)]:result[str(p)]=sha(p)
 return result
before=owner();frozen=current_inputs();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir();start=time.monotonic()
def write(name,data):(D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
write('owner-before',before);write('inputs-before',frozen)
code=-1
with (D/'engine.log').open('w',encoding='utf-8') as log:
 try:code=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--script','res://tools/review_bill_master_install_native_v1.gd','--resolution','1600x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
 except subprocess.TimeoutExpired:pass
after=owner();current=current_inputs();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];source_changes=[p for p in frozen.keys()|current.keys() if frozen.get(p)!=current.get(p)]
report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8');clean=not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
ok=code==0 and report.get('failures')==0 and len(report.get('saves',[]))==4 and report.get('selectedSlots')==238 and not changes and not source_changes and clean
v=dict(passed=ok,engineExit=code,engineLogClean=clean,seconds=round(time.monotonic()-start,2),checks=report.get('checks'),failures=report.get('failures'),captures=len(report.get('captures',[])),inputCount=len(frozen),inputChanges=source_changes,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA'],normalAdmission=ok)
for name,data in [('validation',v),('inputs-after',current),('owner-after',after)]:write(name,data)
print(json.dumps(v))
if not ok:print('\n'.join(line for line in log.splitlines() if any(s in line for s in ['ERROR','WARNING',' at:']))[-2400:])
raise SystemExit(0 if ok else 1)
