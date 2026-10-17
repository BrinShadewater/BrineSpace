from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];W=P/'walk-source-v1'
assert not (P/'FAMILY_REVIEW.json').exists(),'Preserve built bank'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((W/'SOURCE_REVIEW.json').read_bytes());assert source['frameCount']==142
for name,digest in source['bindings'].items():assert sha(R/name)==digest
idle=R/'character/veld-idle-west-original-master-v1/blink-only-v2';action=R/'character/veld-interact-west-original-master-v1/original-action-video-v1'
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');assert shell.size==(33,39)
bindings={shellpath.relative_to(R).as_posix():sha(shellpath),str(Path(__file__).relative_to(R)):sha(Path(__file__))}
records=[];manifests={};checks=0
for gear in ['bare','helmet']:
 idlepack=json.loads((idle/f'{gear}-source-manifest.json').read_bytes());actionpack=json.loads((action/f'{gear}-source-manifest.json').read_bytes())
 states=[]
 for stateid,old in [('idle-west',idlepack['states'][0]),('interact-west',actionpack['states'][0])]:
  state=dict(old);state['id']=stateid;state['loop']=True
  states.append(state)
  for ref in state['frameFiles']:
   path=R/ref[6:];bindings[path.relative_to(R).as_posix()]=sha(path)
   checks+=1
 walkrefs=[]
 for i in range(26,50):
  barepath=W/f'frames/bare/{i:03}.png';bare=Image.open(barepath).convert('RGBA')
  bindings[barepath.relative_to(R).as_posix()]=sha(barepath)
  im=bare
  if gear=='helmet':
   im=bare.copy();im.paste((0,0,0,0),(117,76,150,103));im.alpha_composite(shell,(116,65))
   mask=np.ones((256,256),bool);mask[65:104,116:150]=False
   assert np.array_equal(np.array(im)[mask],np.array(bare)[mask]);checks+=1
   path=P/f'frames/helmet-walk/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
  else:path=barepath
  walkrefs.append('res://'+path.relative_to(R).as_posix());bindings[path.relative_to(R).as_posix()]=sha(path)
 states.insert(1,dict(id='walk-west',frameFiles=walkrefs,frameCount=24,frameDurationsMs=[round((i+1)*1000/24)-round(i*1000/24) for i in range(26,50)],loop=True,facings=['west']*24,waterKinds=['walk']*24,waterPoses=[False]*24,depthOffsets=[0.0]*24,provenance='One consecutive complete alternating cycle, raw indices26..49 inclusive; entire142-frame source retained separately.'))
 inv=json.loads((R/'character/veld-library-closeout-v1/installed/selected-library.json').read_bytes());old=json.loads((R/inv['resolved'][gear]['walk-west']['manifest']).read_bytes());stride=old.get('strideDistanceCells',{}).get('walk-west',old.get('strideDistanceCells',{}).get('walk',0.1796875))
 data=dict(name='Veld original West standing family '+gear,status='staged_family_motion_join_review_not_installed',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,strideDistanceCells={'walk-west':stride},states=states)
 path=P/f'{gear}-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');bindings[path.relative_to(R).as_posix()]=sha(path);manifests[gear]=data
 for state in states:
  refs=[R/ref[6:] for ref in state['frameFiles']];ims=[Image.open(ref).convert('RGBA') for ref in refs]
  ims[0].save(P/f'{gear}-{state["id"]}.png',save_all=True,append_images=ims[1:],duration=state['frameDurationsMs'],loop=0,disposal=0,blend=0)
 board=Image.new('RGB',(2048,580),'#202a30');draw=ImageDraw.Draw(board)
 slots=[('idle-west',141),('walk-west',0),('walk-west',23),('walk-west',0),('idle-west',0),('idle-west',141),('interact-west',0),('interact-west',141)]
 for j,(sid,n) in enumerate(slots):
  state=next(s for s in states if s['id']==sid);im=Image.open(R/state['frameFiles'][n][6:]).convert('RGBA');board.paste(im,(j*256,30),im);draw.text((j*256+4,4),sid+' '+str(n),fill='white')
  crop=im.crop((95,65,160,125)).resize((195,180),Image.Resampling.NEAREST);board.paste(crop,(j*256+20,330),crop)
 board.save(P/f'{gear}-boundary-review.png')
report=dict(checks=checks,failures=0,slotsPerGear=308,walkCycle=dict(firstRawIndex=26,lastRawIndex=49,durationMs=1000,wholeSourceSlotsPreserved=142,reason='Full consecutive left/right alternating cycle between same passing stance; not omission of bad middle frames.'),helmet=dict(source=shellpath.relative_to(R).as_posix(),position=[116,65],clearBox=[117,76,150,103],bodyOutsideFittingExact=True),stride='Existing selected walk stride retained for trial; root contact validation pending',bindings=bindings,scope='Staged complete idle142/scanner142 and one24-slot walk cycle. All raw walk142 retained. No normal selection/controller/save changes. Loop/contact/material/transition review pending.')
(P/'FAMILY_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:report[k] for k in ['checks','slotsPerGear','walkCycle']}))
