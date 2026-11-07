"""Package coherent generated North gait materials inside frozen motion geometry."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_full_polish import material_mask,grade
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-walk-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    raw=Image.open(BASE/'sources/north-walk-01.png').convert('RGBA')
    assert raw.size==(1536,1024)
    baseline=json.loads((BASE/'baseline.json').read_text())['states']
    document=json.loads((BASE/'edit-plan.json').read_text());plan=document['poses']
    mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
    candidates=[];records=[]
    for p in plan:
        slot=p['slot'];cell=raw.crop((slot%3*512,slot//3*512,slot%3*512+512,slot//3*512+512))
        a=np.array(cell);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
        cell=Image.fromarray(a);box=cell.getbbox()
        assert box is not None
        original=Image.open(BASE/f'sources/original-{slot:03d}.png').convert('RGBA')
        assert sha(BASE/f'sources/original-{slot:03d}.png')==p['sha256']
        ob=original.getbbox();tile=cell.crop(box).resize((ob[2]-ob[0],ob[3]-ob[1]),Image.Resampling.LANCZOS)
        b=np.array(mapper(tile));o=np.array(original.crop(ob));valid=(b[:,:,3]>=128)&(o[:,:,3]>0)
        out=o.copy();out[valid,:3]=b[valid,:3];out[:,:,3]=o[:,:,3]
        frame=original.copy();frame.paste(Image.fromarray(out),ob[:2]);candidates.append(frame)
        records.append({'slot':slot,'generatedBox':box,'originalBox':ob,'source':p['path'],'sourceSha256':p['sha256'],'visiblePixels':int((o[:,:,3]>0).sum()),'mappedPixels':int(valid.sum())})
    idle=Image.open(ROOT/baseline['idle-north']['files'][0]).convert('RGBA')
    mask,lum,_=material_mask(idle);target=float(lum[mask].mean())
    values=[]
    for im in candidates:
        m,l,_=material_mask(im);values.append(float(l[m].mean()))
    median=float(np.median(values));gain=float(np.clip(target/median,.9,1.06)) if abs(target-median)>=5 else 1.0
    output=BASE/'candidate-01';output.mkdir(exist_ok=True)
    frames=[]
    board=Image.new('RGB',(184*8,480),'#293b40');draw=ImageDraw.Draw(board)
    for slot,im in enumerate(candidates):
        result=grade(im,gain,mapper)[0]
        old=Image.open(BASE/f'sources/original-{slot:03d}.png').convert('RGBA')
        assert np.array_equal(np.array(result)[:,:,3],np.array(old)[:,:,3])
        path=output/f'{slot:03d}.png';result.save(path);frames.append(path.name)
        records[slot].update({'candidateSha256':sha(path),'gain':gain,'ivoryMeanBefore':values[slot]})
        m,l,_=material_mask(result);records[slot]['ivoryMeanAfter']=float(l[m].mean())
        for row,image in enumerate((old,result)):
            x=(slot+2)*184;y=row*240;board.paste(image,(x,y+28),image)
            draw.text((x+3,y+6),f'{"Before" if row==0 else "Candidate"} gait{slot}',fill='white')
            draw.line((x+3,y+200,x+179,y+200),fill='#839597')
    for row in range(2):
        board.paste(idle,(0,row*240+28),idle);draw.text((4,row*240+6),'Selected idle',fill='white')
        start=Image.open(ROOT/'character/marsh-ground-cardinal-v1/north-start-candidate-01/003.png').convert('RGBA')
        board.paste(start,(184,row*240+28),start);draw.text((188,row*240+6),'New start toe-off',fill='white')
    board.save(output/'comparison.png')
    oldspec=baseline['walk-north']
    state=dict(document['selectedEntry']['state']);state['frameFiles']=frames
    manifest=dict(document['selectedEntry']['manifest']);manifest['name']='marsh-north-walk-material-v1';manifest['states']=[state]
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    source=BASE/'sources/north-walk-01.png';prompt=BASE/'sources/north-walk-01.prompt.txt'
    recipe={'status':'staged-review-pending','generation':'built-in imagegen exec-51f03fc5-e055-4f94-a419-00a6e16e8d27','prompt':prompt.relative_to(ROOT).as_posix(),'promptSha256':sha(prompt),'editedSheet':source.relative_to(ROOT).as_posix(),'editedSheetSha256':sha(source),'references':[{'path':p,'sha256':sha(ROOT/p)} for p in ['character/marsh-north-walk-material-v1/sources/north-walk-edit-input.png','character/marsh-motion-polish-v1/sources/north-standing-identity-01.png',baseline['idle-north']['files'][0],'character/marsh-ground-cardinal-v1/sources/north-start-01.png']],'extract':'128 alpha; six explicit3x2cells; corresponding full-body bounds mapped to original bounds; original alpha retained exactly; standard palette; one pooled ivory gain','ivoryTarget':target,'pooledCandidateMedian':median,'gain':gain,'frames':records,'limits':'Material/detail revision preserves original alpha geometry and source phase, not newly authored gait motion. Root/controller and final visual acceptance separate.'}
    (output/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    # Stage a matched start endpoint; preserve original candidate/history separately.
    start_output=output/'north-start';start_output.mkdir(exist_ok=True)
    start_source=ROOT/'character/marsh-ground-cardinal-v1/north-start-candidate-01'
    for i in range(4):(start_output/f'{i:03d}.png').write_bytes((start_source/f'{i:03d}.png').read_bytes())
    (start_output/'004.png').write_bytes((output/'001.png').read_bytes())
    start_manifest=json.loads((start_source/'manifest.json').read_text())
    (start_output/'manifest.json').write_text(json.dumps(start_manifest,indent=2)+'\n')
    print(f'Six North gait material candidates; original alpha,150ms slots,pivot/density retained; pooled gain{gain:.4f}')
if __name__=='__main__':main()
