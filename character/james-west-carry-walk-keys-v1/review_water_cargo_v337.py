from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-cargo-master-v337'
data=json.loads((o/'inputs.json').read_bytes())
for ref in data['inputs']:
 assert hashlib.sha256((r/ref['source']).read_bytes()).hexdigest()==ref['sourceSha256']
 if 'referenceSha256' in ref:assert hashlib.sha256((o/ref['role']).read_bytes()).hexdigest()==ref['referenceSha256']
assert hashlib.sha256((o/'actual-submitted-prompt.txt').read_bytes()).hexdigest()==data['actualSubmittedPromptSha256']
raw=Image.open(o/'raw.png').convert('RGBA');assert raw.width==raw.height
candidate=raw.resize((320,320),Image.Resampling.NEAREST);candidate.save(o/'fixed-canvas-candidate.png')
target=Image.open(o/'target.png').convert('RGBA').resize((320,320),Image.Resampling.NEAREST)
ordinary=Image.open(o/'ordinary-swim-reference.png').convert('RGBA').resize((320,320),Image.Resampling.NEAREST)
def bounds(im):
 mask=np.asarray(im)[:,:,3]>128;ys,xs=np.where(mask);return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
metrics={name:bounds(im) for name,im in [('selectedCargo',target),('candidate',candidate),('ordinarySwim',ordinary)]}
board=Image.new('RGB',(960,670),(48,59,64));draw=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('Selected cargo',target),('Rejected edit',candidate),('Ordinary swim',ordinary)]):
 draw.text((col*320+8,8),label,fill='white');board.paste(im,(col*320,30),im)
 for j,height in enumerate([82,54,27]):
  resized=im.resize((round(320*height/148),round(320*height/148)),Image.Resampling.LANCZOS)
  y=350+j*105;board.paste(resized,(col*320+(320-resized.width)//2,y),resized)
  draw.text((col*320+4,y+5),f'H{height}',fill='white')
board.save(o/'comparison.png')
report=dict(mode='builtin image_gen edit',generatedSource='exec-3bd5cce1-775c-49dc-94f1-a8ce7276a059.png',rawSize=list(raw.size),squareNormalization=[320,320],normalization='Whole square only, nearest; no bbox scale/translation/grade alteration.',bounds=metrics,disposition='rejected_scale_and_equipment_drift_before_native',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Quilt fabric refinement improved versus coarse input, but body/case enlarged and shifted on unchanged square canvas.','Belt wrench visible in selected cargo source is not retained in candidate; hip equipment redesigned.','No candidate fitting or pixel surgery used to rescue the failed invariants.'],next='Use high-density authored cargo source when available and an explicit fixed composition reference; require case/head/tool positions before extending keys. No identical prompt-only retry.')
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(metrics))
