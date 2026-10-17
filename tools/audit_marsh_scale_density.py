"""Freeze every current pose; publish common-ruler size/density review without resizing art."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
from publish_marsh_gesture_review import selected,resolve

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-scale-density-review-2026-10-14'
OUT=BASE/'review'

def registered(record,slot):
    p,m,s=record;im=Image.open(resolve(p.parent,s['frameFiles'][slot])).convert('RGBA')
    out=Image.new('RGBA',(280,288));offset=(140-round(m['pivot'][0]),224-round(m['pivot'][1]))
    b=im.getbbox()
    assert b and b[0]+offset[0]>=0 and b[1]+offset[1]>=0 and b[2]+offset[0]<=280 and b[3]+offset[1]<=288
    out.paste(im,offset);return out

def main():
    BASE.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True);d=selected();cache={};frames=[];contract={}
    for key,(p,m,s) in d.items():
        assert m['standingHeight']==148
        assert m.get('textureFilter','nearest')=='nearest'
        assert len(s['frameFiles'])==len(s['frameDurationsMs']) and all(t>0 for t in s['frameDurationsMs'])
        for i,f in enumerate(s['frameFiles']):
            path=resolve(p.parent,f)
            if path not in cache:
                im=Image.open(path).convert('RGBA');a=np.array(im);alpha=a[:,:,3];mask=alpha>160;y,x=np.where(mask)
                cache[path]={'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'canvas':list(im.size),'coreBounds':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'partialAlphaFraction':round(float(((alpha>0)&(alpha<255)).sum())/int((alpha>0).sum()),4),'coreMedianAlpha':float(np.median(alpha[mask])),'opaqueColors':len(np.unique(a[mask,:3],axis=0))}
            registered(d[key],i)
            frames.append({'state':key,'slot':i,'pivot':m['pivot'],'standingHeight':m['standingHeight'],'duration':s['frameDurationsMs'][i],**cache[path]})
        contract[key]={'manifest':p.relative_to(ROOT).as_posix(),'metadata':{k:v for k,v in m.items() if k!='states'},'state':s,'files':[cache[resolve(p.parent,f)] for f in s['frameFiles']]}
    frozen=BASE/'selected-before.json'
    if frozen.exists():assert json.loads(frozen.read_text())==contract,'Selection changed since scale audit freeze'
    else:frozen.write_text(json.dumps(contract,indent=2)+'\n')
    # Keep the initial exploratory measurements separate. Counts of warm-colour
    # components are not head anatomy or proof of pixel-density differences.
    inventory={'states':len(d),'holds':len(frames),'uniqueSources':len(cache),'standingRuler':148,'nominalWorldHeight':384*.17,'sourcePixelsPerWorldUnit':148/(384*.17),'frames':frames}
    (BASE/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    keys=list(d)
    for page in range(math.ceil(len(keys)/16)):
        board=Image.new('RGB',(1120,1600),'#26333c');draw=ImageDraw.Draw(board)
        for col,direction in enumerate(['south','north','east','west']):
            im=registered(d['idle-'+direction],0);board.paste(im,(col*280,24),im);draw.text((col*280+4,4),'REFERENCE / idle-'+direction,fill='white')
        for n,key in enumerate(keys[page*16:page*16+16]):
            slot=len(d[key][2]['frameFiles'])//2;col=n%4;row=n//4+1;im=registered(d[key],slot)
            board.paste(im,(col*280,row*320+24),im);draw.text((col*280+4,row*320+4),key+'/'+str(slot),fill='white')
        board.save(BASE/f'atlas-{page:02}.png')
    # Original PNG references retain all native pixels, alpha, aspect and pivots.
    # The local viewer uses Image loading, not fetch, so it works from file URLs.
    viewer={}
    for key,record in contract.items():
        viewer[key]={'pivot':record['metadata']['pivot'],'height':148,'durations':record['state']['frameDurationsMs'],'loop':record['state']['loop'],'facings':record['state'].get('facings',[]),'files':['../../../'+f['path'] for f in record['files']]}
    template=(ROOT/'tools/marsh_scale_density_review.html').read_text(encoding='utf-8')
    (OUT/'index.html').write_text(template.replace('__DATA__',json.dumps(viewer)),encoding='utf-8')
    (OUT/'review-data.json').write_text(json.dumps(viewer,indent=2)+'\n')
    print(f'{len(d)} states / {len(frames)} holds / {len(cache)} unique sources: uniform148 ruler, nearest sampling, complete registered alpha bounds; no artwork changed')

if __name__=='__main__':main()
