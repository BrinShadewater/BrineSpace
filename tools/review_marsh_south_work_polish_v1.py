"""Whole-canvas pilot packaging and registered diagnostic comparisons; no artwork fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-south-work-polish-v1';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
request=json.loads((OUT/'request-000.json').read_text())
for e in request['references']:assert h(Path(e['path']))==e['sha256']
for e in request['frozenSelected']:assert h(ROOT/e['path'])==e['sha256']
old=Image.open(ROOT/'character/marsh-master-repair-v1/frames/repair-south/000.png').convert('RGBA')
raw=Image.open(OUT/'pilot-000.raw.png').convert('RGBA');assert raw.width==raw.height and raw.width>=184
new=raw.resize((184,184),Image.Resampling.LANCZOS);new.save(OUT/'pilot-000.png')
idle=Image.open(ROOT/'character/marsh-south-idle-material-v1/candidate-01/000.png').convert('RGBA')
bounds=lambda im:Image.fromarray((np.array(im)[:,:,3]>=128).astype('uint8')*255).getbbox()
a,b=bounds(old),bounds(new)
report={'requestSha256':h(OUT/'request-000.json'),'rawSha256':h(OUT/'pilot-000.raw.png'),'rawCanvas':list(raw.size),'candidateSha256':h(OUT/'pilot-000.png'),'oldOpaqueBounds':a,'candidateOpaqueBounds':b,'crownDelta':b[1]-a[1],'soleDelta':b[3]-a[3],'heightRatio':(b[3]-b[1])/(a[3]-a[1]),'method':'Single whole-canvas uniform184/rawwidth resampling preserving generated alpha, original pivot92/172 and standingHeight148. No alpha stencil, regional patch, grade, translation, bound fitting or anatomy correction.','normalAdmission':False,'visualReviewed':False}
board=Image.new('RGB',(1104,620),'#293b40');draw=ImageDraw.Draw(board)
for col,(name,im) in enumerate([('Selected repair',old),('Whole-pose pilot',new),('Selected idle',idle)]):
 board.paste(im.resize((368,368),Image.Resampling.NEAREST),(col*368,26),im.resize((368,368),Image.Resampling.NEAREST));draw.text((col*368+8,8),name,fill='white')
 board.paste(im,(col*368,422),im)
board.save(OUT/'pilot-000-joins.png');report['boardSha256']=h(OUT/'pilot-000-joins.png')
(OUT/'pilot-000-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
