"""Correct ivory controller-panel brightness with fixed directional material gains."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-controller-tone-v1';ORIGINAL=ROOT/'character/marsh-maintenance-match-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def panel_mask(image):
    a=np.asarray(image);rgb=a[:,:,:3].astype(float);lum=rgb.mean(2);top=image.getbbox()[1]
    mask=(a[:,:,3]>0)&(rgb[:,:,0]>=rgb[:,:,1])&(rgb[:,:,0]-rgb[:,:,1]<=25)&(rgb[:,:,0]-rgb[:,:,2]<65)&(lum>100)
    mask[:top+30]=False
    return mask,lum
def transform(image,gain,mapper):
    a=np.asarray(image).copy();mask,lum=panel_mask(image);weight=np.clip((lum-100)/35,0,1)*mask
    b=a.copy();b[:,:,:3]=np.clip(np.rint(a[:,:,:3]*(1+weight[:,:,None]*(gain-1))),0,255).astype('uint8');mapped=np.asarray(mapper(Image.fromarray(b))).copy();b[mask]=mapped[mask]
    assert np.array_equal(a[~mask],b[~mask]);assert np.array_equal(a[:,:,3],b[:,:,3]);return Image.fromarray(b),mask

def prepare():
    BASE.mkdir(parents=True,exist_ok=True)
    if not (BASE/'contract.json').exists():
        states={}
        catalog=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text())
        for path in catalog['body']:
            manifest=ROOT/'character/marsh-v2'/path
            for state in json.loads(manifest.read_text())['states']:
                if state['id'].rsplit('-',1)[0] in ('interact','kneel','repair','stand'):
                    states[state['id']]={'manifest':manifest.relative_to(ROOT).as_posix(),'metadata':state,'files':[(manifest.parent/f).resolve().relative_to(ROOT).as_posix() for f in state['frameFiles']]}
        (BASE/'contract.json').write_text(json.dumps({'states':states},indent=2)+'\n')
    contract=json.loads((BASE/'contract.json').read_text())
    mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()));directions={};records={};board=Image.new('RGB',(552,232*4),'#293b40');draw=ImageDraw.Draw(board)
    for row,d in enumerate(('south','north','east','west')):
        idle=Image.open(ROOT/f'character/marsh-v2/frames/bare/idle-{d}/000.png').convert('RGBA');donor=Image.open(ORIGINAL/f'frames/repair-{d}/002.png').convert('RGBA');imask,ilum=panel_mask(idle);mask,lum=panel_mask(donor);target=float(ilum[imask].mean());weight=np.clip((lum[mask]-100)/35,0,1);gain=float(np.clip(1+(target-float(lum[mask].mean()))/float((lum[mask]*weight).mean()),.70,1.0))
        corrected,_=transform(donor,gain,mapper);result=np.asarray(corrected)[:,:,:3].mean(2);directions[d]={'gain':gain,'referenceMean':target,'beforeMean':float(lum[mask].mean()),'afterMeanOnOriginalMask':float(result[mask].mean()),'material':'ivory panels only; protect top 30 body rows and all pixels outside panel mask'}
        for col,im in enumerate((idle,donor,corrected)):board.paste(im,(184*col,row*232+24),im);draw.text((184*col+4,row*232+4),d+' '+('idle','before','after')[col],fill='white')
        for key,info in contract['states'].items():
            if not key.endswith('-'+d):continue
            for i,target_path in enumerate(info['files']):
                source=ORIGINAL/f'frames/{key}/{i:03}.png';image=Image.open(source).convert('RGBA');same_idle=image.tobytes()==idle.tobytes();corrected,mask=transform(image,1.0 if same_idle else gain,mapper)
                if same_idle:corrected=image.copy();mask[:]=False
                dest=BASE/f'frames/{key}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);corrected.save(dest);mask_path=BASE/f'masks/{key}/{i:03}.png';mask_path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(mask_path)
                records[target_path]={'before':sha(source),'after':sha(dest),'source':dest.relative_to(ROOT).as_posix(),'originalSource':source.relative_to(ROOT).as_posix(),'mask':mask_path.relative_to(ROOT).as_posix(),'gain':1.0 if same_idle else gain,'reason':'Fixed directional ivory-panel gain matched to selected idle; head, alpha, geometry and outside-mask pixels exact'}
    board.save(BASE/'comparison.png');(BASE/'correction.json').write_text(json.dumps({'directions':directions,'frames':records},indent=2)+'\n');print(json.dumps(directions))

def install(backup=False):
    records=json.loads((BASE/'correction.json').read_text())['frames'];contract=json.loads((BASE/'contract.json').read_text())
    for rel,r in records.items():
        target=ROOT/rel
        if backup:
            assert sha(target)==r['before'],rel;saved=BASE/'installation-backup'/rel;assert not saved.exists();saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
        shutil.copy2(ROOT/r['source'],target)
    if backup:
        for rel in {v['manifest'] for v in contract['states'].values()}:
            saved=BASE/'installation-backup'/rel;saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,saved)
        (BASE/'colour-lock.json').write_text(json.dumps(records,indent=2)+'\n');(BASE/'installation.json').write_text(json.dumps({'frameCount':len(records),'frames':records},indent=2)+'\n')
    return records
if __name__=='__main__':prepare()
