from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, numpy as np
p=Path(__file__).resolve().parent; r=p.parents[1]; out=p/'stance-inbetween-v38'
d=json.loads((out/'inputs.json').read_bytes())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(r/f)==v for f,v in d['preCallSha256'].items())
base=Image.open(r/d['base']).convert('RGBA'); raw=Image.open(out/'raw.png').convert('RGBA')
assert raw.width==raw.height
normalized=raw.resize((256,256),Image.Resampling.LANCZOS); normalized.save(out/'normalized.png')
rect=d['admission']; candidate=base.copy(); candidate.paste(normalized.crop(rect),rect[:2]);candidate.save(out/'bare-candidate.png')
helmet=Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA')
cap=(102,62,155,110); equipped=candidate.copy(); equipped.paste(helmet.crop(cap),cap[:2]);equipped.save(out/'helmet-candidate.png')
a=np.array(base); b=np.array(candidate);mask=np.ones((256,256),bool);mask[147:228,88:166]=False
assert np.array_equal(a[mask],b[mask]); assert np.array_equal(a[:147],b[:147])
assert np.array_equal(np.array(equipped)[110:],b[110:])
files=[r/d['base'],out/'bare-candidate.png',p/'leg-bridge-v20/candidate.png',p/'master-head-review-v16/bare-000.png']
for kind,box,scale in [('whole',(0,0,256,256),1),('legs',(88,140,166,230),3)]:
    w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(w*4,2*(h+25)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,f in enumerate(files):
            im=Image.open(f).convert('RGBA')
            if mode=='helmet':im.paste(helmet.crop(cap),cap[:2])
            board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(col*w,row*(h+25)+25))
            draw.text((col*w+3,row*(h+25)+5),mode+' '+['standing','new weight shift','next leg pose','walk0'][col],fill='white')
    board.convert('RGB').save(out/('comparison-'+kind+'.png'))
report=dict(outsideAdmissionExact=int(mask.sum()),upperHeadCaseAbove147Exact=True,pairedBodyBelow110Exact=True,changedLegPixels=int(np.any(a!=b,axis=2).sum()),rawSize=list(raw.size),sourceAcceptance=False,normalChanged=False,visualReviewPending=True,fullGoalComplete=False,outputSha256={f.name:sha(f) for f in out.glob('*.png')})
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['outsideAdmissionExact','upperHeadCaseAbove147Exact','changedLegPixels','rawSize','normalChanged']}))
