from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
original=Image.open(r/inputs['sources']['target']).convert('RGBA')
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.width==raw.height
small=raw.resize((64,64),Image.Resampling.LANCZOS)
# Generated crop's cap was placed two pixels above requested framing. Register
# this equipment cap alone to the measured neighbor crown. Face/collar/body
# never move, resize or receive generated pixels.
layer=Image.new('RGBA',(256,256));layer.alpha_composite(small,(96,58))
cap=(102,64,152,84);candidate=original.copy();candidate.paste(layer.crop(cap),(cap[0],cap[1]))
candidate.save(p/'candidate-cap.png')
oa=np.asarray(original);ca=np.asarray(candidate);protected=np.ones((256,256),bool);protected[64:84,102:152]=False
assert np.array_equal(oa[protected],ca[protected])
def crown(im):
    yy,xx=np.where(np.asarray(im)[:,:,3]>=32);return int(224-yy.min())
board=Image.new('RGB',(5*384,650),'#303b40');d=ImageDraw.Draw(board)
sources=[('previous',Image.open(r/inputs['sources']['previous']).convert('RGBA')),('original dip',original),('cap candidate',candidate),('next',Image.open(r/inputs['sources']['next']).convert('RGBA'))]
for i,(name,im) in enumerate(sources):
    bg=Image.new('RGBA',(256,256),'#303b40');bg.alpha_composite(im)
    board.paste(bg.convert('RGB').crop((96,56,160,120)).resize((384,384),Image.Resampling.NEAREST),(i*384,20))
    board.paste(bg.convert('RGB'),(i*384,394));d.text((i*384+4,4),f'{name} crown{crown(im)}',fill='white')
board.save(p/'cap-review.png')
report={'selected':False,'visualReviewPending':True,'rawSize':list(raw.size),
 'uniformWholeCropScale':64/raw.width,'equipmentCapAttachment':[96,58],
 'capAdmissionRect':list(cap),'protectedPixelsExact':int(protected.sum()),
 'protectedFaceCollarBodyFeet':True,'bodyTranslationOrScale':False,'gradeApplied':False,
 'originalCrownDiagnostic':crown(original),'candidateCrownDiagnostic':crown(candidate),
 'sourceHash':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),
 'scope':'Authored cap source registration trial only. Requested raw framing overshot by2px; cap attachment compensated explicitly. Canonical face/collar/body protected. Numeric crown success is not shell contour/material/temporal acceptance. No native actor/paired bank/normal selection.'}
(p/'cap-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
