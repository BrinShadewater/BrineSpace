"""Source-resolution audit isolated from the owner profile."""
from pathlib import Path
import os,json,subprocess,time,hashlib
from run_bill_east_walk_join_native_v2 import owner,inputs
R=Path(__file__).resolve().parents[1];D=R/'output/bill-installed-coverage-v2';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((R/'character/bill-installed-coverage-2026-10-04/source-audit.json').read_text())
def frozen():
 result=inputs()
 for relative in audit['sourcePaths']+list(audit['manifestBindings']):result[str(R/relative)]=sha(R/relative)
 for relative in ['character/bill-installed-coverage-2026-10-04/source-audit.json','tools/audit_bill_installed_coverage_v1.py','tools/review_bill_installed_coverage_v2.gd','tools/review_bill_installed_coverage_v2.gd.uid','tools/run_bill_installed_coverage_v2.py']:result[str(R/relative)]=sha(R/relative)
 return result
before=owner();source=frozen();env=os.environ.copy();env['APPDATA']=str(D/'scratch-appdata');Path(env['APPDATA']).mkdir()
def write(name,data):(D/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
write('owner-before',before);write('inputs-before',source);start=time.monotonic()
with (D/'engine.log').open('w',encoding='utf-8') as log:
 process=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--headless','--path',str(R),'--script','res://tools/review_bill_installed_coverage_v2.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
after=owner();current=frozen();log=(D/'engine.log').read_text();q=json.loads((D/'report.json').read_text()) if (D/'report.json').exists() else {}
changes=[p for p in source.keys()|current.keys() if source.get(p)!=current.get(p)];owner_changes=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
clean=not any(s in log for s in ['ERROR:','SCRIPT ERROR','WARNING:']);ok=process.returncode==0 and q.get('failures')==0 and not changes and not owner_changes and clean
v={'passed':ok,'engineExit':process.returncode,'engineLogClean':clean,'seconds':round(time.monotonic()-start,2),'checks':q.get('checks'),'failures':q.get('failures'),'summary':q.get('summary'),'inputCount':len(source),'inputChanges':changes,'ownerNonLogCount':len(before),'ownerChanges':owner_changes,'scratchAPPDATA':env['APPDATA'],'visualAcceptance':False}
for name,data in [('validation',v),('owner-after',after),('inputs-after',current)]:write(name,data)
print(json.dumps(v))
if not ok:print('\n'.join(log.splitlines()[-22:]))
raise SystemExit(0 if ok else 1)
