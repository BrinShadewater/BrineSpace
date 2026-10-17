from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'belt-contact-v34'
d=json.loads((out/'inputs.json').read_bytes());assert all(hashlib.sha256((r/f).read_bytes()).hexdigest()==v for f,v in d['preCallSha256'].items())
base=Image.open(r/d['originalLegBase']).convert('RGBA');upper=Image.open(r/d['upperRaw']).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
candidate=base.copy();rect=d['upperAdmission'];candidate.paste(upper.crop(rect),rect[:2]);before_gear=candidate.copy()
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
local=raw.resize((48,48),Image.Resampling.LANCZOS);local.save(out/'native-crop.png')
gear=d['gearAdmission'];crop=d['crop'];candidate.paste(local.crop((gear[0]-crop[0],gear[1]-crop[1],gear[2]-crop[0],gear[3]-crop[1])),gear[:2]);candidate.save(out/'candidate.png')
mask=np.ones((256,256),bool);mask[104:159,88:166]=False
assert mask.sum()==61246 and np.array_equal(np.array(base)[mask],np.array(candidate)[mask])
gmask=np.ones((256,256),bool);gmask[141:159,124:137]=False
assert gmask.sum()==65302 and np.array_equal(np.array(before_gear)[gmask],np.array(candidate)[gmask])
assert np.array_equal(np.array(base)[:104],np.array(candidate)[:104]) and np.array_equal(np.array(base)[159:],np.array(candidate)[159:])
files=[r/'character/james-carry-headcaps-v1/frames/004.png',r/d['originalLegBase'],out/'candidate.png',p/'master-head-review-v16/bare-000.png']
helmet=Image.open(r/'character/james-carry-authored-helmet-v1/frames/004.png').convert('RGBA')
for kind,box,scale in [('whole',(0,0,256,256),1),('body',(80,96,176,240),2)]:
    w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(4*w,2*(h+26)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,mode in enumerate(['bare','helmet']):
        for col,f in enumerate(files):
            im=Image.open(f).convert('RGBA')
            if mode=='helmet':im.paste(helmet.crop((102,62,155,110)),(102,62))
            if col==2:im.save(out/(mode+'-candidate.png'))
            board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(col*w,row*(h+26)+26))
            draw.text((col*w+3,row*(h+26)+7),mode+' '+['standing','leg study','belt-fixed upper','walk0'][col],fill='white')
    board.convert('RGB').save(out/('chain-'+kind+'.png'))
(out/'review.json').write_text(json.dumps(dict(outsideUpper61246Exact=True,outsideGear65302Exact=True,faceAbove104Exact=True,kneesShinsBelow159Exact=True,sourceAcceptance=False,visualReviewPending=True,normalChanged=False,scope='V33 authored upper pose admitted only104..159 on V20 base; V34 generated belt repair only13x18. All face/knee/shin pixels protected. Helmet preview reuses original registered cap. No finite/native/normal adoption or continuous-motion acceptance.'),indent=2)+'\n')
print('V34 packaged: face/knees exact,61246 upper-body and65302 local gear protections pass.')
