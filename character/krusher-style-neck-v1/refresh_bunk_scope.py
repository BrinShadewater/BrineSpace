from pathlib import Path
import json
H=Path(__file__).resolve().parent;R=H.parents[1];P=R/'character/krusher-animation-package-v9';index=json.loads((P/'package.json').read_text());jobs=json.loads((H/'bunk-scope.json').read_text())
for job in jobs:
 q=index['states'][job['gear']+':'+job['key']];mp=P/q['manifest'];m=json.loads(mp.read_text());s=next(s for s in m['states'] if s['id']==job['key'])
 assert job['durations']==s['frameDurationsMs'] and len(job['files'])==len(s['frameFiles'])
 job['files']=[(mp.parent/f).resolve().as_posix() for f in s['frameFiles']]
(H/'bunk-scope.json').write_text(json.dumps(jobs,indent=2)+'\n');print('Six final-package bunk jobs / 30 source poses; original clocks exact.')

