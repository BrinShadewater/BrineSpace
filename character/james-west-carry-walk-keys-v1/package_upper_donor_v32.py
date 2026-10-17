from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'upper-donor-v32'
inputs=json.loads((out/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in inputs['preCallSha256'].items())
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
native=raw.resize((144,144),Image.Resampling.LANCZOS);native.save(out/'native-crop.png')
base=Image.open(r/inputs['baseFile']).convert('RGBA');candidate=base.copy();rect=inputs['admissionRegion'];crop=inputs['crop']
candidate.paste(native.crop((rect[0]-crop[0],rect[1]-crop[1],rect[2]-crop[0],rect[3]-crop[1])),rect[:2]);candidate.save(out/'candidate.png')
mask=np.ones((256,256),bool);mask[110:169,88:166]=False
assert mask.sum()==60934 and np.array_equal(np.array(base)[mask],np.array(candidate)[mask])
(out/'review.json').write_text(json.dumps(dict(rawSha256=hashlib.sha256((out/'raw.png').read_bytes()).hexdigest(),outside60934Exact=True,visualReviewPending=True,
    sourceAcceptance=False,selected=False,scope='Upper-body admission only; exact V20 head/collar and legs outside. No fit,grade,warp,mirror or runtime adoption.'),indent=2)+'\n')
files=[r/'character/james-carry-headcaps-v1/frames/004.png',r/inputs['baseFile'],out/'candidate.png',p/'master-head-review-v16/bare-000.png']
head=r/'character/james-carry-authored-helmet-v1/frames/004.png';helmet=Image.open(head).convert('RGBA');groups=[]
for mode in ('bare','helmet'):
    bank=[]
    for f in files:
        im=Image.open(f).convert('RGBA')
        if mode=='helmet':im.paste(helmet.crop((102,62,155,110)),(102,62))
        bank.append(im)
    groups.append(bank)
for kind,box,scale in [('whole',(0,0,256,256),1),('body',(80,96,176,240),2)]:
    w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(4*w,2*(h+26)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,bank in enumerate(groups):
        for i,im in enumerate(bank):
            board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(i*w,row*(h+26)+26))
            draw.text((i*w+3,row*(h+26)+7),('helmet ' if row else 'bare ')+['standing','leg study','donor upper','walk0'][i],fill='white')
    board.convert('RGB').save(out/f'chain-{kind}.png')
(out/'chain-review.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files+[head]},
    visualReviewPending=True,sourceAcceptance=False,selected=False,scope='Four paired source poses only. No finite timing, native run, continuous visual acceptance or normal runtime change.'),indent=2)+'\n')
print('Actual-donor upper trial packaged;60934 outside pixels exact to V20 source.')
