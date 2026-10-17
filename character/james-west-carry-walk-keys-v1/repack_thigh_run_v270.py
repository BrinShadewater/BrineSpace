from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];old=p/'thigh-run-v268';out=p/'thigh-run-v270';out.mkdir(exist_ok=True)
for name in ['raw.png','prompt.txt','edit-target.png','master-quilt-reference.png']:shutil.copyfile(old/name,out/name)
d=json.loads((old/'inputs.json').read_bytes());d.update(packagingOnly=True,repackOf=268,rawSource='character/james-west-carry-walk-keys-v1/thigh-run-v268/raw.png',rawSha256=hashlib.sha256((old/'raw.png').read_bytes()).hexdigest())
board=Image.new('RGBA',(864,384),(47,59,63,255))
for i,phase in enumerate([19,20]):
 row=next(row for row in d['sources'] if row['phase']==phase);row['admissionPolygon']=[[124,143],[151,145],[162,166],[147,171],[125,160]]
 im=Image.open(r/row['files']['bare']['file']).convert('RGBA');draw=ImageDraw.Draw(im);poly=[tuple(xy) for xy in row['admissionPolygon']];draw.line(poly+[poly[0]],fill=(0,220,220,255));draw.rectangle((134,164,154,184),outline=(230,120,70,255));board.alpha_composite(im.crop((104,128,176,192)).resize((432,384),Image.Resampling.NEAREST),(i*432,0))
board.save(out/'admission-review.png');(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
s=(p/'package_thigh_run_v268.py').read_text(encoding='utf-8').replace('thigh-run-v268','thigh-run-v270');(p/'package_thigh_run_v270.py').write_text(s,encoding='utf-8')
s=(p/'prepare_thigh_window_v269.py').read_text(encoding='utf-8').replace('thigh-window-v269','thigh-window-v271').replace('thigh-run-v268','thigh-run-v270');(p/'prepare_thigh_window_v271.py').write_text(s,encoding='utf-8')
report=json.loads((old/'package-review.json').read_bytes());report.update(disposition='superseded_packaging_undercovered_panel_edges19_20',nativeIncluded=False);(old/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('Reused existing raw; extended19/20 component admission, original knee rectangle still protected.')
