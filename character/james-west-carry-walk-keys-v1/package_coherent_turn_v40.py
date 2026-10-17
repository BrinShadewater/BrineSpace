from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'coherent-turn-v40';d=json.loads((out/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(r/f)==v for f,v in d['preCallSha256'].items())
base=Image.open(r/d['base']).convert('RGBA');raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
native=raw.resize((256,256),Image.Resampling.LANCZOS);native.save(out/'normalized.png');rect=d['admission'];candidate=base.copy();candidate.paste(native.crop(rect),rect[:2]);candidate.save(out/'bare-candidate.png')
cap=Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA');helmet=candidate.copy();helmet.paste(cap.crop((102,62,155,110)),(102,62));helmet.save(out/'helmet-candidate.png')
mask=np.ones((256,256),bool);mask[104:228,88:166]=False
assert np.array_equal(np.array(base)[mask],np.array(candidate)[mask]);assert np.array_equal(np.array(base)[:104],np.array(candidate)[:104]);assert np.array_equal(np.array(candidate)[110:],np.array(helmet)[110:])
files=[r/d['base'],out/'bare-candidate.png',p/'whole-belt-admission-v35/bare-candidate.png',p/'master-head-review-v16/bare-000.png'];labels=['standing','coherent turn9 study','V35 next study','walk0']
for kind,box,scale in [('whole',(0,0,256,256),1),('body',(80,96,176,240),2)]:
    w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(4*w,2*(h+25)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,f in enumerate(files):
            im=Image.open(f).convert('RGBA')
            if mode=='helmet':im.paste(cap.crop((102,62,155,110)),(102,62))
            board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(col*w,row*(h+25)+25));draw.text((col*w+3,row*(h+25)+5),mode+' '+labels[col],fill='white')
    board.convert('RGB').save(out/('comparison-'+kind+'.png'))
(out/'review.json').write_text(json.dumps(dict(outsideAdmissionExact=int(mask.sum()),faceAbove104Exact=True,registeredHelmetCapExact=True,pairedBodyBelow110Exact=True,sourceAcceptance=False,normalChanged=False,visualReviewPending=True,rawSize=list(raw.size)),indent=2)+'\n')
print('V40 exact face/helmet and55864 outside body pixels protected; two paired comparison boards saved.')
