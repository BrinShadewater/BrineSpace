"""Package whole transparent output without fitting; compare selected family."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((P/'generation-provenance-v1.json').read_text())
for path,digest in q['frozenInputs'].items():assert sha(Path(path))==digest,path
for r in q['references']:assert sha(Path(r['path']))==r['sha256']
assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
original=Image.open(q['referenceSource']).convert('RGBA').crop(q['referenceCrop'])
original=original.resize(q['referenceResampledSize'],Image.Resampling.BICUBIC)
support=Image.new('RGBA',(1408,1408));support.alpha_composite(original,q['referenceTranslation'])
assert support.tobytes()==Image.open(q['references'][1]['path']).convert('RGBA').tobytes()
target=Image.new('RGBA',(352,352));target.alpha_composite(Image.open(q['source']).convert('RGBA'),q['targetTranslation'])
assert target.resize((1408,1408),Image.Resampling.NEAREST).tobytes()==Image.open(q['references'][0]['path']).convert('RGBA').tobytes()
raw=Image.open(q['savedPath']).convert('RGBA');assert raw.width==raw.height
candidate=raw.resize((352,352),Image.Resampling.LANCZOS)
candidate.crop(q['returnCrop']).save(P/'interact-003-candidate.png')
mask=np.asarray(candidate)[:,:,3]>127;before=np.asarray(target)[:,:,3]>127
def bounds(a):
 y,x=np.where(a);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
keep=np.zeros(mask.shape,bool);x,y,r,b=q['returnCrop'];keep[y:b,x:r]=True
metrics={'beforeBounds':bounds(before),'candidateBounds':bounds(mask),'bodyBelow115IoU':float((before[115:]&mask[115:]).sum()/(before[115:]|mask[115:]).sum()),'opaquePixelsOutsideOriginalCanvas':int((mask&~keep).sum()),'uniformWholeCanvasScale':352/raw.width}
idle=Image.open(ROOT/'character/crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png').convert('RGBA');idleCanvas=Image.new('RGBA',(352,352));idleCanvas.alpha_composite(idle,(68,52))
master=support.resize((352,352),Image.Resampling.LANCZOS)
board=Image.new('RGBA',(1520,750),(31,35,40,255));d=ImageDraw.Draw(board)
for n,(label,im) in enumerate([('Selected interaction 003',target),('Candidate / full raw canvas',candidate),('Original East master',master),('Selected idle',idleCanvas)]):
 x=n*380;d.text((x+8,8),label,fill='white');board.alpha_composite(im,(x+8,32));d.line((x+90,256,x+275,256),fill=(70,185,195))
 board.alpha_composite(im.crop((130,60,210,135)).resize((240,225),Image.Resampling.NEAREST),(x+65,420))
board.save(P/'master-idle-review.png')
family=Image.new('RGBA',(2280,1040),(31,35,40,255));fd=ImageDraw.Draw(family)
familyInputs={}
for row in range(2):
 for n in range(6):
  source=ROOT/f'character/bill-bare-east-selected-v1/frames/interact-east/{n:03}.png';familyInputs[str(source)]=sha(source)
  im=Image.new('RGBA',(352,352));im.alpha_composite(Image.open(source).convert('RGBA'),(68,52))
  if row==1 and n==3:im=candidate
  x=n*380;y=row*520;fd.text((x+8,y+8),f'{n:03} | '+('Selected' if row==0 else 'Single-pose study'),fill='white');family.alpha_composite(im,(x+8,y+30))
  family.alpha_composite(im.crop((130,60,210,135)).resize((160,150),Image.Resampling.NEAREST),(x+90,y+365))
family.save(P/'interaction-family-review.png')
report={'metrics':metrics,'familyInputs':familyInputs,'sourceReceiptSha256':sha(P/'generation-provenance-v1.json'),'visualReview':'pending','normalAdmission':False,'nativeRun':False,'fullVisualAcceptance':False,'scope':'Whole canvas uniform normalization only; no anatomy fit, grade, source splicing or preferred family replacement. Neighbor row changes only003 for diagnostic study, not a finished six-pose candidate.'}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics))
