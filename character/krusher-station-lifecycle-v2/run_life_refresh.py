from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,sys,json,time
P=Path(__file__).resolve().parent
names=['repair','galley','bunk','chairs:crew_lounge','chairs:observation_room','mortality','construction','workshop']
def run(name):
 out=P/'review'/name.replace(':','/')/'runner.log';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('w') as log:
  result=subprocess.run([sys.executable,str(P/('run_'+name.split(':')[0]+'.py'))]+name.split(':')[1:],stdout=log,stderr=subprocess.STDOUT)
 print(json.dumps({'fixture':name,'exit':result.returncode,'log':str(out)}),flush=True)
 return name,result.returncode
with ThreadPoolExecutor(max_workers=2) as pool:
 results=dict(job.result() for job in as_completed([pool.submit(run,n) for n in names]))
(P/'review/life-refresh.json').write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any(results.values()))
