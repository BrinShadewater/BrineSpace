from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];B=R/'character/veld-cargo-north-original-master-v3';I=R/'character/veld-idle-north-original-master-v1'
source=json.loads((P/'source-registration.json').read_text());checks=0;fits=[];bindings={};refs={g:[] for g in ['bare','helmet']}
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shellpath).convert('RGBA');assert shell.size==(34,36)
board=Image.new('RGB',(1792,620),'#202a30');d=ImageDraw.Draw(board)
for row in source['rows']:
    assert row['height']==148 and abs(row['headRegionWidth']-22)<=1;checks+=1
for i in range(6):
    bare=Image.open(P/'diagnostic-frames'/f'{i:03}.png').convert('RGBA');a=np.array(bare);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    clear=(int(hx.min())-3,top,int(hx.max())+4,top+26);pos=(112,top-9)
    helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
    protected=np.ones((256,256),bool);protected[pos[1]:max(top+26,pos[1]+36),min(112,clear[0]):max(146,clear[2])]=False
    assert np.array_equal(np.array(helmet)[protected],a[protected]);checks+=1;fits.append({'phase':i,'helmetPosition':pos,'clearBox':clear,'wholeShellSize':[34,36]})
    for row,(g,f) in enumerate([('bare',bare),('helmet',helmet)]):
        dest=P/'frames'/g/f'{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest);ref='res://'+dest.relative_to(R).as_posix();refs[g].append(ref);bindings[ref]=hashlib.sha256(dest.read_bytes()).hexdigest()
        aa=np.array(f);assert not np.any(np.concatenate([aa[0,:,3],aa[-1,:,3],aa[:,0,3],aa[:,-1,3]])>20);checks+=1
        board.paste(f,(i*256,row*300+30),f);d.text((i*256+4,row*300+5),g+' authored gait '+str(i),fill='white')
for g in refs:
    prior=json.loads((B/f'{g}-manifest.json').read_text());older=json.loads((I/f'{g}-manifest.json').read_text())
    prior['states'] += [s for s in older['states'] if s['id'] in ['carry-north','carry-start-north','carry-stop-north']]
    (P/f'baseline-{g}-manifest.json').write_text(json.dumps(prior,indent=2)+'\n')
    data=copy.deepcopy(prior);data['name']='Veld original-master North carry/action family '+g
    held=next(s for s in data['states'] if s['id']=='pickup-north')['frameFiles'][-1]
    board.paste(Image.open(R/held[6:]),(1536,(0 if g=='bare' else 300)+30),Image.open(R/held[6:]));d.text((1540,(0 if g=='bare' else 300)+5),g+' exact held',fill='white')
    for s in data['states']:
        if s['id']=='carry-north':s['frameFiles']=[refs[g][i] for i in [2,3,4,5,0,1]]
        elif s['id']=='carry-start-north':s['frameFiles']=[held]+refs[g][:3]
        elif s['id']=='carry-stop-north':s['frameFiles']=list(reversed([held]+refs[g][:3]))
        images=[]
        for ref in s['frameFiles']:
            f=Image.open(R/ref[6:]).convert('RGBA');bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);images.append(bg)
        path=P/f"{g}-{s['id']}.apng";images[0].save(path,format='PNG',save_all=True,append_images=images[1:],duration=s['frameDurationsMs'],loop=0 if s['loop'] else 1,disposal=0,blend=0)
        with Image.open(path) as movie:
            assert movie.n_frames==len(images);checks+=1
            for j,frame in enumerate(images):movie.seek(j);assert movie.convert('RGBA').tobytes()==frame.tobytes();checks+=1
    states={s['id']:s for s in data['states']}
    for a,ia,b,ib in [('pickup-north',-1,'carry-start-north',0),('carry-start-north',-1,'carry-north',0),('carry-stop-north',-1,'pickup-north',-1),('unload-north',-1,'idle-north',0)]:
        assert Image.open(R/states[a]['frameFiles'][ia][6:]).tobytes()==Image.open(R/states[b]['frameFiles'][ib][6:]).tobytes();checks+=1
    (P/f'{g}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
board.save(P/'paired-gait-held.png')
for file in [P/'raw-gait-v3.png',P/'source-registration.json',shellpath,B/'bare-manifest.json',B/'helmet-manifest.json']:
    bindings[file.relative_to(R).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceScale':source['sourceScale'],'rows':source['rows'],'helmetFits':fits,'bindings':bindings,'carrySourceOrder':[2,3,4,5,0,1],'startSources':['exact held',0,1,2],'stopSources':[2,1,0,'exact held'],'scope':'Six original-guided gait sources, balanced alternating support. Derived320ms start/stop source ramps and840ms carry. Exact latest cargo held/idle joins; older turn endpoints still differ. No independent prop, natural controller/cadence/save acceptance.'},indent=2)+'\n')
print(f'{checks} source/body-protection/alias/APNG checks,0 failures')
