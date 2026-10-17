from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent;S=R/'character/bill-east-interact-master-consistency-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=json.loads((P/'source-baseline.json').read_text());groups=[];metrics=[];inputs={}
def common(im):
 out=Image.new('RGBA',(352,352));out.alpha_composite(im,(68,52));return out
def bounds(mask):
 y,x=np.where(mask);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
for slot in [0,18,36]:
 before=common(Image.open(R/a['rows'][slot]['path']).convert('RGBA'));inputs[a['rows'][slot]['path']]=a['rows'][slot]['sha256'];assert sha(R/a['rows'][slot]['path'])==a['rows'][slot]['sha256']
 if slot==0:
  new=common(Image.open(P/'sources/seed-000.png').convert('RGBA'));inputs[str((P/'seed-provenance.json').relative_to(R))]=sha(P/'seed-provenance.json')
 elif (P/f'provenance-{slot:03}.json').exists():
  q=json.loads((P/f'provenance-{slot:03}.json').read_text())
  for path,h in q['frozenInputs'].items():assert sha(Path(path))==h,path
  assert sha(Path(q['savedPath']))==q['sha256'];new=Image.open(q['savedPath']).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
  for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
  inputs[str((P/f'provenance-{slot:03}.json').relative_to(R))]=sha(P/f'provenance-{slot:03}.json');inputs[str(Path(q['savedPath']).relative_to(R))]=q['sha256']
 else:continue
 aa=np.array(before)[:,:,3]>127;bb=np.array(new)[:,:,3]>127;keep=np.zeros(bb.shape,bool);keep[52:236,68:252]=True;metrics.append({'slot':slot,'beforeBounds':bounds(aa),'candidateBounds':bounds(bb),'bodyBelow115IoU':float((aa[115:]&bb[115:]).sum()/(aa[115:]|bb[115:]).sum()),'opaqueOverflow':int((bb&~keep).sum())});groups.extend([(f'{slot:03} Selected breathing',before),(f'{slot:03} New study',new)]);(P/'candidate-frames').mkdir(exist_ok=True);new.crop((68,52,252,236)).save(P/f'candidate-frames/{slot:03}.png')
master=Image.open(P/'sources/original-east-master-common.png').convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
groups.extend([('Original East master',master),('Interaction extended-arm join',common(Image.open(S/'frames/interact-east/003.png').convert('RGBA')))])
board=Image.new('RGBA',(1520,1040),(31,35,40,255));d=ImageDraw.Draw(board)
for n,(label,im) in enumerate(groups):
 x=n%4*380;y=n//4*520;d.text((x+8,y+8),label,fill='white');board.alpha_composite(im,(x+8,y+25));d.line((x+95,y+249,x+275,y+249),fill=(70,185,195));board.alpha_composite(im.crop((130,60,210,135)).resize((160,150),Image.Resampling.NEAREST),(x+95,y+365))
board.save(P/'key-pose-review.png');q={'scope':'Sparse breathing midpoint/peak study only, not complete 72-slot loop or native contact/cadence evidence. No selection or runtime changes. Original master authority; exact seed derived from identical selected idle0/interaction0 source.', 'metrics':metrics,'newIndependentGenerationUnits':len(metrics)-1,'derivedSeedCount':1,'authoredUniquePoses':len(metrics),'requiredUniquePoses':37,'sourceSlotCount':72,'sourceTimelineMs':3000,'frozenInputs':inputs,'boardSha256':sha(P/'key-pose-review.png'),'visualReview':'pending raw and key pose board','normalAdmission':False,'nativeRun':False,'completeFamily':False};(P/'review.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps({'metrics':metrics,'authoredUniquePoses':len(metrics),'requiredUniquePoses':37}))
