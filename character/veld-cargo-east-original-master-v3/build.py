from pathlib import Path
import json,hashlib,copy,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent;R=P.parents[1];Q=R/'character/veld-cargo-east-original-master-v2';checks=0
def component(im):
 a=np.array(im.convert('RGBA'));labels,n=ndimage.label(a[:,:,3]>200);counts=np.bincount(labels.ravel());counts[0]=0;a[~ndimage.binary_dilation(labels==counts.argmax(),iterations=3)]=0;return Image.fromarray(a)
source=json.loads((Q/'shared-case-registration.json').read_text(encoding='utf-8'));atlas=json.loads((Q/'contact-registration.json').read_text(encoding='utf-8'));case=Image.open(Q/'shared-floor-case.png').convert('RGBA');case.save(P/'floor-case.png');case_pos=tuple(source['sharedCompleteCase']['position'])
bodies={gear:[] for gear in ['bare','helmet']}
for i in range(6):
 if i<3:
  for gear in bodies:bodies[gear].append(Image.open(Q/f'frames/{gear}/{i:03}.png').convert('RGBA'))
  continue
 b=Image.new('RGBA',(256,256))
 if i==3:
  im=component(Image.open(Q/'raw-deep-body-v1.png'));ratio=source['independentDeepBody']['uniformScale'];im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS);b.alpha_composite(im,tuple(source['independentDeepBody']['offset']))
 elif i==4:
  row=atlas['rows'][i];im=component(Image.open(Q/'raw-unload-v4.png').crop(tuple(row['sourceCell'])));scale=atlas['sourceScale'];im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);b.alpha_composite(im,tuple(row['offset']))
 else:b.alpha_composite(Image.open(R/'character/veld-side-foundation-v1/east-standing.png').convert('RGBA'),(36,52))
 bodies['bare'].append(b)
 a=np.array(b);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];shell=Image.open(R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png').convert('RGBA');_,sx=np.where(np.array(shell)[-4:,:,3]>160);pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
 equipped=b.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,pos);bodies['helmet'].append(equipped)
for gear,figures in bodies.items():
 refs=[]
 for i,b in enumerate(figures):
  out=Image.new('RGBA',(256,256))
  if i>=3:out.alpha_composite(case,case_pos)
  out.alpha_composite(b);old=Image.open(Q/f'frames/{gear}/{i:03}.png').convert('RGBA');assert out.tobytes()==old.tobytes(),'Source decomposition changed '+gear+str(i);checks+=1
  path=P/f'frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);b.save(path);refs.append('res://'+path.relative_to(R).as_posix())
  a=np.array(b);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
 pack=json.loads((Q/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 for state in pack['states']:
  ids=[int(Path(ref).stem) for ref in state['frameFiles']];state['frameFiles']=[refs[i] for i in ids]
 pack.update(name='Veld original East cargo body / separate prop '+gear,status='staged_not_installed');(P/f'{gear}-manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
contract={'textureFile':'res://character/veld-cargo-east-original-master-v3/floor-case.png','frameSize':[256,256],'pivot':[128,224],'standingHeight':148,'topLeftOffsetFromFoot':[case_pos[0]-128,case_pos[1]-224],'unloadDepositMs':260,'pickupTakeMs':260,'sourceOwnership':{'heldCaseEmbeddedPoses':[0,1,2],'bodyOnlyPoses':[3,4,5]},'storagePolicy':'Caller retires visual floor case when ordinary cargo delivery is credited. This pack does not change gameplay delivery or make a collectible.','scope':'Staged visual prop contract; world lifetime/departure/checkpoint fixture, normal integration pending.'}
(P/'cargo-contract.json').write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8')
paths=[Q/'build_shared_case.py',Q/'source-record.json',Q/'shared-case-registration.json',Q/'contact-registration.json',Q/'raw-deep-body-v1.png',Q/'raw-unload-v4.png',Q/'shared-floor-case.png',R/'character/veld-side-foundation-v1/east-standing.png',R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png',P/'build.py',P/'cargo-contract.json',P/'floor-case.png'];paths+=list((Q/'frames').rglob('*.png'))+list((P/'frames').rglob('*.png'))+list(P.glob('*-manifest.json'))
report={'checks':checks,'failures':0,'sourceRecompositionExact':True,'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'Complete body extraction plus separate complete floor equipment. All12 recomposed sources exactly equal previous paired pack; true original empty body now ordinary idle source. No new artwork/anatomy/RGB/grade changes.'};(P/'registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='bindings'}))
board=Image.new('RGB',(1536,600),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(bodies):
 for i,b in enumerate(bodies[gear]):board.paste(b,(i*256,row*290+20),b);d.text((i*256+4,row*290+3),f'{gear} body {i}',fill='white')
board.save(P/'body-only-review.png')
