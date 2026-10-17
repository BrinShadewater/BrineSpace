from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];B=R/'character/veld-idle-south-original-master-v1'
shellpath=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/011.png'
shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-4:,:,3]>160);center=(sx.min()+sx.max())/2
bare=json.loads((B/'bare-manifest.json').read_text());old=json.loads((B/'helmet-manifest.json').read_text());oldstates={s['id']:s for s in old['states']}
checks=0;rows=[];bindings={};cache={};oldbindings={}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for path in [B/'bare-manifest.json',B/'helmet-manifest.json',shellpath]:bindings[path.relative_to(R).as_posix()]=digest(path)
for state in bare['states']:
    prior=oldstates[state['id']];assert len(prior['frameFiles'])==len(state['frameFiles']);checks+=1
    refs=[];board=Image.new('RGB',(256*len(state['frameFiles']),600),'#202a30');draw=ImageDraw.Draw(board)
    for i,(bref,href) in enumerate(zip(state['frameFiles'],prior['frameFiles'])):
        bp=R/bref[6:];hp=R/href[6:];body=Image.open(bp).convert('RGBA');before=Image.open(hp).convert('RGBA');b=np.array(body);h=np.array(before)
        bindings[bref]=digest(bp);bindings[href]=digest(hp)
        key=(digest(bp),digest(hp))
        if key in cache:
            ref,fit=cache[key];result=Image.open(R/ref[6:]).convert('RGBA')
        else:
            yy,xx=np.where(np.any(b!=h,axis=2));box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
            assert box[3]-box[1]<=50 and box[2]-box[0]<=55,(state['id'],i,box)
            _,gx=np.where(h[box[3]-4:box[3],box[0]:box[2],3]>160);anchor=(gx.min()+gx.max())/2+box[0]
            pos=(round(anchor-center),box[3]-shell.height)
            result=body.copy();result.paste((0,0,0,0),tuple(box));result.alpha_composite(shell,pos)
            protected=np.ones((256,256),bool);protected[min(box[1],pos[1]):max(box[3],pos[1]+shell.height),min(box[0],pos[0]):max(box[2],pos[0]+shell.width)]=False
            assert np.array_equal(np.array(result)[protected],b[protected]);checks+=1
            out=P/'frames/helmet'/f'{len(cache):03}.png';out.parent.mkdir(parents=True,exist_ok=True);result.save(out);ref='res://'+out.relative_to(R).as_posix()
            fit={'clearBox':box,'position':list(pos),'shellSize':list(shell.size),'protectedBody':True};cache[key]=(ref,fit)
        refs.append(ref);rows.append({'state':state['id'],'slot':i,'bare':bref,'oldHelmet':href,'newHelmet':ref,'fit':fit})
        x=i*256;board.paste(before,(x,24),before);board.paste(result,(x,324),result);draw.text((x+4,4),'previous '+str(i),fill='white');draw.text((x+4,304),'shared original '+str(i),fill='white')
    board.save(P/(state['id']+'-comparison.png'));prior['frameFiles']=refs
    for field in ['frameDurationsMs','loop','facings','depthOffsets','waterKinds','waterPoses']:
        assert prior.get(field)==state.get(field),(state['id'],field);checks+=1
old['states']=[oldstates[s['id']] for s in bare['states']]
for gear,data in [('bare',bare),('helmet',old)]:
    data.update(name='Veld South shared original helmet '+gear,status='staged_not_installed')
    (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
    states={s['id']:s for s in data['states']}
    for a,ai,b,bi in [('unload-south',-1,'idle-south',0),('pickup-south',0,'idle-south',0),('pickup-south',-1,'carry-start-south',0),('carry-start-south',-1,'carry-south',0),('carry-stop-south',-1,'pickup-south',-1)]:
        assert Image.open(R/states[a]['frameFiles'][ai][6:]).tobytes()==Image.open(R/states[b]['frameFiles'][bi][6:]).tobytes(),(gear,a,b);checks+=1
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'uniqueHelmetFrames':len(cache),'rows':rows,'bindings':bindings,'wholeShellSource':shellpath.relative_to(R).as_posix(),'gradeChanged':False,'scope':'Rigid whole shared South helmet on original-master corrected bodies. Existing bare sources and clocks unchanged. Turn body grade and normal integration remain open.'},indent=2)+'\n')
print(f'{checks} protected-body/metadata/join checks, zero failures; {len(cache)} unique helmet frames.')
