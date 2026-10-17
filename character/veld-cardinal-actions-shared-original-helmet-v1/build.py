from pathlib import Path
import hashlib,json,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
directions=['north','east','west']
shellrefs={'north':'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png','east':'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png','west':'character/veld-helmet-original-turntable-west-v1/mixed-v5-study/shells/005.png'}
checks=0;rows=[];bindings={};cache={};combined={};baseline={}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(folder,gear):
    path=R/'character'/folder/f'{gear}-manifest.json';bindings[path.relative_to(R).as_posix()]=digest(path)
    data=json.loads(path.read_text())
    for state in data['states']:
        state['frameFiles']=[ref if ref.startswith('res://') else 'res://'+(path.parent/ref).relative_to(R).as_posix() for ref in state['frameFiles']]
    return data
for direction in directions:
    packs={}
    for gear in ['bare','helmet']:
        cargo=load('veld-cargo-'+direction+'-master-family-v1',gear)
        start=load('veld-carry-'+direction+'-start-master-v1',gear)
        gait=load('veld-carry-'+direction+'-master-proportions-v1'+('/paired-package-v1' if direction=='east' else ''),gear)
        states={}
        for family in [cargo,start,gait]:
            for state in family['states']:states[state['id']]=state
        base=copy.deepcopy(start);base['states']=list(states.values());packs[gear]=base
        if gear not in combined:
            combined[gear]=copy.deepcopy(base);combined[gear]['states']=[];combined[gear]['strideDistanceCells']={}
            baseline[gear]=copy.deepcopy(combined[gear])
        combined[gear]['strideDistanceCells'].update(gait.get('strideDistanceCells',{}))
        baseline[gear]['strideDistanceCells'].update(gait.get('strideDistanceCells',{}))
        baseline[gear]['states'].extend(copy.deepcopy(base['states']))
    shellpath=R/shellrefs[direction];bindings[shellrefs[direction]]=digest(shellpath);shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-4:,:,3]>160);center=(sx.min()+sx.max())/2
    equipped={s['id']:s for s in packs['helmet']['states']}
    for state in packs['bare']['states']:
        prior=equipped[state['id']];assert len(prior['frameFiles'])==len(state['frameFiles']);checks+=1
        refs=[];board=Image.new('RGB',(256*len(state['frameFiles']),600),'#202a30');draw=ImageDraw.Draw(board)
        for i,(bref,href) in enumerate(zip(state['frameFiles'],prior['frameFiles'])):
            bp=R/bref[6:];hp=R/href[6:];body=Image.open(bp).convert('RGBA');before=Image.open(hp).convert('RGBA');b=np.array(body);h=np.array(before)
            bindings[bref]=digest(bp);bindings[href]=digest(hp);key=(direction,digest(bp),digest(hp))
            if key in cache:
                ref,fit=cache[key];result=Image.open(R/ref[6:]).convert('RGBA')
            else:
                yy,xx=np.where(np.any(b!=h,axis=2));box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
                assert box[3]-box[1]<=55 and box[2]-box[0]<=60,(state['id'],i,box)
                _,gx=np.where(h[box[3]-4:box[3],box[0]:box[2],3]>160);anchor=(gx.min()+gx.max())/2+box[0]
                pos=(round(anchor-center),box[3]-shell.height)
                result=body.copy();result.paste((0,0,0,0),tuple(box));result.alpha_composite(shell,pos)
                protected=np.ones((256,256),bool);protected[min(box[1],pos[1]):max(box[3],pos[1]+shell.height),min(box[0],pos[0]):max(box[2],pos[0]+shell.width)]=False
                assert np.array_equal(np.array(result)[protected],b[protected]);checks+=1
                out=P/'frames/helmet'/f'{len(cache):03}.png';out.parent.mkdir(parents=True,exist_ok=True);result.save(out);ref='res://'+out.relative_to(R).as_posix()
                fit={'clearBox':box,'position':list(pos),'wholeShellSource':shellrefs[direction],'shellSize':list(shell.size),'protectedBody':True};cache[key]=(ref,fit)
            refs.append(ref);rows.append({'state':state['id'],'slot':i,'bare':bref,'oldHelmet':href,'newHelmet':ref,'fit':fit})
            x=i*256;board.paste(before,(x,24),before);board.paste(result,(x,324),result);draw.text((x+4,4),'previous '+str(i),fill='white');draw.text((x+4,304),'shared original '+str(i),fill='white')
        board.save(P/(state['id']+'-comparison.png'));prior['frameFiles']=refs
        for field in ['frameDurationsMs','loop','facings','depthOffsets','waterKinds','waterPoses']:
            assert prior.get(field)==state.get(field),(state['id'],field);checks+=1
    for gear in ['bare','helmet']:combined[gear]['states'].extend(packs[gear]['states'])
for gear,data in combined.items():
    data.update(name='Veld N/E/W shared original helmet actions '+gear,status='staged_not_installed')
    (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n')
    (P/f'baseline-{gear}-manifest.json').write_text(json.dumps(baseline[gear],indent=2)+'\n')
    states={s['id']:s for s in data['states']}
    for direction in directions:
        for a,ai,b,bi in [('unload',-1,'pickup',0),('pickup',-1,'carry-start',0),('carry-start',-1,'carry',0),('carry-stop',-1,'pickup',-1)]:
            assert Image.open(R/states[a+'-'+direction]['frameFiles'][ai][6:]).tobytes()==Image.open(R/states[b+'-'+direction]['frameFiles'][bi][6:]).tobytes(),(gear,direction,a,b);checks+=1
turns=json.loads((R/'character/veld-helmet-original-turntable-west-v1/helmet-manifest.json').read_text());turns={s['id']:s for s in turns['states']}
for direction,route in [('north','north-east'),('east','east-south'),('west','west-north')]:
    states={s['id']:s for s in combined['helmet']['states']};source=R/turns['carry-turn-'+route]['frameFiles'][0][6:];bindings[source.relative_to(R).as_posix()]=digest(source)
    assert Image.open(source).tobytes()==Image.open(R/states['pickup-'+direction]['frameFiles'][-1][6:]).tobytes(),direction;checks+=1
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'uniqueHelmetFrames':len(cache),'rows':rows,'bindings':bindings,'wholeShellSources':shellrefs,'gradeChanged':False,'scope':'Rigid whole original N/E/W equipment on unchanged staged master action bodies. Exact held/turn and lifecycle sources, no body grade edits or normal integration.'},indent=2)+'\n')
print(f'{checks} protected-body/metadata/lifecycle/cardinal-turn checks0; {len(cache)} unique helmet frames;15 actions.')
