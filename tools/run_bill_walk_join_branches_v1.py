"""Run targeted join state checks under an isolated profile with owner fingerprints."""
from pathlib import Path
import os,json,subprocess
from run_bill_east_walk_join_native_v1 import owner
R=Path(__file__).resolve().parents[1];D=R/'output/bill-walk-join-branches-v1';D.mkdir(exist_ok=False)
before=owner();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir()
with (D/'engine.log').open('w',encoding='utf-8') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--headless','--path',str(R),'--script','res://tools/test_bill_walk_join_candidate_v1.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=60)
after=owner();changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)];report=json.loads((D/'report.json').read_text(encoding='utf-8')) if (D/'report.json').exists() else {};log=(D/'engine.log').read_text(encoding='utf-8');ok=r.returncode==0 and report.get('failures')==0 and not changes and not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:'])
v=dict(passed=ok,engineExit=r.returncode,report=report,ownerNonLogCount=len(before),ownerChanges=changes,scratchAPPDATA=env['APPDATA']);(D/'verification.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print(json.dumps(v));print(log[-1000:] if not ok else '')
raise SystemExit(0 if ok else 1)
