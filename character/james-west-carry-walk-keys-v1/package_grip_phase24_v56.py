from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'case-grip-phase24-v56';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((80,80),Image.Resampling.LANCZOS);crop.save(out/'native-generated-crop.png')
box=(90,118,146,155);local=(box[0]-80,box[1]-104,box[2]-80,box[3]-104);results={}
for mode in ['bare','helmet']:
    src=Image.open(p/'master-material-phase24-v52'/(mode+'-head-protected.png')).convert('RGBA');im=src.copy();im.paste(crop.crop(local),box[:2]);im.save(out/(mode+'-candidate.png'));a=np.asarray(im);b=np.asarray(src);mask=np.ones((256,256),dtype=bool);mask[box[1]:box[3],box[0]:box[2]]=False
    assert np.array_equal(a[mask],b[mask]);assert int(mask.sum())==63464
    results[mode]=im
assert np.array_equal(np.asarray(results['bare'])[110:],np.asarray(results['helmet'])[110:])
whole=Image.new('RGBA',(768,560),(47,58,63,255));wd=ImageDraw.Draw(whole)
contact=Image.new('RGBA',(640,200),(47,58,63,255));cd=ImageDraw.Draw(contact)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,im) in enumerate([('original pose',Image.open(p/'master-head-review-v16'/(mode+'-024.png')).convert('RGBA')),('material before',Image.open(p/'master-material-phase24-v52'/(mode+'-head-protected.png')).convert('RGBA')),('contact trial',results[mode])]):
        whole.alpha_composite(im,(col*256,row*280+24));wd.text((col*256+5,row*280+5),mode+' '+label,fill='white')
for col,(label,f) in enumerate([('original grip',p/'master-head-review-v16/bare-024.png'),('material before',p/'master-material-phase24-v52/bare-head-protected.png'),('local contact trial',out/'bare-candidate.png'),('repaired entry',p/'master-material-v49/bare-head-protected.png')]):
    im=Image.open(f).convert('RGBA').crop((80,104,160,184));contact.alpha_composite(im.resize((160,160),Image.Resampling.NEAREST),(col*160,24));cd.text((col*160+4,5),label,fill='white')
whole.save(out/'paired-whole-review.png');contact.save(out/'contact-review.png')
(out/'review.json').write_text(json.dumps(dict(admissionBox=list(box),outsidePixelsExact=63464,headLegsOutsideExact=True,pairedBodyBelow110Exact=True,rawSize=list(raw.size),normalization='One full crop normalization to80, fixed coordinate admission; no bbox fitting/paint/color edits.',visualReviewPending=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
rasters=[f.relative_to(r).as_posix() for f in out.glob('*.png')];attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(outsidePixelsExact=63464,pairedBodyBelow110Exact=True,lfsRasters=len(rasters))))
