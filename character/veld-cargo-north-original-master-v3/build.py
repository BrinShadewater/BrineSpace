from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];B=R/'character/veld-idle-north-original-master-v1'
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shellpath).convert('RGBA')
assert shell.size==(34,36)
refs={g:[] for g in ['bare','helmet']};checks=0;fits=[];bindings={}
source=json.loads((P/'source-registration.json').read_text())
for row in source['rows']:
    assert abs(row['headRegionWidth']-22)<=1;checks+=1
for i in [0,4,5]:assert source['rows'][i]['height']==148;checks+=1
board=Image.new('RGB',(1536,620),'#202a30');d=ImageDraw.Draw(board)
for i in range(6):
    if i==5:
        bare=Image.open(B/'frames/bare/000.png').convert('RGBA');equipped=Image.open(B/'frames/helmet/000.png').convert('RGBA')
        fit={'pose':i,'exactPreparedIdleAlias':True}
    else:
        bare=Image.open(P/'diagnostic-frames'/f'{i:03}.png').convert('RGBA');a=np.array(bare);ys,xs=np.where(a[:,:,3]>200);top=int(ys.min())
        headx=np.where(a[top:top+16,:,3]>128)[1]
        clear=(int(headx.min())-3,top,int(headx.max())+4,top+26);position=(112,top-9)
        equipped=bare.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,position)
        protected=np.ones((256,256),bool);protected[position[1]:max(clear[3],position[1]+36),min(112,clear[0]):max(146,clear[2])]=False
        assert np.array_equal(np.array(equipped)[protected],a[protected]);checks+=1
        fit={'pose':i,'position':position,'clearBox':clear,'wholeShellSize':[34,36],'bodyProtected':True}
    fits.append(fit)
    for row,(g,f) in enumerate([('bare',bare),('helmet',equipped)]):
        dest=P/'frames'/g/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest)
        ref='res://'+dest.relative_to(R).as_posix();refs[g].append(ref);bindings[ref]=hashlib.sha256(dest.read_bytes()).hexdigest()
        aa=np.array(f);assert not np.any(np.concatenate([aa[0,:,3],aa[-1,:,3],aa[:,0,3],aa[:,-1,3]])>20);checks+=1
        board.paste(f,(i*256,row*300+30),f);d.text((i*256+4,row*300+5),g+' unload '+str(i),fill='white')
for g in refs:
    old=json.loads((B/f'{g}-manifest.json').read_text());baseline=copy.deepcopy(old)
    baseline['states']=[s for s in baseline['states'] if s['id'] in ['unload-north','pickup-north','idle-north']]
    (P/f'baseline-{g}-manifest.json').write_text(json.dumps(baseline,indent=2)+'\n')
    data=copy.deepcopy(baseline);data['name']='Veld original-master North cargo '+g
    for state in data['states']:
        if state['id']=='unload-north':state['frameFiles']=refs[g]
        elif state['id']=='pickup-north':state['frameFiles']=list(reversed(refs[g]))
        images=[]
        for ref in state['frameFiles']:
            im=Image.open(R/ref[6:]).convert('RGBA');bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(im);images.append(bg)
        path=P/f"{g}-{state['id']}.apng";images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=state['frameDurationsMs'],loop=0 if state['loop'] else 1,disposal=0,blend=0)
        with Image.open(path) as decoded:
            assert decoded.n_frames==len(images);checks+=1
            for j,im in enumerate(images):decoded.seek(j);assert decoded.convert('RGBA').tobytes()==im.tobytes();checks+=1
    unload,pickup,idle=[next(s for s in data['states'] if s['id']==a) for a in ['unload-north','pickup-north','idle-north']]
    assert Image.open(R/unload['frameFiles'][-1][6:]).tobytes()==Image.open(R/idle['frameFiles'][0][6:]).tobytes();checks+=1
    assert Image.open(R/pickup['frameFiles'][0][6:]).tobytes()==Image.open(R/idle['frameFiles'][0][6:]).tobytes();checks+=1
    (P/f'{g}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
board.save(P/'paired-unload.png')
for file in [P/'raw-unload-v6.png',P/'source-registration.json',shellpath,B/'bare-manifest.json',B/'helmet-manifest.json']:
    bindings[file.relative_to(R).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceScale':source['sourceScale'],'rows':source['rows'],'helmetFits':fits,'bindings':bindings,'scope':'Staged original-guided whole North unload/pickup with exact original idle endpoint. Held endpoint now differs from older gait/start/turn: rebase them before integration. Cases remain within source poses3–5, independent prop ownership unproven. No RGB grading or per-pose resizing.'},indent=2)+'\n')
print(f'{checks} whole-source/material-protection/alias/APNG checks,0 failures')
