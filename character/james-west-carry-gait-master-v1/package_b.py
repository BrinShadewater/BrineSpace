from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'contact-b-inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
raw=Image.open(p/'contact-b-raw.png').convert('RGBA');assert raw.width==raw.height
local=raw.resize((88,88),Image.Resampling.LANCZOS);local.save(p/'contact-b-native-crop.png')
base=Image.open(p/'base.png').convert('RGBA');out=base.copy();rect=inputs['admissionRegion'];out.paste(local.crop((rect[0]-88,rect[1]-152,rect[2]-88,rect[3]-152)),rect[:2]);out.save(p/'contact-b.png')
a=base.copy();b=out.copy()
for im in [a,b]:im.paste((0,0,0,0),rect)
assert a.tobytes()==b.tobytes()
board=Image.new('RGBA',(1152,560),(48,59,63,255));d=ImageDraw.Draw(board)
for i,im in enumerate([base,out]):
    board.alpha_composite(im,(i*256,30));d.text((i*256+5,8),'standing base' if i==0 else 'contact B draft',fill='white')
    board.alpha_composite(im.crop((88,152,176,240)).resize((352,352),Image.Resampling.NEAREST),(i*352,205))
    for j,h in enumerate([82,54,27]):
        sz=round(256*h/148);board.alpha_composite(im.resize((sz,sz),Image.Resampling.LANCZOS),(750+j*130-sz//2,40+i*230+round(224*(1-h/148))))
board.convert('RGB').save(p/'contact-b-comparison.png')
(p/'contact-b-review.json').write_text(json.dumps({'protectedOutsideExact':True,'protectedOutsidePixels':65536-(rect[2]-rect[0])*(rect[3]-rect[1]),'nativeAlpha128Bounds':out.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'sourceAcceptance':False,'selected':False,'visualReviewPending':True,'scope':'One independently generated lower-body contact source; no complete gait/timing/native/cadence acceptance.','rawSha256':hashlib.sha256((p/'contact-b-raw.png').read_bytes()).hexdigest()},indent=2)+'\n',encoding='utf-8')
print('Contact A packaged without fit/translation/regrade; outside lower-body exact.')
