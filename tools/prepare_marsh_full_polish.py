"""Frozen-source material grading, with content-identical shared joins preserved."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-full-polish-v1'
DIRECTIONS=('south','north','east','west')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def material_mask(image):
    a=np.asarray(image);rgb=a[:,:,:3].astype(float);lum=rgb.mean(2)
    # Ivory panels; exclude sage, graphite, skin, hair, white fluid and lights.
    mask=(a[:,:,3]>0)&(rgb[:,:,0]>=rgb[:,:,1])&(rgb[:,:,0]-rgb[:,:,1]<=25)&(rgb[:,:,0]-rgb[:,:,2]<65)&(rgb[:,:,0]-rgb[:,:,2]>12)&(lum>105)&(lum<230)
    warm=(a[:,:,3]>0)&(rgb[:,:,0]-rgb[:,:,1]>20)&(rgb[:,:,0]-rgb[:,:,2]>45)
    labs,n=label(warm);counts=np.bincount(labs.ravel());counts[0]=0
    protected=np.zeros(mask.shape,bool)
    for c in np.flatnonzero(counts>=8):
        y,x=np.where(labs==c)
        if y.min()>image.getbbox()[1]+30:continue
        protected[max(0,y.min()-5):min(mask.shape[0],y.max()+6),max(0,x.min()-5):min(mask.shape[1],x.max()+6)]=True
    mask&=~binary_dilation(protected,iterations=2)
    return mask,lum,protected

def family(key):
    a=key.rsplit('-',1)[0]
    if key.startswith(('idle-','walk')):return 'reference'
    if key.startswith(('swim-carry','swim-pickup','cargo-drain')):return 'loaded-water'
    if key.startswith(('swim','tread','death-water')):return 'water'
    if a in ('sit-down','sit-idle','sit-rise','read-seated'):return 'seated'
    if a in ('eat','drink'):return 'galley'
    if a=='death-ground':return 'ground-shutdown'
    if a=='recover-air':return 'recovery'
    if a in ('torch-draw','torch-stow','weld'):return 'welding'
    if a in ('carry','pickup','unload','cargo-unload') or key.startswith('carry-turn'):return 'cargo'
    if a=='run':return 'run'
    if a in ('kneel','repair','stand','interact','inspect','salvage'):return 'diagnostic'
    return 'rest'

def grade(image,gain,mapper):
    mask,lum,protected=material_mask(image);a=np.asarray(image).copy();b=a.copy()
    weight=np.clip((lum-105)/35,0,1)*mask
    if gain!=1.0:
        b[:,:,:3]=np.clip(np.rint(a[:,:,:3]*(1+weight[:,:,None]*(gain-1))),0,255).astype('uint8')
        mapped=np.asarray(mapper(Image.fromarray(b)));b[mask]=mapped[mask]
    return Image.fromarray(b),mask,protected,gain

def prepare():
    BASE.mkdir(parents=True,exist_ok=True)
    frozen=BASE/'baseline-contract.json'
    if not frozen.exists():
        shutil.copy2(ROOT/'character/marsh-consistency-review-v1/runtime-contract.json',frozen)
        for s in json.loads(frozen.read_text())['states'].values():
            for f in s['files']:
                p=BASE/'original'/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/f,p)
        cat=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())
        for path in cat['body']:
            rel='character/marsh-v2/'+path;p=BASE/'original'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,p)
    contract=json.loads(frozen.read_text());states=contract['states'];donors={};refs={};identities={};allrows=[]
    priority={'reference':0,'cargo':1,'diagnostic':2,'galley':3,'run':4,'seated':5,'rest':6,'welding':7,'recovery':8,'water':9,'ground-shutdown':10,'loaded-water':11}
    for k,s in states.items():
        d=k.rsplit('-',1)[-1];group=family(k)
        if '-turn-' in k:d=k.split('-')[-1]
        for i,(f,h) in enumerate(zip(s['files'],s['hashes'])):
            orig=BASE/'original'/f;assert sha(orig)==h
            im=Image.open(orig).convert('RGBA');mask,lum,protected=material_mask(im)
            if d in DIRECTIONS and mask.sum()>80 and '-turn-' not in k:
                donors.setdefault((group,d),[]).append(float(lum[mask].mean()))
            if k.startswith('idle-') and i==0:refs[d]=float(lum[mask].mean())
            # Joins may pad the same pose into a taller swimming-turn canvas.
            # Compare actual artwork, independently of transparent padding.
            crop=im.crop(im.getbbox());visual_hash=hashlib.sha256(str(crop.size).encode()+crop.tobytes()).hexdigest()
            if visual_hash not in identities or priority[group]<priority[identities[visual_hash][0]]:identities[visual_hash]=(group,d)
            allrows.append((k,i,f,h,visual_hash))
    gains={};measurements={}
    for (group,d),means in donors.items():
        donor=float(np.median(means));target=refs[d];gap=donor-target
        # Preserve accepted locomotion and welding's local tool illumination.
        gain=1.0 if group in ('reference','welding','diagnostic','cargo','rest') or abs(gap)<8 else float(np.clip(target/donor,.84,1.08))
        gains[(group,d)]=gain;measurements[group+'-'+d]={'reference':target,'donorMedian':donor,'gain':gain}
    mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
    cache={};records={};selection={};changed=0
    for k,i,f,h,visual_hash in allrows:
        orig=BASE/'original'/f;out=BASE/f'frames/{k}/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True)
        group,d=identities[visual_hash];gain=gains.get((group,d),1.0)
        if h not in cache:
            cache[h]=grade(Image.open(orig).convert('RGBA'),gain,mapper)
        im,mask,protected,gain=cache[h]
        if gain==1:shutil.copy2(orig,out)
        else:im.save(out)
        maskpath=BASE/f'masks/{k}/{i:03}.png';maskpath.parent.mkdir(parents=True,exist_ok=True);Image.fromarray((mask if gain!=1 else np.zeros(mask.shape,bool)).astype('uint8')*255).save(maskpath)
        source=out.relative_to(ROOT).as_posix();after=sha(out)
        selection.setdefault(k,[]).append(source)
        if after!=h:
            changed+=1;record={'before':h,'after':after,'source':source,'original':orig.relative_to(ROOT).as_posix(),'mask':maskpath.relative_to(ROOT).as_posix(),'gain':gain,'family':group,'reason':'Fixed family/direction ivory material grade; identity, geometry, alpha and detail preserved'}
            if f in records:assert records[f]['after']==after
            records[f]=record
    changed_states=[k for k,s in states.items() if any(f in records for f in s['files'])]
    staged={}
    for d in DIRECTIONS:
        staged['injury-ground-'+d]=[]
        for i in range(6):
            orig=ROOT/f'character/marsh-shutdown-injury-match-v1/frames/injury-ground-{d}/{i:03}.png';out=BASE/f'frames/injury-ground-{d}/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True)
            gain=1.0 if i==0 else gains.get(('ground-shutdown',d),1.0)
            if gain==1:shutil.copy2(orig,out)
            else:grade(Image.open(orig).convert('RGBA'),gain,mapper)[0].save(out)
            staged['injury-ground-'+d].append(out.relative_to(ROOT).as_posix())
    (BASE/'selection.json').write_text(json.dumps({'states':selection,'changedStates':changed_states,'stagedFrames':staged,'stagedInjury':'Separate preview only; same ground shutdown grade; white fluid retained'},indent=2)+'\n')
    (BASE/'colour-lock.json').write_text(json.dumps(records,indent=2)+'\n')
    (BASE/'grading.json').write_text(json.dumps({'fits':measurements,'changedSlots':changed,'changedPaths':len(records),'policy':'Fixed family/direction gain; identical source content shares one result; no resizing, detail reduction or global tint'},indent=2)+'\n')
    print(len(states),'states reviewed;',changed,'graded slots;',len(records),'changed runtime paths')

def install():
    selection=json.loads((BASE/'selection.json').read_text())['states'];states=json.loads((BASE/'baseline-contract.json').read_text())['states']
    for k,files in selection.items():
        for f,s in zip(states[k]['files'],files):
            if sha(ROOT/f)!=sha(ROOT/s):shutil.copy2(ROOT/s,ROOT/f)

if __name__=='__main__':prepare()
