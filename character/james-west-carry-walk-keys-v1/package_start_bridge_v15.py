from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,sys,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'start-bridge-v15';name=sys.argv[1]
inputs=json.loads((out/f'{name}-inputs.json').read_bytes());assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preCallSha256'].items())
raw=Image.open(out/f'{name}-raw.png').convert('RGBA');assert raw.width==raw.height
crop=inputs['crop'];rect=inputs['admissionRegion'];native=raw.resize((144,144),Image.Resampling.LANCZOS);native.save(out/f'{name}-native-crop.png')
base=Image.open(r/inputs['baseFile']).convert('RGBA');candidate=base.copy();candidate.paste(native.crop((24,8,102,132)),(88,104));candidate.save(out/f'{name}.png')
a=np.array(base);b=np.array(candidate);mask=np.ones((256,256),bool);mask[104:228,88:166]=False
assert mask.sum()==55864 and np.array_equal(a[mask],b[mask])
board=Image.new('RGBA',(768,410),(48,59,63,255));d=ImageDraw.Draw(board)
for i,im in enumerate((base,candidate)):
 board.alpha_composite(im.crop(crop).resize((384,384),Image.Resampling.NEAREST),(i*384,26));d.text((i*384+5,7),'standing endpoint' if not i else name,fill='white')
board.convert('RGB').save(out/f'{name}-comparison.png')
(out/f'{name}-review.json').write_text(json.dumps({'protectedOutsidePixels':55864,'protectedOutsideExact':True,'admissionRegion':rect,'boundsAlpha128':candidate.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'rawSha256':hashlib.sha256((out/f'{name}-raw.png').read_bytes()).hexdigest(),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Native144 crop once downsampled and admitted at fixed coordinates. No fit/grade/warp. Full body stance and planted foot contact unaccepted.'},indent=2)+'\n')
print(name+': protected55864 outside pixels exact; no body fit.')
