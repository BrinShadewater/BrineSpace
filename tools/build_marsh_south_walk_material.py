"""Package a coherent generated South material revision in frozen gait geometry."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw
from prepare_marsh_full_polish import material_mask,grade
from prepare_marsh_carry_chain import palette_module
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-walk-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    grid='--grid' in sys.argv
    rawpath=BASE/('sources/south-walk-02.raw.png' if grid else 'sources/south-walk-01.raw.png');raw=Image.open(rawpath).convert('RGBA');w,h=raw.size
    baseline=json.loads((BASE/'baseline.json').read_text());mapper=palette_module().remapper(json.loads((ROOT/'character/palette-standard-v1/palettes/marsh.json').read_text()))
    records=[];candidates=[];originals=[]
    for p in baseline['states']:
        slot=p['slot'];path=ROOT/p['path'];assert sha(path)==p['sha256'],path
        old=Image.open(path).convert('RGBA');ob=old.getbbox()
        bounds=(slot%3*w//3,slot//3*h//2,(slot%3+1)*w//3,(slot//3+1)*h//2) if grid else (slot*w//6,0,(slot+1)*w//6,h)
        cell=raw.crop(bounds);a=np.array(cell);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);a[a[:,:,3]==0]=0
        cell=Image.fromarray(a);box=cell.getbbox();assert box is not None
        tile=cell.crop(box).resize((ob[2]-ob[0],ob[3]-ob[1]),Image.Resampling.LANCZOS)
        b=np.array(mapper(tile));o=np.array(old.crop(ob));valid=(b[:,:,3]>=128)&(o[:,:,3]>0)
        out=o.copy();out[valid,:3]=b[valid,:3];out[:,:,3]=o[:,:,3]
        frame=old.copy();frame.paste(Image.fromarray(out),ob[:2]);candidates.append(frame);originals.append(old)
        records.append({'slot':slot,'cell':bounds,'generatedBounds':box,'originalBounds':ob,'originalSha256':p['sha256'],'visiblePixels':int((o[:,:,3]>0).sum()),'mappedPixels':int(valid.sum()),'mappingCoverage':float(valid.sum()/(o[:,:,3]>0).sum())})
    idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-south/000.png').convert('RGBA')
    mask,lum,_=material_mask(idle);target=float(lum[mask].mean());values=[]
    for im in candidates:m,l,_=material_mask(im);values.append(float(l[m].mean()))
    median=float(np.median(values));gain=float(np.clip(target/median,.9,1.06)) if abs(target-median)>=5 else 1.0
    out=BASE/('candidate-02' if grid else 'candidate-01');out.mkdir(exist_ok=True);board=Image.new('RGB',(1472,480),'#293b40');draw=ImageDraw.Draw(board)
    for slot,im in enumerate(candidates):
        result=grade(im,gain,mapper)[0];assert np.array_equal(np.array(result)[:,:,3],np.array(originals[slot])[:,:,3])
        file=out/('%03d.png'%slot);result.save(file);records[slot].update({'sha256':sha(file),'ivoryMeanBefore':values[slot],'sharedGain':gain})
        m,l,_=material_mask(result);records[slot]['ivoryMeanAfter']=float(l[m].mean())
        for row,frame in enumerate([originals[slot],result]):
            x=(slot+2)*184;y=row*240;board.paste(frame,(x,y+28),frame);draw.text((x+2,y+5),('old ' if row==0 else 'repair ')+str(slot),fill='white')
    for row in range(2):
        for i,p in enumerate(['character/marsh-v2/frames/bare/idle-south/000.png','character/marsh-south-start-v1/candidate-04/003.png']):
            frame=Image.open(ROOT/p).convert('RGBA');board.paste(frame,(i*184,row*240+28),frame);draw.text((i*184+2,row*240+5),'idle' if i==0 else 'staged start3',fill='white')
    board.save(out/'comparison.png')
    catalog=json.loads((ROOT/'character/marsh-v2/catalog.json').read_text());selected=None
    for path in catalog['body']:
        data=json.loads((ROOT/'character/marsh-v2'/path).read_text())
        for state in data['states']:
            if state['id']=='walk-south':selected={'manifest':{k:v for k,v in data.items() if k!='states'},'state':state}
    assert selected is not None
    state=selected['state'];state['frameFiles']=['%03d.png'%i for i in range(6)]
    manifest=selected['manifest'];manifest['states']=[state];(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    start=out/'south-start';start.mkdir(exist_ok=True)
    for i in range(4):(start/('%03d.png'%i)).write_bytes((ROOT/'character/marsh-south-start-v1/candidate-04'/('%03d.png'%i)).read_bytes())
    (start/'004.png').write_bytes((out/'004.png').read_bytes())
    (start/'manifest.json').write_bytes((ROOT/'character/marsh-south-start-v1/candidate-04/manifest.json').read_bytes())
    recipe={'status':'unselected material candidate; static/native joins pending','rawSha256':sha(rawpath),'frames':records,'ivoryTarget':target,'pooledCandidateMedian':median,'sharedIvoryGain':gain,'method':'Whole generated pose RGB mapped to corresponding original full-body bounds; original alpha geometry exactly retained; transparent mapped holes retain original pixels. Standard palette; one pooled ivory gain, never per-frame normalization. No limb/head patches or motion edits. This is internal material/detail mapping, not independently rescaled actor geometry. Inspect generated head/panel placement against preserved outline before accepting.','startEndpoint':'candidate01 gait4 byte-identical to staged south-start004; first4 start frames unchanged from candidate04','limits':'Not normal catalog selection, new motion authorship, native acceptance, service/safety/save/title Continue or cross-family completion.'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    print('Six frozen-alpha South gait candidates; shared gain',round(gain,4),'coverage',[round(r['mappingCoverage'],3) for r in records])
if __name__=='__main__':main()
