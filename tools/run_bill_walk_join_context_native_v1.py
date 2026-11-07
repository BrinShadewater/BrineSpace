from pathlib import Path
import os,json,subprocess,time
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1];D=R/'output/bill-walk-join-context-native-v1';D.mkdir(exist_ok=False)
before=owner();frozen=inputs();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir()
start=time.monotonic()
with (D/'engine.log').open('w',encoding='utf-8') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--script','res://tools/review_bill_walk_join_context_native_v1.gd','--resolution','1600x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
after=owner();current=inputs();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];source_changes=[p for p in frozen.keys()|current.keys() if frozen.get(p)!=current.get(p)]
report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8')
ok=r.returncode==0 and report.get('failures')==0 and len(report.get('contexts',[]))==9 and not changes and not source_changes and not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
v=dict(passed=ok,engineExit=r.returncode,seconds=round(time.monotonic()-start,2),checks=report.get('checks'),failures=report.get('failures'),contexts=report.get('contexts'),inputCount=len(frozen),inputChanges=source_changes,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA'],normalAdmission=False)
for name,data in [('validation',v),('inputs-before',frozen),('inputs-after',current),('owner-before',before),('owner-after',after)]: (D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(v));print(log[-2400:] if not ok else '')
raise SystemExit(0 if ok else 1)
