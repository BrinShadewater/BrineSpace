from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((P/'SOURCE_REVIEW.json').read_bytes())
shellpath=R/'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png'
shell=Image.open(shellpath).convert('RGBA');assert shell.size==(33,39)
bindings={str(shellpath.relative_to(R).as_posix()):sha(shellpath),str(Path(__file__).relative_to(R).as_posix()):sha(Path(__file__))}
fits=[];checks=0
for i,row in enumerate(source['frames']):
 path=P/f'frames/bare/{i:03}.png';bare=Image.open(path).convert('RGBA');a=np.asarray(bare)
 top=row['top'];xs=np.where(a[top:top+16,:,3]>128)[1];left=int(xs.min())
 # Track existing rigid shell against moving head; never move or rescale body.
 pos=(left-3,top-11);box=(left-2,top,left+31,top+27)
 im=bare.copy();im.paste((0,0,0,0),box);im.alpha_composite(shell,pos)
 mask=np.ones((256,256),bool);mask[pos[1]:top+28,pos[0]:left+31]=False
 assert np.array_equal(a[mask],np.array(im)[mask]);checks+=1
 dest=P/f'frames/helmet/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest)
 for f in [path,dest]:bindings[f.relative_to(R).as_posix()]=sha(f)
 fits.append(dict(frame=i,headLeft=left,headTop=top,shellPosition=pos,clearBox=box))
sequences=[('repair-west',list(range(142)))]
for gear in ['bare','helmet']:
 states=[]
 for key,indices in sequences:
  refs=['res://'+(P/f'frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in indices]
  holds=[round((i+1)*1000/24)-round(i*1000/24) for i in indices]
  holds=[round((j+1)*4000/len(indices))-round(j*4000/len(indices)) for j in range(len(indices))]
  state=dict(id=key,frameFiles=refs,frameCount=len(refs),frameDurationsMs=holds,loop=False,facings=['west']*len(refs),waterKinds=['repair']*len(refs),waterPoses=[False]*len(refs),depthOffsets=[0.0]*len(refs),sourceIndices=indices)
  states.append(state);ims=[Image.open(R/f[6:]).convert('RGBA') for f in refs]
  ims[0].save(P/f'{gear}-{key}.png',save_all=True,append_images=ims[1:],duration=holds,loop=1,disposal=0,blend=0)
 data=dict(name='Veld original West kneeling examination '+gear,status='staged_source_and_phase_review_not_installed',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,states=states)
 dest=P/f'{gear}-manifest.json';dest.write_text(json.dumps(data,indent=2)+'\n');bindings[dest.relative_to(R).as_posix()]=sha(dest)
 board=Image.new('RGB',(2048,580),'#202a30');d=ImageDraw.Draw(board)
 for j,i in enumerate([0,29,53,54,90,91,115,141]):
  im=Image.open(P/f'frames/{gear}/{i:03}.png').convert('RGBA');board.paste(im,(j*256,24),im);d.text((j*256+4,4),str(i),fill='white');crop=im.crop((75,65,160,155)).resize((170,180),Image.Resampling.NEAREST);board.paste(crop,(j*256+25,330),crop)
 board.save(P/f'{gear}-boundary-review.png')
(P/'FAMILY_REVIEW.json').write_text(json.dumps(dict(bodyOutsideHelmetChecks=checks,failures=0,bindings=bindings,helmetFits=fits,phases={k:{'sourceIndices':v,'durationMs':4000 if k=='repair-west' else sum(round((i+1)*1000/24)-round(i*1000/24) for i in v)} for k,v in sequences},retiming='All142 examination poses retained, uniformly5917ms source to4000ms phase (~1.47925x). Complete unretimed source retained separately.',scope='Stationary examination from exact lowering endpoint. Vial returned before rise, all142 poses retained, finite4s repair phase. No normal admission.'),indent=2)+'\n')
print('Paired142 lowering-only whole source slots. Body outside helmet exact142/142.')
