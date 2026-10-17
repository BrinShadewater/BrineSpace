from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,copy
P=Path(__file__).resolve().parent;R=P.parents[2];shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png';shell=Image.open(shellpath).convert('RGBA');frame_paths={g:[] for g in ['bare','helmet']};checks=0;bindings=[];fits=[]
for i,p in enumerate(sorted((P/'diagnostic-frames').glob('*.png'))):
 bare=Image.open(p).convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];_,sx=np.where(np.array(shell)[-4:,:,3]>160);pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),top+28-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+27)
 helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos);protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(clear[2],pos[0]+shell.width)]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1;fits.append(list(pos));bindings.append(p)
 for gear,im in [('bare',bare),('helmet',helmet)]:
  path=P/f'frames/{gear}/{i:03d}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);frame_paths[gear].append(path);bindings.append(path);z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
assert len(frame_paths['bare'])==6
for gear in frame_paths:
 data=json.loads((P.parent/'single-transition-source-v1'/f'{gear}-source-manifest.json').read_text(encoding='utf-8'));state=copy.deepcopy(data['states'][0]);state.update(id='carry-preparation-source-east',frameCount=6,frameFiles=['res://'+p.relative_to(R).as_posix() for p in frame_paths[gear]],frameDurationsMs=[70]*6,loop=False)
 for k in ['facings','waterKinds','waterPoses','depthOffsets']:state[k]=state[k]*6
 data.update(name='Veld East six-pose initial lift source study '+gear,status='provisional_source_motion_study_only',strideDistanceCells={},states=[state]+data['states'][1:]);path=P/f'{gear}-source-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8');bindings.append(path)
 for other in data['states'][1:]:bindings.extend(R/p[6:] for p in other['frameFiles'])
bindings.extend([P/'raw-first-lift-v1.png',P/'prompt.txt',P/'source-registration.json',P/'transition-audit.json',P/'register_source.py',Path(__file__),shellpath])
record={'generationId':'65b02932-42fe-41b6-9591-69237fbeb2e5','checks':checks,'failures':0,'helmetPositions':fits,'protectedBodyExact':True,'scope':'Complete six-pose independent source motion study. Original-only row gives neutral cloth and progressive far lift, but master head27-28vs26, upperbody45-47vs42, near sole centroid126.5..129vs125.5 and excess lift/advance remain. Not accepted identity/rigid contact/full start-stop/controller/normal selectors. Exact original held/idle references retained for comparison; no substituted source endpoint or clipped chronology.','bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(bindings))}}
(P/'key-record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'helmetPositions':fits}))
