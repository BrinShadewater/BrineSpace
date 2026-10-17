from pathlib import Path
import json,hashlib
H=Path('character/krusher-continuous-playback-v1');R=Path.cwd();expected=json.loads((H/'library.json').read_text());seen={k:set() for k in expected['states']};videoCount=0;stale=0
for name in ['playback-v11-final','playback-v11-retry','playback-v11-collar-final','playback-v11-collar-sealed']:
 folder=H/name;contract=json.loads((folder/'contract.json').read_text())
 for p in folder.glob('batch-*.json'):
  report=json.loads(p.read_text());assert p.with_suffix('.webm').exists();videoCount+=1
  for row in report['rows']:
   key=row['key']
   for i,yes in enumerate(row['seen']):
    if not yes:continue
    if contract['states'][key]['files'][i]==expected['states'][key]['files'][i]:seen[key].add(i)
    else:stale+=1
missing=[(k,i) for k,s in expected['states'].items() for i in range(len(s['files'])) if i not in seen[k]];assert not missing
for s in expected['states'].values():
 for file in s['files']:
  p=R/file.lstrip('/');assert hashlib.sha256(p.read_bytes()).hexdigest()==p.stem
q={'states':586,'frameHolds':sum(map(len,seen.values())),'missingHolds':missing,'continuousVideos':videoCount,'contextualPlans':198,'turnChains':72,'shortHoldRetry':'A 20ms torch-stow-east hold was recaptured by a bounded original-timing replay.','finalCollarReplay':'All 15 target holds in the 3 final bunk states replayed; older source observations excluded.','olderSourceObservationsExcluded':stale,'allObservedFinalSourceHashesExact':True,'visualScope':'All 586 states ran continuously and were recorded. Agent visual inspection uses chronological decoded motion witnesses plus selected live playback; this is not uninterrupted human viewing of every recording.'};(H/'continuous-coverage.json').write_text(json.dumps(q,indent=2)+'\n');print(q)
# Decode the final targeted sequence at each authored hold, preserving source order.
import av
from PIL import Image,ImageDraw
L=json.loads((H/'playback-v11-collar-sealed/contract.json').read_text());targets=[]
for j,plan in enumerate(L['plans']):
 offset=0
 for seg in plan['segments']:
  if seg['role']=='target':break
  offset+=seg['duration']
 t=offset
 for slot,duration in enumerate(L['states'][plan['key']]['durations']):targets.append(((t+duration/2)/1000,j,slot));t+=duration
images={};targets.sort();pos=0
with av.open(str(H/'playback-v11-collar-sealed/batch-000.webm')) as c:
 for frame in c.decode(video=0):
  if pos==len(targets):break
  tm=float(frame.time or 0)
  if tm<targets[pos][0]:continue
  im=frame.to_image().convert('RGBA')
  while pos<len(targets) and targets[pos][0]<=tm:
   _,j,slot=targets[pos];x=j%3*400+276;y=j//3*360+184;images[(j,slot)]=im.crop((x,y,x+112,y+120));pos+=1
board=Image.new('RGBA',(7*160,3*190),'#28343a');d=ImageDraw.Draw(board)
for j,plan in enumerate(L['plans']):
 d.text((8,j*190+2),plan['key'],fill='white')
 for slot in range(plan['targetSlots']):board.alpha_composite(images[(j,slot)].resize((140,150)),(slot*160,j*190+24))
board.save(H/'final-bunk-motion.png')
