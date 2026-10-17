"""Build/validate requested stages; full output retained beside each script."""
from pathlib import Path
import subprocess,sys,json,time
H=Path(__file__).resolve().parent
stages=sys.argv[1:] or ['build_inspection','build_actions','validate_actions','build_cargo','validate_cargo','build_meals','validate_meals','build_equipment','validate_equipment','build_rest','validate_rest','build_recovery','build_death','validate_recovery_death','build_water','validate_water','build_package','validate_package']
for name in stages:
 start=time.monotonic()
 with (H/(name+'.log')).open('w',encoding='utf8') as log:
  p=subprocess.run([sys.executable,str(H/(name+'.py'))],stdout=log,stderr=subprocess.STDOUT)
 lines=(H/(name+'.log')).read_text().splitlines()
 print(json.dumps({'stage':name,'exit':p.returncode,'seconds':round(time.monotonic()-start,2),'tail':lines[-5:] if p.returncode else [s[:300] for s in lines[-3:]]}),flush=True)
 if p.returncode:raise SystemExit(p.returncode)
