"""Run targeted crew/service regressions with an isolated profile and owner fingerprints."""
from pathlib import Path
import os, sys, subprocess, json, time
from run_bill_inspection_activities_validation import fingerprint, ROOT
OUT=ROOT/'output/bill-inspection-regression-v1'
OUT.mkdir(exist_ok=True)
before=fingerprint()
env=os.environ.copy()
scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True)
env['APPDATA']=str(scratch)
started=time.monotonic()
with (OUT/'regression.log').open('w',encoding='utf-8') as log:
    result=subprocess.run([sys.executable,str(ROOT/'tools/run_tests.py'),'--only','test_bill_npc,test_crew_room_activity,test_crew_life_rooms,test_cold_store_stations,test_galley_counter_stations'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=360)
after=fingerprint()
changed=[name for name in before.keys()|after.keys() if before.get(name)!=after.get(name)]
for name,value in [('profile-before.json',before),('profile-after.json',after)]:
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
report={'passed':result.returncode==0 and not changed,'returnCode':result.returncode,'seconds':round(time.monotonic()-started,2),'realProfileFileCount':len(before),'realProfileChanges':changed}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
print('\n'.join((OUT/'regression.log').read_text(encoding='utf-8').splitlines()[-12:]))
raise SystemExit(0 if report['passed'] else 1)
