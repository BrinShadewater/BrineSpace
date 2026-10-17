from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in d['preCallSha256'].items())
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((80,80),Image.Resampling.LANCZOS)
ims=[Image.open(r/k).convert('RGBA') for k in d['sources']]
original=ims[1];trial=original.copy();box=(104,64,162,134)
trial.paste(crop.crop((8,8,66,78)),(104,64))
protected=0
for y in range(256):
    for x in range(256):
        if not(box[0]<=x<box[2] and box[1]<=y<box[3]):
            assert trial.getpixel((x,y))==original.getpixel((x,y));protected+=1
assert protected==61476
trial.save(p/'candidate.png')
review=Image.new('RGB',(4*320,600),'#303b40');draw=ImageDraw.Draw(review)
for i,(name,im) in enumerate(zip(['entry','original middle','new midpoint','exit'],[ims[0],ims[1],trial,ims[2]])):
    draw.text((i*320+8,8),name,fill='white');review.paste(im,(i*320+32,30),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST)
    review.paste(upper,(i*320,280),upper)
review.save(p/'comparison.png')
report={'selected':False,'visualReviewPending':True,'sourceSize':raw.size,'uniformScale':80/raw.width,'admittedRect':box,'protectedPixels':protected,'sourceSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'candidateSha256':hashlib.sha256((p/'candidate.png').read_bytes()).hexdigest(),'scope':'One bare midpoint only; no timing bank, helmet pairing or native admission.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
