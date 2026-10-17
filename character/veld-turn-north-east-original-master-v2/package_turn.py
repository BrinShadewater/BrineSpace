from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];G=R/'character/veld-turn-north-east-original-master-v1';H=R/'character/veld-helmet-original-turntable-v1';old=R/'character/veld-cargo-turns-master-family-v1/north-east-candidate-v5';refs={'bare':[],'helmet':[]};checks=0;fits=[];bindings={};board=Image.new('RGB',(1536,590),'#202a30');d=ImageDraw.Draw(board)
for i in range(6):
    if i==0:
        pair={gear:Image.open(G/f'gather-frames/{gear}/000.png').convert('RGBA') for gear in refs};fits.append({'phase':i,'exactWholeGatherAlias':True})
    else:
        bare=Image.open(P/f'diagnostic-frames-v2/{i:03}.png').convert('RGBA');a=np.array(bare);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());hx=np.where(a[top:top+16,:,3]>128)[1]
        shellpath=H/f'v3-study/shells/{i:03}.png';shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-4:,:,3]>160);center=(sx.min()+sx.max())/2
        # Whole angular shell, fixed authored scale. Anchor gasket under head above collar.
        axis=(hx.min()+hx.max())/2;pos=(round(axis-center),104-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,103)
        helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
        protected=np.ones((256,256),bool);protected[min(top,pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
        assert np.array_equal(a[protected],np.array(helmet)[protected]);checks+=1;pair={'bare':bare,'helmet':helmet};fits.append({'phase':i,'sourceShell':shellpath.relative_to(R).as_posix(),'wholeShellSize':list(shell.size),'position':pos,'clearBox':clear})
        bindings[shellpath.relative_to(R).as_posix()]=hashlib.sha256(shellpath.read_bytes()).hexdigest()
    for row,(gear,f) in enumerate(pair.items()):
        if i==0:ref='res://'+(G/f'gather-frames/{gear}/000.png').relative_to(R).as_posix()
        else:
            dest=P/f'frames/{gear}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest);ref='res://'+dest.relative_to(R).as_posix()
        refs[gear].append(ref);bindings[ref[6:]]=hashlib.sha256((R/ref[6:]).read_bytes()).hexdigest();z=np.array(f);assert not np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20);checks+=1
        board.paste(f,(i*256,row*285+22),f);d.text((i*256+4,row*285+4),gear+(' exact gathered' if i==0 else f' turn{i}'),fill='white')
for gear in refs:
    m=json.loads((old/f'{gear}-manifest.json').read_text());m.update(name='Veld original-guided North–East pivot '+gear,status='staged_not_installed')
    for state in m['states']:
        state['frameFiles']=refs[gear] if state['id']=='carry-turn-north-east' else list(reversed(refs[gear]));assert sum(state['frameDurationsMs'])==800 and not state['loop'];checks+=1
        images=[]
        for ref in state['frameFiles']:
            bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(R/ref[6:]).convert('RGBA'));images.append(bg)
        path=P/f'{gear}-{state["id"]}.apng';images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
        with Image.open(path) as movie:
            assert movie.n_frames==6;checks+=1
            for j,f in enumerate(images):movie.seek(j);assert movie.convert('RGBA').tobytes()==f.tobytes();checks+=1
    (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
board.save(P/'paired-turn-source.png')
for path in [P/'raw-turn-v2.png',P/'source-audit-v2.json',G/'gather-registration.json']:
    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'fits':fits,'bindings':bindings,'sourceOrder':[0,1,2,3,4,5],'reverseOrder':[5,4,3,2,1,0],'durationMs':800,'scope':'Whole original-guided body pivot, exact reviewed gathered North source alias, whole existing original angular shells/body protection, finite reverse timing unchanged. Wider held-to-gather motion and new East held join remain separate; no normal/controller/gait acceptance.'},indent=2)+'\n');print(f'{checks}source/protection/timing/APNGchecks,0failures')
