from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parents[3];K=P.parent;A=R/'character/veld-interact-north-original-master-v1/front-occluded-v2'
bindings={};checks=0
for q in [K/'full-source-record.json',A/'full-source-record.json']:
 old=json.loads(q.read_bytes())['bindings'];assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in old.items());bindings.update(old);bindings[q.relative_to(R).as_posix()]=hashlib.sha256(q.read_bytes()).hexdigest()
for gear in ['bare','helmet']:
 keys=json.loads((K/f'{gear}-native-manifest.json').read_bytes());idle=keys['states'][0];source=json.loads((A/f'{gear}-native-manifest.json').read_bytes());action=next(s for s in source['states'] if s['id']=='interact-north')
 files=idle['frameFiles']+action['frameFiles']+idle['frameFiles'];ds=idle['frameDurationsMs']+action['frameDurationsMs']+idle['frameDurationsMs'];assert len(files)==82 and sum(ds)==6250
 state=dict(id='source-interact-north',frameCount=82,frameFiles=files,frameDurationsMs=ds,loop=False,facings=['north']*82,waterKinds=['interact']*82,waterPoses=[False]*82,depthOffsets=[0.0]*82)
 keys['states']=[state]+keys['states'][1:];keys['status']='staged_complete_unchanged_two_key_idle_scanner_join_study';manifest=P/f'{gear}-native-manifest.json';manifest.write_text(json.dumps(keys,indent=2)+'\n');bindings[manifest.relative_to(R).as_posix()]=hashlib.sha256(manifest.read_bytes()).hexdigest()
 images=[Image.open(R/f[6:]).convert('RGBA') for f in files];dest=P/f'{gear}-joined-source.png';images[0].save(dest,save_all=True,append_images=images[1:],duration=ds,loop=1,disposal=0,blend=0);replay=Image.open(dest);assert replay.n_frames==82
 for i,im in enumerate(images):replay.seek(i);assert np.array_equal(np.asarray(im),np.asarray(replay.convert('RGBA')));assert round(replay.info['duration'])==ds[i];checks+=2
 board=Image.new('RGB',(2048,560),'#202a30');d=ImageDraw.Draw(board)
 for j,i in enumerate([0,1,2,3,78,79,80,81]):
  im=images[i];board.paste(im,(j*256,24),im);d.text((j*256+3,3),f'Joined slot{i}',fill='white');detail=im.crop((96,64,160,128)).resize((256,256),Image.Resampling.NEAREST);board.paste(detail,(j*256,288),detail)
 board.save(P/f'{gear}-join-details.png')
for q in [P/'build.py',K/'KEY_REVIEW.json']:bindings[q.relative_to(R).as_posix()]=hashlib.sha256(q.read_bytes()).hexdigest()
(P/'full-source-record.json').write_text(json.dumps(dict(bindings=bindings,replayChecks=checks,failures=0,scope='Full unchanged two-key idle/complete first78action/two-key idle; no omission/interpolation/art edits or production adoption.'),indent=2)+'\n');print(checks,'source replay checks0;82poses6250ms pergear')
