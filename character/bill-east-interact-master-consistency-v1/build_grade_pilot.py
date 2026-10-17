from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,ast,subprocess
R=Path.cwd();P=R/'character/bill-east-interact-master-consistency-v1';B=P/'grade-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();q=json.loads((B/'provenance.json').read_text())
for path,h in q['frozenInputs'].items():assert sha(Path(path))==h
raw=Image.open(B/'raw.png').convert('RGBA');assert raw.width==raw.height
new=raw.resize((352,352),Image.Resampling.LANCZOS);old=Image.open(B/'target.png').convert('RGBA').resize((352,352),Image.Resampling.NEAREST);idle=Image.open(B/'idle-reference.png').convert('RGBA').resize((352,352),Image.Resampling.NEAREST);master=Image.open(P/'sources/original-east-master-common.png').convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
def bounds(im):
 y,x=np.where(np.array(im)[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
a=np.array(old)[:,:,3]>127;b=np.array(new)[:,:,3]>127;keep=np.zeros(b.shape,bool);keep[52:236,68:252]=True
metrics={'beforeBounds':bounds(old),'candidateBounds':bounds(new),'bodyBelow115IoU':float((a[115:]&b[115:]).sum()/(a[115:]|b[115:]).sum()),'opaqueOverflow':int((b&~keep).sum())}
new.crop((68,52,252,236)).save(B/'candidate-003.png')
board=Image.new('RGBA',(1520,1020),(31,35,40,255));d=ImageDraw.Draw(board)
for n,(label,im) in enumerate([('Previous study',old),('Restrained grade pilot',new),('Current idle',idle),('Original East master',master)]):
 x=380*n;d.text((x+12,12),label,fill='white');board.alpha_composite(im,(x+8,30));d.line((x+95,254,x+275,254),fill=(70,185,195));board.alpha_composite(im.crop((130,60,210,135)).resize((240,225),Image.Resampling.NEAREST),(x+70,300))
 for row,h in enumerate([82,54,27]):
  factor=h/148;small=im.resize((round(352*factor),round(352*factor)),Image.Resampling.LANCZOS);board.alpha_composite(small,(x+round(190-160*factor),700+row*95-round(224*factor)));d.text((x+12,700+row*95),f'H{h}',fill='white')
board.save(B/'comparison.png');metrics.update(rawSha256=sha(B/'raw.png'),comparisonSha256=sha(B/'comparison.png'),visualReview='pending board',normalAdmission=False,nativeRun=False)
(B/'review.json').write_text(json.dumps(metrics,indent=2)+'\n')
for p in [P/'prepare_grade_pilot.py',P/'save_grade_pilot.py',P/'record_native_milestone.py']:ast.parse(p.read_text())
print(json.dumps(metrics))

