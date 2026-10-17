from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seat-front-continue-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
records=json.loads((O/'contacts.json').read_text());board=Image.new('RGB',(540,1280),'#202a30');d=ImageDraw.Draw(board);reports=[];files=[]
for row,r in enumerate(records):
 crops=[]
 for col,suffix in enumerate(('before','after')):
  path=O/f'{r["name"]}-{suffix}.png';im=Image.open(path).convert('RGB');crop=im.crop((520,520,655,665));crops.append(np.array(crop))
  board.paste(crop.resize((270,290),Image.Resampling.NEAREST),(col*270,row*320+25));d.text((col*270+5,row*320+5),f'{r["name"]} {suffix}',fill='white');files.append(path)
 delta=np.abs(crops[0].astype(int)-crops[1].astype(int));reports.append({'name':r['name'],'roomCropByteExact':bool(not delta.any()),'maxRoomCropChannelDifference':int(delta.max()),'sourcePixelsExact':'verified by native fixture; room shade distinct'})
board.save(P/'front-continue-room-board.png');files.append(P/'front-continue-room-board.png')
files += [O/n for n in ['contacts.json','validation.json','native.log','profile-before.json','profile-after.json','final.png']]
files += [R/'tests/test_veld_seat_front_continue.gd',R/'tests/test_veld_seat_front_continue.gd.uid',R/'tools/run_veld_seat_front_continue.py']
bound={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'front-continue-review.json').write_text(json.dumps({'cases':reports,'records':records,'scope':'four prescribed actual disk/fresh-scene front/retained-side contact restores; paired staged sources, exact source/offset/depth/clock/pause; natural route proven separately','files':bound},indent=2)+'\n')
print(json.dumps({'cases':reports,'boundFiles':len(bound)}))
