from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];C=R/'character/veld-cargo-north-original-master-v3';frames={};checks=0;bindings={}
bare=Image.open(P/'diagnostic-gather-v2.png').convert('RGBA');a=np.array(bare);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());hx=np.where(a[top:top+16,:,3]>128)[1]
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shellpath).convert('RGBA');assert shell.size==(34,36);checks+=1
clear=(int(hx.min())-3,top,int(hx.max())+4,top+26);pos=(112,top-9);helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
protected=np.ones((256,256),bool);protected[pos[1]:max(top+26,pos[1]+36),min(pos[0],clear[0]):max(pos[0]+34,clear[2])]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1
for gear,image in [('bare',bare),('helmet',helmet)]:
    dest=P/'gather-frames'/gear/'000.png';dest.parent.mkdir(parents=True,exist_ok=True);image.save(dest);ref='res://'+dest.relative_to(R).as_posix();frames[gear]=ref
    m=json.loads((C/f'{gear}-manifest.json').read_text());template=copy.deepcopy(next(s for s in m['states'] if s['id']=='idle-north'));template.update(id='carry-turn-ready-north',frameFiles=[ref],frameDurationsMs=[1000],loop=True)
    m.update(name='Veld original North gathered stance '+gear,status='staged_source_pose_only_not_installed',states=[template]);(P/f'gather-{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    z=np.array(image);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
for f in [P/'raw-gather-v2.png',P/'gather-audit-v2.json',P/'diagnostic-gather-v2.png',shellpath,*[R/r[6:] for r in frames.values()]]:bindings[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
(P/'gather-registration.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'helmetPosition':pos,'headClearBox':clear,'wholeShellSize':[34,36],'scope':'Whole gathered stance body and fixed original North shell; body protected outside head fit. Source pose only: no gather motion, turn chronology, gait contact or gameplay acceptance.'},indent=2)+'\n');print(f'{checks} source/protected-body/clipping checks,0failures')
