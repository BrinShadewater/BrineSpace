from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];old=p/'thigh-crossing-v274';out=p/'thigh-crossing-v276';out.mkdir(exist_ok=True)
for name in ['raw.png','prompt.txt','edit-target.png','master-quilt-reference.png','coordinate-source-review.png']:shutil.copyfile(old/name,out/name)
d=json.loads((old/'inputs.json').read_bytes());d.update(packagingOnly=True,repackOf=274,rawSource='character/james-west-carry-walk-keys-v1/thigh-crossing-v274/raw.png',rawSha256=hashlib.sha256((old/'raw.png').read_bytes()).hexdigest())
knees={26:[118,162,138,181],27:[117,161,135,180],28:[112,159,134,180],29:[108,157,131,180],30:[104,155,129,184]};board=Image.new('RGBA',(1296,768),(47,59,63,255))
for i,row in enumerate(d['sources']):
 phase=row['phase']
 if phase in knees:row['protectedRectangles']=[knees[phase],[96,112,129,147]]
 im=Image.open(r/row['files']['bare']['file']).convert('RGBA');draw=ImageDraw.Draw(im);poly=[tuple(xy) for xy in row['admissionPolygon']];draw.line(poly+[poly[0]],fill=(0,220,220,255))
 for x0,y0,x1,y1 in row['protectedRectangles']:draw.rectangle((x0,y0,x1-1,y1-1),outline=(230,120,70,255))
 board.alpha_composite(im.crop((104,128,176,192)).resize((432,384),Image.Resampling.NEAREST),((i%3)*432,(i//3)*384))
board.save(out/'admission-review.png');(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
s=(p/'package_thigh_crossing_v274.py').read_text(encoding='utf-8').replace('thigh-crossing-v274','thigh-crossing-v276');(p/'package_thigh_crossing_v276.py').write_text(s,encoding='utf-8')
s=(p/'prepare_thigh_window_v275.py').read_text(encoding='utf-8').replace('thigh-window-v275','thigh-window-v277').replace('thigh-crossing-v274','thigh-crossing-v276');(p/'prepare_thigh_window_v277.py').write_text(s,encoding='utf-8')
report=json.loads((old/'package-review.json').read_bytes());report.update(disposition='superseded_packaging_complete_knee_rims_required',nativeIncluded=True,nativeWindow=275,sourceAcceptance=False);(old/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('Reused existing crossing raw; complete original knee rims protected including phase30 prior fitting finish.')
