from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];C=R/'character/veld-cargo-north-original-master-v3';G=R/'character/veld-gather-north-original-master-v1';checks=0;refs={'bare':[],'helmet':[]};bindings={};fits=[]
def bind(path):bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
def sole(im,side):
    a=np.array(im);lo,hi=(90,128) if side=='left' else (128,166);y,x=np.where(a[210:225,lo:hi,3]>128);bottom=int(y.max()+210);x=np.where(a[bottom-2:bottom+1,lo:hi,3]>128)[1]+lo
    return {'centerX':float((x.min()+x.max())/2),'bottom':bottom,'width':int(x.max()-x.min()+1)}
held=Image.open(C/'frames/bare/000.png').convert('RGBA');end=Image.open(G/'gather-frames/bare/000.png').convert('RGBA');left=sole(held,'left')['centerX'];right=sole(end,'right')['centerX']
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shellpath).convert('RGBA');bind(shellpath)
board=Image.new('RGB',(1280,590),'#202a30');d=ImageDraw.Draw(board);contact=[]
for phase in range(5):
    if phase in (0,4):
        base=C/'frames' if phase==0 else G/'gather-frames';pair={g:Image.open(base/g/'000.png').convert('RGBA') for g in refs};files={g:'res://'+(base/g/'000.png').relative_to(R).as_posix() for g in refs};fit={'phase':phase,'exactEndpointAliases':files}
    else:
        version=3 if phase==3 else 2
        path=P/f'diagnostic-interiors-v{version}/{phase-1:03}.png';source=Image.open(path).convert('RGBA');side='left' if phase<3 else 'right';target=left if side=='left' else right;before=sole(source,side);dx=round(target-before['centerX'])
        # One authored ruler and vertical registration; only complete-figure X placement.
        bare=Image.new('RGBA',(256,256));bare.alpha_composite(source,(dx,0));bind(path)
        a=np.array(bare);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());hx=np.where(a[top:top+16,:,3]>128)[1];axis=(hx.min()+hx.max())/2;pos=(round(axis-16),top-9);clear=(int(hx.min())-3,top,int(hx.max())+4,top+26)
        helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
        protected=np.ones((256,256),bool);protected[pos[1]:max(clear[3],pos[1]+36),min(pos[0],clear[0]):max(pos[0]+34,clear[2])]=False;assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1
        pair={'bare':bare,'helmet':helmet};files={}
        for gear,im in pair.items():
            dest=P/f'frames/{gear}/{phase:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);files[gear]='res://'+dest.relative_to(R).as_posix()
        fit={'phase':phase,'source':path.relative_to(R).as_posix(),'wholeFrameHorizontalTranslation':dx,'supportSide':side,'targetSupportCenter':target,'before':before,'after':sole(bare,side),'helmetPosition':pos,'headClearBox':clear,'wholeShellSize':[34,36],'protectedBodyExact':True}
        assert abs(fit['after']['centerX']-target)<=.5 and fit['after']['bottom']==224;checks+=2
    fits.append(fit);contact.append({'phase':phase,'left':sole(pair['bare'],'left'),'right':sole(pair['bare'],'right')})
    for row,(gear,im) in enumerate(pair.items()):
        ref=files[gear];refs[gear].append(ref);bind(R/ref[6:]);z=np.array(im);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
        board.paste(im,(phase*256,row*285+22),im);d.text((phase*256+4,row*285+4),gear+f' phase{phase}'+(' exact endpoint' if phase in (0,4) else ''),fill='white')
durations=[80,120,100,120,180]
for gear in refs:
    m=json.loads((C/f'{gear}-manifest.json').read_text());template=copy.deepcopy(next(s for s in m['states'] if s['id']=='idle-north'));states=[]
    for reverse in [False,True]:
        state=copy.deepcopy(template);state.update(id='carry-spread-north' if reverse else 'carry-gather-north',frameFiles=list(reversed(refs[gear])) if reverse else refs[gear],frameDurationsMs=list(reversed(durations)) if reverse else durations,loop=False)
        for key,value in [('facings','north'),('waterKinds','idle'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]*5
        assert sum(state['frameDurationsMs'])==600 and len(state['frameFiles'])==5;checks+=1;states.append(state)
        images=[]
        for ref in state['frameFiles']:
            bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(R/ref[6:]).convert('RGBA'));images.append(bg)
        dest=P/f'{gear}-{state["id"]}.apng';images[0].save(dest,format='PNG',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
        with Image.open(dest) as movie:
            assert movie.n_frames==5;checks+=1
            for i,expected in enumerate(images):movie.seek(i);assert movie.convert('RGBA').tobytes()==expected.tobytes();checks+=1
    m.update(name='Veld original North whole gather/spread '+gear,status='staged_not_installed',states=states,strideDistanceCells={});(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
for path in [P/'raw-interiors-v2.png',P/'interiors-audit-v2.json',P/'raw-interiors-v3.png',P/'interiors-audit-v3.json',G/'gather-registration.json']:bind(path)
board.save(P/'paired-motion-source.png');(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'fits':fits,'contacts':contact,'bindings':bindings,'durationMs':600,'sourceOrder':[0,1,2,3,4],'reverseOrder':[4,3,2,1,0],'unusedSource':'interior4 not selected: exact reviewed corrected gathered endpoint replaces its less certain shoe placement','scope':'Whole-figure horizontal support-sole registration only, common source scale and vertical floor retained. Both exact master endpoints. No anatomy strips or RGB changes. Right second-contact and body balance need independent native motion review; no natural gameplay/gait acceptance.'},indent=2)+'\n');print(f'{checks}source/whole-fit/endpoint/timing/APNGchecks,0failures');print(json.dumps(contact))
