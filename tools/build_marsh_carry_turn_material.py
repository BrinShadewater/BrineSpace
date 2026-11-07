"""Pack complete intermediate yaws; preserve endpoints and torso registration."""
from pathlib import Path
import argparse,hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
from rebuild_bill_art import binary
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';S=B/'sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def chest_mid(f):
    b=f.getbbox();y=b[1]+round((b[3]-b[1])*.28);xs=np.flatnonzero(np.array(f)[:,:,3][y]>=128);assert len(xs)>0
    return ((int(xs.min())+int(xs.max()))/2,y)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pair',required=True);ap.add_argument('--source',required=True);ap.add_argument('--generation-id',required=True);args=ap.parse_args();pair=args.pair;stem=args.source;origin,dest=pair.split('-')
    reqpath=S/f'{stem}.request.json';req=json.loads(reqpath.read_text());assert sha(S/f'{stem}.prompt.txt')==req['promptSha256']
    for q in req['orderedReferences']+req['sourceFrames']+req.get('guideDependencies',[]):assert sha(ROOT/q['path'])==q['sha256']
    original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(args.generation_id+'.png');rawpath=S/f'{stem}.raw.png';shutil.copy2(original,rawpath)
    req.update(status='Retained unselected three whole intermediate yaws plus neutral; temporal joins pending',generationId=args.generation_id,originalGeneratedPath=str(original),rawSha256=sha(rawpath));reqpath.write_text(json.dumps(req,indent=2)+'\n')
    raw=Image.open(rawpath).convert('RGBA');a=np.array(raw);xs=np.flatnonzero(np.sum(a[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==4,len(groups)
    edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(3)]+[raw.width];cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(4)];cells=[binary(raw.crop(c)) for c in cuts];nb=cells[-1].getbbox();scale=req['neutralOccupiedTargetHeight']/(nb[3]-nb[1])
    g=json.loads((S/'guide-provenance.json').read_text());endpoints=[ROOT/g['stagedEndpoints'][f]['path'] for f in [origin,dest]];ends=[Image.open(p).convert('RGBA') for p in endpoints];target=[chest_mid(f)[0] for f in ends]
    O=B/f'{stem}-unselected';O.mkdir(exist_ok=True);records=[];poses=[]
    for i,c in enumerate(cells):
        dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox();measured,y=chest_mid(dense)
        wanted=target[0]+(target[1]-target[0])*(i+1)/4 if i<3 else 92
        offset=(round(wanted-measured),172-b[3]);f=Image.new('RGBA',(184,184));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]);name=f'intermediate-{i+1}.png' if i<3 else 'ruler.png';f.save(O/name);poses.append(f);fb=f.getbbox();records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'occupiedBounds':fb,'occupiedSize':[fb[2]-fb[0],fb[3]-fb[1]],'sourceChestRow':y,'sourceChestMidX':measured,'targetChestMidX':wanted,'sha256':sha(O/name)})
    timing=next(t['timing'] for t in g['selectedTurns'] if t['key']==f'carry-turn-{pair}');row=[ends[0],*poses[:3],ends[1]];states=[]
    for name,frames,paths in [(f'carry-turn-{pair}',row,[endpoints[0],None,None,None,endpoints[1]]),(f'carry-turn-{dest}-{origin}',list(reversed(row)),[endpoints[1],None,None,None,endpoints[0]])]:
        folder=O/name;folder.mkdir(exist_ok=True);files=[]
        for i,(f,p) in enumerate(zip(frames,paths)):
            q=folder/f'{i:03}.png'
            if p:shutil.copy2(p,q);assert sha(p)==sha(q)
            else:f.save(q)
            files.append(f'{name}/{i:03}.png')
        old=next(t['timing'] for t in g['selectedTurns'] if t['key']==name);states.append({'id':name,'frameFiles':files,**old})
    m={'revision':f'marsh-carry-turn-material-{stem}-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states};(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    row[0].save(O/'forward.apng',save_all=True,append_images=row[1:],duration=timing['frameDurationsMs'],loop=0,disposal=0,blend=0)
    decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(O/'forward.apng'))];assert len(decoded)==5
    for f,p in zip(decoded,row):assert f.tobytes()==p.tobytes()
    board=Image.new('RGB',(1840,430),'#293b40');d=ImageDraw.Draw(board)
    for i,f in enumerate(row):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,45),large);d.text((i*368+4,5),('Exact staged '+origin if i==0 else 'Exact staged '+dest if i==4 else f'Whole intermediate {i} / yaw provisional'),fill='white')
    board.save(O/'comparison.png');idle=Image.open(ROOT/g['primaryIdles'][dest]['path']).convert('RGBA');board=Image.new('RGB',(736,430),'#293b40');d=ImageDraw.Draw(board)
    for i,f in enumerate([idle,poses[3]]):large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(i*368,45),large);d.text((i*368+4,5),['Selected destination idle PRIMARY','Unobstructed neutral ruler'][i],fill='white')
    board.save(O/'neutral-comparison.png')
    (O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'commonNeutralScale':scale,'neutralOccupiedTargetHeight':req['neutralOccupiedTargetHeight'],'rawSha256':sha(rawpath),'records':records,'stagedEndpoints':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in endpoints],'endpointChestMidX':target,'exactEndpointCopies':4,'reverseWholeFrameOrder':True,'apngExactDecodedFrames':5,'operations':'Four complete alpha128 cells,ONE unobstructed neutral BOX scale,no clipped opaque pixels. Whole integer torso-row registration interpolated from unchanged endpoint chest-row midpoints;not independent bbox centering. Generic bbox bottom172 is not anatomical sole proof. No mirror,patch,recolour or per-pose/cargo-width fit. Three authored poses and exact endpoints,reverse whole order only.','limits':'Head/body/crate yaw and material/registration/temporal joins provisional. Source packaging only;no native/full-save/normal admission.'},indent=2)+'\n')
    print(json.dumps({'commonNeutralScale':scale,'sizes':[r['occupiedSize'] for r in records],'unchangedEndpointCopies':4,'reverseStates':2,'apngExactDecodedFrames':5,'normalAdmission':False}))
if __name__=='__main__':main()
