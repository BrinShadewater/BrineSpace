from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];inventory=json.loads((p/'walk-donor-inputs.json').read_bytes());m=r/inventory['manifest'];data=json.loads(m.read_bytes());state=next(s for s in data['states'] if s['id']=='walk-west');indices=[0,8,12,20,28,32,36,44,48];frames=[];files=[m]
for index in indices:
    ref=state['frameFiles'][index];f=r/ref.removeprefix('res://') if ref.startswith('res://') else m.parent/ref;files.append(f);out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(f).convert('RGBA'),(round(128-data['pivot'][0]),round(224-data['pivot'][1])));frames.append(out)
board=Image.new('RGBA',(1056,1230),(48,59,63,255));d=ImageDraw.Draw(board)
for i,(index,im) in enumerate(zip(indices,frames)):
    x=(i%3)*352;y=(i//3)*410;board.alpha_composite(im.crop((88,144,176,240)).resize((352,384),Image.Resampling.NEAREST),(x,y+26));d.text((x+5,y+7),'selected walk-west '+str(index),fill='white')
board.convert('RGB').save(p/'walk-limb-ownership.png')
(p/'limb-ownership-inputs.json').write_text(json.dumps({'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'indices':indices,'visualReviewPending':True,'scope':'Nine enlarged representative source leg phases, not continuous cadence/full limb tracking.'},indent=2)+'\n',encoding='utf-8')
print('Nine original selected limb-detail phases prepared without transforming anatomy.')
