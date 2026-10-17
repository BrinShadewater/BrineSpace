from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-cargo-source-v338'
d=json.loads((o/'inputs.json').read_bytes());assert hashlib.sha256((r/d['source']).read_bytes()).hexdigest()==d['sourceSha256'];assert hashlib.sha256((o/'actual-submitted-prompt.txt').read_bytes()).hexdigest()==d['promptSha256'];assert hashlib.sha256((o/'target.png').read_bytes()).hexdigest()==d['targetSha256']
raw=Image.open(o/'raw.png').convert('RGBA');assert raw.width==raw.height
candidate=raw.resize((300,300),Image.Resampling.NEAREST);candidate.save(o/'fixed-source-candidate.png')
control=Image.open(o/'target.png').convert('RGBA').resize((300,300),Image.Resampling.NEAREST)
def bound(im):
 ys,xs=np.where(np.asarray(im)[:,:,3]>128);return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
board=Image.new('RGB',(900,1000),(48,59,64));draw=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('Original authoring source',control),('Candidate same source ruler',candidate)]):
 x=col*300;draw.text((x+5,5),label,fill='white');board.paste(im,(x,25),im)
 scale=d['sourceScale'];mapped=im.resize((round(300*scale),round(300*scale)),Image.Resampling.LANCZOS)
 pos=(round(d['oldRegisteredPosition'][0]-d['sourceOffset'][0]*scale),round(d['oldRegisteredPosition'][1]-d['sourceOffset'][1]*scale))
 native=Image.new('RGBA',(256,276));native.alpha_composite(mapped,pos)
 if col==1:native.save(o/'fixed-registration-candidate.png')
 for j,h in enumerate([148,82,54,27]):
  image=native.resize((round(256*h/148),round(276*h/148)),Image.Resampling.LANCZOS)
  y=350+[0,280,435,535][j];board.paste(image,(x+(300-image.width)//2,y),image);draw.text((x+4,y+5),f'H{h}',fill='white')
selected=r/'character/james-water-cargo-west-v1/frames/bare/swim-carry/000.png';im=Image.open(selected).convert('RGBA');draw.text((605,5),'Selected game frame',fill='white');board.paste(im,(622,350),im)
# Separate source-density display above from actual native scale below.
board.save(o/'comparison.png')
report=dict(rawSize=list(raw.size),sourceBounds=bound(control),candidateBounds=bound(candidate),fixedScale=d['sourceScale'],sourceOffset=d['sourceOffset'],registeredPosition=pos,normalChanged=False,sourceAcceptance=False,disposition='rejected_master_detail_and_protected_identity_drift',findings=['Higher-density tightly framed reference improves gross composition versus337; material still uses broad padded bands instead of original fine curved quilting.','Face/hair/shoulder emblem and case hardware redrawn; exact protected identity is unproven.','Do not assert missing belt wrench from ambiguous hip device/ring silhouette alone.337 stronger missing-wrench claim is not established by source evidence.'],next='Stop repeating imagegen-only same-pose attempts. Review original master detail against source-authoring anatomy and identify a genuinely more constrained editing route; proceed with remaining hazard/death and game-phase evidence meanwhile.')
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['rawSize','sourceBounds','candidateBounds','registeredPosition']}))
