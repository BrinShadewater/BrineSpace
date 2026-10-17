from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-east-first-lift-row-v1';checks=0
for gear in ['bare','helmet']:
 frames=[Image.open(O/f'{gear}-{i:03d}-native.png').convert('RGBA') for i in range(6)]
 frames[0].save(P/f'{gear}-native-source-review.png',save_all=True,append_images=frames[1:],duration=[70]*6,loop=1,disposal=0,blend=0)
 replay=Image.open(P/f'{gear}-native-source-review.png');assert replay.n_frames==6
 for i,im in enumerate(frames):replay.seek(i);assert np.array_equal(np.array(replay.convert('RGBA')),np.array(im));assert round(replay.info['duration'])==70;checks+=2
 board=Image.new('RGB',(800,620),(32,43,49));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im.crop((180,30,280,590)),(i*100,35));d.text((i*100+4,12),f'Pose{i}',fill='white')
 for i,(box,label) in enumerate([((380,30,480,590),'Held master'),((580,30,680,590),'Empty master')]):board.paste(frames[0].crop(box),(600+i*100,35));d.text((600+i*100+2,12),label,fill='white')
 board.save(P/f'{gear}-native-all-pose-review.png')
for i in range(6):
 bare=np.array(Image.open(O/f'bare-{i:03d}-native.png'));helmet=np.array(Image.open(O/f'helmet-{i:03d}-native.png'));assert np.array_equal(bare[460:575,180:280],helmet[460:575,180:280]);checks+=1
expected=json.loads((O/'inputs-after.json').read_text(encoding='utf-8'));changed=[n for n,h in expected.items() if hashlib.sha256((R/n).read_bytes()).hexdigest()!=h];assert not changed
report={'checks':checks,'failures':0,'nativeInputsStillUnchanged':len(expected),'scope':'Exact six-frame native replay pixels/durations per gear and all6 native148lower-body pairs identical; read-only master/source diagnostics. Does not prove rigid contact/master style/full start-stop/ordinary integration.'}
(P/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
