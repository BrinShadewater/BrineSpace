from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-breathing-continue-v1'
v=json.loads((O/'validation.json').read_text());assert v['passed']
rows=json.loads((O/'continuity.json').read_text())['records'];board=Image.new('RGB',(312,len(rows)*264),'#202a30');d=ImageDraw.Draw(board);review=[];paths=[]
for row,r in enumerate(rows):
 arrays=[]
 for col,phase in enumerate(('before','after')):
  path=O/f"{r['name']}-{phase}.png";crop=Image.open(path).convert('RGB').crop((270,280,348,402));arrays.append(np.array(crop));board.paste(crop.resize((156,244),Image.Resampling.NEAREST),(col*156,row*264+20));d.text((col*156+3,row*264+3),r['name']+' '+phase,fill='white');paths.append(path)
 delta=np.abs(arrays[0].astype(int)-arrays[1].astype(int));review.append({'name':r['name'],'exactSourcePixelsRestored':r['exactPixelsRestored'],'exactRoomCrop':bool(np.array_equal(*arrays)),'roomCropMaxDelta':int(delta.max()),'roomCropDifferentPixels':int(np.any(delta!=0,axis=2).sum())})
board.save(P/'continue-room-board.png');(P/'continue-room-review.json').write_text(json.dumps(review,indent=2)+'\n')
paths += [O/'native.log',O/'validation.json',O/'continuity.json',O/'profile-before.json',O/'profile-after.json',R/'tests/test_veld_breathing_continue.gd',R/'tests/test_veld_breathing_continue.gd.uid',R/'tools/run_veld_breathing_continue.py',P/'continue-room-board.png',P/'continue-room-review.json']
files={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(P/'continue-evidence.json').write_text(json.dumps({'scope':'eight disk checkpoints/fresh scene interior and second-cycle held restores,16actual power/suspend interruptions, timed entry/exit; fixed supports/equipment exact, interrupted local breath relaxes to neutral; no natural routing/owner acceptance/whole-room shade proof','normalSelection':False,'files':files},indent=2)+'\n')
print(json.dumps({'freshRestores':len(rows),'roomCropsExact':sum(v['exactRoomCrop'] for v in review),'cropDeltas':[v['roomCropMaxDelta'] for v in review],'evidenceFiles':len(files)}))
