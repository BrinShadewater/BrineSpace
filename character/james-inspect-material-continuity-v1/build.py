"""One directional cloth calibration across complete selected diagnostics sources."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];I=R/'character/james-inspect-tablet-v1'
records=[];packs={};boards={};sourcehash={}
def cloth(a,sample=False):
    rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy=np.indices(a.shape[:2])[0];lum=rgb.mean(2)
    warm=(r-b>12)&(r-g>5);gold=(r-b>18)&(g-b>10)
    return (a[:,:,3]>0)&(yy>=60)&~warm&~gold&(np.ptp(rgb,2)<28)&(lum>12)&(lum<140)&((yy<145)&(yy>67)&(a[:,:,3]>240) if sample else True)
sources={mode:json.loads((I/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']}
masters={mode:json.loads((R/path).read_text()) for mode,path in [('bare','character/crew-runtime-matte-v1/branforth/manifest.json'),('helmet','character/james-shared-helmet-runtime-v1/manifest.json')]}
gains={}
for direction in ['east','south','west','north']:
    state=next(s for s in sources['bare']['states'] if s['id']=='inspect-'+direction)
    arrays=[np.array(Image.open(I/f).convert('RGBA')) for f in state['frameFiles'][1:-1]]
    sm=np.median(np.concatenate([a[:,:,:3][cloth(a,True)] for a in arrays]),0)
    masterstate=next(s for s in masters['bare']['states'] if s['id']=='idle-'+direction);master=np.array(Image.open(R/'character/crew-runtime-matte-v1/branforth'/masterstate['frameFiles'][0]).convert('RGBA'));tm=np.median(master[:,:,:3][cloth(master,True)],0)
    gains[direction]={'sourcePooledClothMedian':sm.tolist(),'masterClothMedian':tm.tolist(),'gain':(tm/sm).tolist()}
for mode,original in sources.items():
    pack=copy.deepcopy(original);pack['name']='James complete tablet cloth continuity '+mode;pack['status']=json.loads((P/'selection.json').read_text())['status'] if (P/'selection.json').exists() else 'candidate_material_review_pending';states=[]
    for state in original['states']:
        direction=state['id'].split('-')[-1];gain=np.array(gains[direction]['gain']);frames=[];old=[];paths=[]
        for i,f in enumerate(state['frameFiles']):
            src=(I/f).resolve();im=Image.open(src).convert('RGBA');a=np.array(im);out=a.copy();mask=cloth(a)
            if i in [0,len(state['frameFiles'])-1]:mask[:]=False
            rgb=a[:,:,:3].astype(float);out[:,:,:3][mask]=np.rint(rgb[mask]*gain).clip(0,255).astype('uint8')
            assert np.array_equal(a[:,:,3],out[:,:,3]);assert np.array_equal(a[~mask],out[~mask])
            dest=P/'frames'/mode/direction/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(dest);paths.append(dest.relative_to(P).as_posix());old.append(im);frames.append(Image.fromarray(out));sourcehash[src.relative_to(R).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest()
            records.append({'mode':mode,'direction':direction,'index':i,'alphaExact':True,'outsideClothMaskExact':True,'changedPixels':int(np.any(a!=out,2).sum()),'source':src.relative_to(R).as_posix(),'frame':paths[-1]})
        new=copy.deepcopy(state);new['frameFiles']=paths;new['provenance']['materialContinuity']='One pooled facing-specific cloth gain shared by bare/helmet entire clip; fixed y>=60 excludes head/helmet, skin/gold protected, exact idle endpoints. No anatomy/alpha/clock changes.';states.append(new)
        masterroot=R/('character/crew-runtime-matte-v1/branforth' if mode=='bare' else 'character/james-shared-helmet-runtime-v1');ms=next(s for s in masters[mode]['states'] if s['id']=='idle-'+direction);mi=Image.open(masterroot/ms['frameFiles'][0]).convert('RGBA')
        board=Image.new('RGB',(7*184,3*216),'#303b40');d=ImageDraw.Draw(board);indices=[0,len(frames)//6,len(frames)//3,len(frames)//2,len(frames)*2//3,len(frames)*5//6,len(frames)-1]
        for col,i in enumerate(indices):
            for row,img in enumerate([mi,old[i],frames[i]]):board.paste(img,(col*184,row*216+25),img);d.text((col*184+6,row*216+6),[mode+' master','original '+str(i),'revised '+str(i)][row],fill='white')
        board.save(P/(mode+'-'+direction+'-review.png'))
    # Preserve original diagnostic clocks independently of inspection's terminal hold.
    for state in list(states):
        direction=state['id'].split('-')[-1];version={'east':'v1','south':'v3','west':'v2','north':'v2'}[direction]
        folder=R/'character'/(f'james-interact-{direction}-matched-{version}' if mode=='bare' else f'james-shared-helmet-interact-{direction}-{version}')
        original_interact=next(s for s in json.loads((folder/'manifest.json').read_text())['states'] if s['id']=='interact-'+direction)
        interaction=copy.deepcopy(original_interact);assert len(interaction['frameFiles'])==len(state['frameFiles']);interaction['frameFiles']=state['frameFiles'];states.append(interaction)
    if mode=='helmet':
        meals=json.loads((R/'character/james-meal-family-v1/helmet-manifest.json').read_text())
        for meal in meals['states']:
            substitute=copy.deepcopy(meal);source=next(s for s in states if s['id']==meal['provenance']['sourceState']);substitute['frameFiles']=[source['frameFiles'][i] for i in meal['provenance']['sourcePoses']];substitute['provenance']['originalPixels']=False;substitute['provenance']['materialSource']='Selected revised complete diagnostics neutral-material frames, exact source indices and unchanged meal substitute clocks.';states.append(substitute)
    pack['states']=states;packs[mode]=pack;(P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
(P/'material-evidence.json').write_text(json.dumps({'frames':len(records),'alphaAllExact':True,'outsideClothMaskAllExact':True,'idleEndpointsExact':True,'gains':gains,'records':records,'sourceHashes':sourcehash,'geometryClockChanges':False,'productionInstalled':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':len(records),'gains':gains,'alphaAllExact':True,'geometryClockChanges':False,'productionInstalled':False}))
