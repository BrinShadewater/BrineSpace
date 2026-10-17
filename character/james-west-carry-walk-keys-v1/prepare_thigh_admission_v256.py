from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];old=p/'thigh-construction-phase12-v255';out=p/'thigh-construction-phase12-v256';out.mkdir(exist_ok=True);d=json.loads((old/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for name in ['raw.png','prompt.txt','edit-target.png','master-quilt-reference.png']:shutil.copyfile(old/name,out/name)
d.update(admissionPolygon=[(128,144),(151,145),(162,166),(147,171),(129,160)],protectedRectangles=[[134,164,155,185]],repackOf=255,rawSource=old.relative_to(r).as_posix()+'/raw.png',rawSha256=sha(old/'raw.png'),sourceSha256={**d['sourceSha256'],(old/'raw.png').relative_to(r).as_posix():sha(old/'raw.png')},packagingOnly=True)
(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
im=Image.open(r/d['baseFolder']/'bare-head-protected.png').convert('RGBA');draw=ImageDraw.Draw(im);poly=d['admissionPolygon'];draw.line(poly+[poly[0]],fill=(0,220,220,255),width=1);im.crop((104,128,176,192)).resize((432,384),Image.Resampling.NEAREST).save(out/'admission-review.png')
s=(p/'package_thigh_v255.py').read_text(encoding='utf-8').replace('thigh-construction-phase12-v255','thigh-construction-phase12-v256')
s=s.replace('mask&=plate[:,:,3]>=250','mask&=plate[:,:,3]>=250\nfor px0,py0,px1,py1 in d.get("protectedRectangles",[]):mask[py0:py1,px0:px1]=False')
(p/'package_thigh_v256.py').write_text(s,encoding='utf-8');print('Prepared wider panel-specific admission with knee protection for existing raw255; no new generation.')
