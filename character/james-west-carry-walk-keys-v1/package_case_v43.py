from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'case-contact-v43';d=json.loads((out/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(r/f)==v for f,v in d['preCallSha256'].items())
base=Image.open(r/d['base']).convert('RGBA');raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
native=raw.resize((64,64),Image.Resampling.LANCZOS);native.save(out/'normalized.png');rect=d['admission'];crop=d['crop'];candidate=base.copy();candidate.paste(native.crop((rect[0]-crop[0],rect[1]-crop[1],rect[2]-crop[0],rect[3]-crop[1])),rect[:2]);candidate.save(out/'bare-candidate.png')
cap=Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA');helmet=candidate.copy();helmet.paste(cap.crop((102,62,155,110)),(102,62));helmet.save(out/'helmet-candidate.png')
mask=np.ones((256,256),bool);mask[123:149,94:134]=False;assert np.array_equal(np.array(base)[mask],np.array(candidate)[mask]);assert np.array_equal(np.array(candidate)[110:],np.array(helmet)[110:])
fs=[r/'character/james-carry-headcaps-v1/frames/004.png',p/'coherent-turn-v40/bare-candidate.png',r/d['base'],out/'bare-candidate.png',p/'master-head-review-v16/bare-000.png'];labels=['standing authority','turn intermediate','before case repair','after case repair','walk0']
for kind,box,scale in [('whole',(0,0,256,256),1),('case',(88,112,152,160),4)]:
    w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(5*w,2*(h+25)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,f in enumerate(fs):
            im=Image.open(f).convert('RGBA')
            if mode=='helmet':im.paste(cap.crop((102,62,155,110)),(102,62))
            board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(col*w,row*(h+25)+25));draw.text((col*w+3,row*(h+25)+5),mode+' '+labels[col],fill='white')
    board.convert('RGB').save(out/('comparison-'+kind+'.png'))
(out/'review.json').write_text(json.dumps(dict(outsideCaseAdmissionExact=int(mask.sum()),originalHeadLegsWristOutsideAdmissionExact=True,pairedBodyBelow110Exact=True,registeredHelmetCapExact=True,sourceAcceptance=False,normalChanged=False,visualReviewPending=True,rawSize=list(raw.size)),indent=2)+'\n')
print('V43 packaged with64496 outside case/grip pixels exact.')
