from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'donor-bridge-v19';name=sys.argv[1]
inputs=json.loads((out/f'{name}-inputs.json').read_bytes());assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preCallSha256'].items())
raw=Image.open(out/f'{name}-raw.png').convert('RGBA');assert raw.width==raw.height;native=raw.resize((144,144),Image.Resampling.LANCZOS);native.save(out/f'{name}-native-crop.png')
base=Image.open(r/inputs['baseFile']).convert('RGBA');candidate=base.copy();candidate.paste(native.crop((24,8,102,132)),(88,104));candidate.paste(Image.open(r/inputs['headSource']).convert('RGBA').crop((102,62,155,110)),(102,62));candidate.save(out/f'{name}.png')
mask=np.ones((256,256),bool);mask[104:228,88:166]=False;mask[62:110,102:155]=True
assert mask.sum()==56182 and np.array_equal(np.array(base)[mask],np.array(candidate)[mask])
board=Image.new('RGBA',(768,410),(48,59,63,255));d=ImageDraw.Draw(board)
for i,im in enumerate((base,candidate)):
 board.alpha_composite(im.crop(inputs['crop']).resize((384,384),Image.Resampling.NEAREST),(i*384,26));d.text((i*384+4,7),'actual pose donor' if not i else name+' master repair',fill='white')
board.convert('RGB').save(out/f'{name}-comparison.png')
(out/f'{name}-review.json').write_text(json.dumps({'rawSha256':hashlib.sha256((out/f'{name}-raw.png').read_bytes()).hexdigest(),'outsideBodyAndRestoredHead56182Exact':True,'exactHeadRegion':[102,62,155,110],'alpha128Bounds':candidate.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'One actual pose-donor master repair, native144 square downsampled once. Head/collar exact; body stance/anatomy/case/foot contacts require visual review.'},indent=2)+'\n')
print(name+': outside56182 exact, selected head/collar restored, no fit/grade/warp.')
