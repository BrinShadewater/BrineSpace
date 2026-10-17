from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
b=r/'character/james-cargo-return-bridges-v1'
m=json.loads((b/'bare-joined-manifest-v9.json').read_bytes())
m['states'][0]['frameFiles'][3]='res://character/james-cargo-return-bridges-v1/collar-v12-bare.png'
for i,f in enumerate(m['states'][0]['frameFiles']):
    if not f.startswith('res://'):m['states'][0]['frameFiles'][i]='res://character/james-cargo-return-bridges-v1/'+f
m['name']='James West collar V12 bare source trial'
m['status']='unselected_single_interior_collar_only_trial'
(b/'bare-joined-manifest-v12.json').write_text(json.dumps(m,indent=2)+'\n')
s=(p/'full_return_v6.gd').read_text().replace('bare-joined-manifest-v9.json','bare-joined-manifest-v12.json')
s=s.replace('full-return-v6','full-return-collar-v12').replace('full_return_v6','full_return_collar_v12')
s=s.replace('No full V9 return/normal selection/Continue/natural scheduling or full master acceptance.','One new bare collar interior only; helmet V9 unchanged. No normal selection/Continue/natural scheduling, paired repair or full master acceptance.')
(p/'full_return_collar_v12.gd').write_text(s)
paths=[r/k for k in json.loads((p/'full_return_v6-inputs.json').read_bytes())]
paths += [p/'full_return_collar_v12.gd',b/'bare-joined-manifest-v12.json',b/'collar-v12-bare.png',b/'package-collar-v12.gd',b/'collar-repair-v11-raw.png',b/'collar-repair-v11-prompt.txt']
(p/'full_return_collar_v12-inputs.json').write_text(json.dumps({str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print('V12 full return trial prepared; original paired head/body preserved outside collar;46inputs frozen.')
