from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
root=Path.cwd();b=root/'character/marsh-retained-gesture-material-v1';o=b/'east-return06-unselected';o.mkdir(exist_ok=True)
old=json.loads((b/'east04-unselected/manifest.json').read_text());new=json.loads((b/'east06-unselected/manifest.json').read_text())
for state in old['states']:
 state['frameFiles'][4]=new['states'][0]['frameFiles'][4]
old['scope']='Staged East04 first three whole gestures plus East06 whole return figure, exact own-idle endpoints; original900ms holds. No local anatomy patch or actual helmet behavior.'
(o/'manifest.json').write_text(json.dumps(old,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r={'sources':[{'path':(b/f/'verification.json').relative_to(root).as_posix(),'sha256':sha(b/f/'verification.json')} for f in ['east04-unselected','east06-unselected']], 'policy':'East04 poses0..2 unchanged, East06 pose3 only. Each source strip uses its one own-neutral-derived density; no per-pose scale fit. East06 full bank not preferred: new whole-source neutral width needs review vs own32. Its return pose is reviewed as an intermediate bent-arm action, not a neutral proportion authority.', 'normalAdmission':False,'fullGoalComplete':False}
board=Image.new('RGB',(1320,690),'#293b40');draw=ImageDraw.Draw(board)
rows=[('East04 prior',json.loads((b/'east04-unselected/manifest.json').read_text())['states'][0]['frameFiles']),('Mixed whole return06',old['states'][0]['frameFiles']),('Exact own idle',[old['states'][0]['frameFiles'][0]]*6)]
for row,(label,files) in enumerate(rows):
 for i,p in enumerate(files):
  src=root/p.removeprefix('res://');im=Image.open(src).convert('RGBA');board.paste(im,(i*220+18,row*230+30),im);draw.text((i*220+3,row*230+3),label+' / '+str(i),fill='white')
p=o/'return-comparison.png';board.save(p);r['board']={'path':p.relative_to(root).as_posix(),'sha256':sha(p),'actuallyInspected':False}
r['slots']=[{'path':p.removeprefix('res://'),'sha256':sha(root/p.removeprefix('res://'))} for p in old['states'][0]['frameFiles']]
(o/'selection.json').write_text(json.dumps(r,indent=2)+'\n')
print('East return-only whole-figure bank prepared; first3 gestures and idle endpoints unchanged')
