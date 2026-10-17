from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];bindings={};checks=0
bare=Image.open(P/'mid-candidate-v2.png').convert('RGBA');a=np.array(bare);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/004.png';shell=Image.open(shellpath).convert('RGBA');_,sx=np.where(np.array(shell)[-4:,:,3]>160);pos=(round((hx.min()+hx.max())/2-(sx.min()+sx.max())/2),104-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,103)
helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos);protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(pos[0],clear[0]):max(pos[0]+shell.width,clear[2])]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1
for gear,im in [('bare',bare),('helmet',helmet)]:
 path=P/f'frames/{gear}/000.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);ref='res://'+path.relative_to(R).as_posix();m=json.loads((R/f'character/veld-north-gather-turn-chain-v1/{gear}-manifest.json').read_text());state=copy.deepcopy(m['states'][0]);state.update(id='carry-turn-mid-north-east',frameCount=1,frameFiles=[ref],frameDurationsMs=[1000],loop=False)
 for key,value in [('facings','north'),('waterKinds','idle'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]
 m.update(name='Veld original-rig intermediate foundation '+gear,status='staged_not_installed',states=[state],strideDistanceCells={});(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
for path in [P/'raw-mid-v2.png',P/'mid-candidate-v2.png',P/'mid-source-audit-v2.json',P/'whole-mid-angle-reference.png',shellpath,R/'character/veld-cargo-turns-master-family-v1/original-east-density-reference.png',R/'character/veld-side-foundation-v1/east-standing.png',P/'frames/bare/000.png',P/'frames/helmet/000.png']:bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'shellSize':list(shell.size),'shellPosition':pos,'protectedBodyExact':True,'status':'whole original-rig intermediate foundation; complete temporal turn still needs other new source poses'},indent=2)+'\n',encoding='utf-8');print(checks,'whole pair/protection/clipping checks0failures; shell',shell.size,pos)
