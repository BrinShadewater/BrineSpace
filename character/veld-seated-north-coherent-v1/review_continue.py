"""Preserve actual before/after Continue room crops and current file hashes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-continue-v1'
native=json.loads((O/'validation.json').read_text());assert native['runtimePassed']
continuity=json.loads((O/'continuity.json').read_text());assert len(continuity['records'])==6
board=Image.new('RGB',(936,528),'#202a30');draw=ImageDraw.Draw(board);differences=[]
for row,gear in enumerate(['bare','helmet']):
    for col,phase in enumerate(['lower','held','rise']):
        crops=[]
        for index,version in enumerate(['before','after']):
            crop=Image.open(O/f'{gear}-{phase}-{version}.png').convert('RGB').crop((270,280,348,402))
            crops.append(crop)
            board.paste(crop.resize((156,244),Image.Resampling.NEAREST),(col*312+index*156,row*264+20))
            draw.text((col*312+index*156+3,row*264+3),f'{gear} {phase} {version}',fill='white')
        a=np.array(crops[0]);b=np.array(crops[1]);delta=np.abs(a.astype(int)-b.astype(int))
        differences.append({'gear':gear,'phase':phase,'roomCropEqual':crops[0].tobytes()==crops[1].tobytes(),'differentPixels':int(np.any(a!=b,axis=2).sum()),'maximumChannelDelta':int(delta.max())})
board.save(O/'continue-room-board.png')
(P/'continue-crop-review.json').write_text(json.dumps({'scope':'Unmodified native room crops before/after actual disk/fresh-scene staged Continue; exact source/contact/depth checks are in native log','comparisons':differences},indent=2)+'\n')
files=[O/name for name in ['native.log','validation.json','profile-before.json','profile-after.json','continuity.json','final.png','continue-room-board.png']]
files.extend(O/f'{gear}-{phase}-{version}.png' for gear in ['bare','helmet'] for phase in ['lower','held','rise'] for version in ['before','after'])
files.extend([R/'tests/test_veld_seated_north_continue.gd',R/'tests/test_veld_seated_north_continue.gd.uid',R/'tools/run_veld_seated_north_continue.py',P/'review_continue.py',P/'continue-crop-review.json'])
(P/'continue-evidence.json').write_text(json.dumps({'scope':continuity['scope'],'nativeRunner':native,'files':{path.relative_to(R).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in files}},indent=2)+'\n')
print(json.dumps({'boundFiles':len(files),'roomCrops':differences}))
