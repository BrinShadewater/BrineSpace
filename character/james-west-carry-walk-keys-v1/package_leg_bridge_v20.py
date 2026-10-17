from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np, hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'leg-bridge-v20'
inputs=json.loads((out/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preCallSha256'].items())
base=Image.open(r/inputs['baseFile']).convert('RGBA');raw=Image.open(out/'raw.png').convert('RGBA')
assert raw.width==raw.height
native=raw.resize((144,144),Image.Resampling.LANCZOS);native.save(out/'native-crop.png')
candidate=base.copy();crop=inputs['crop'];rect=inputs['admissionRegion']
candidate.paste(native.crop((rect[0]-crop[0],rect[1]-crop[1],rect[2]-crop[0],rect[3]-crop[1])),rect[:2]);candidate.save(out/'candidate.png')
a=np.array(base);b=np.array(candidate);mask=np.ones((256,256),bool);mask[140:228,88:166]=False
assert mask.sum()==58672 and np.array_equal(a[mask],b[mask])
review=dict(rawSha256=hashlib.sha256((out/'raw.png').read_bytes()).hexdigest(),protectedPixels58672Exact=True,
    sourceAcceptance=False,selected=False,visualReviewPending=True,admissionRegion=rect,
    scope='Generated lower body only; original standing upper body/head/case exact. No original leg-pixel preservation claim, fitting, grading or mirroring.')
(out/'review.json').write_text(json.dumps(review,indent=2)+'\n')
sources=[base,candidate,Image.open(r/inputs['donorSource']).convert('RGBA'),Image.open(p/'master-head-review-v16/bare-000.png').convert('RGBA')]
board=Image.new('RGB',(768,314),(47,58,62));draw=ImageDraw.Draw(board)
for i,(im,label) in enumerate(zip(sources,['standing master','lower-body trial','actual pose guide','walking endpoint'])):
    draw.text((i*192+4,4),label,fill='white');tile=im.crop((80,96,176,240)).resize((192,288),Image.Resampling.NEAREST);board.paste(tile,(i*192,26),tile)
board.save(out/'comparison.png')
print('Lower-body candidate packaged:58672 protected pixels exact; original upper body/head/case unchanged.')
