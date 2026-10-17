"""Deterministic source extraction only; never draws or invents animation poses."""
from pathlib import Path
import hashlib
import json
import statistics
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT=Path(__file__).resolve().parent
jobs=json.loads((ROOT/'prompts.json').read_text(encoding='utf-8'))
states=[]; checks=[]; contact=[]
timings={'idle-south':[260,220,240,220,240,260], 'walk-east':[170,130,150,170,130,150], 'interact-east':[180,120,140,260,140,180]}
for job in jobs:
    sid=job['id']; source=ROOT/'sources'/f'{sid}-01.png'
    im=Image.open(source).convert('RGBA'); pixels=np.array(im); a=pixels[:,:,3]
    background_method='source-alpha-threshold'
    if sid=='walk-east' and pixels[0,0,0]>200 and pixels[0,0,1]<80 and pixels[0,0,2]>200:
        key=(pixels[:,:,0]>180)&(pixels[:,:,1]<110)&(pixels[:,:,2]>180)
        a=np.where(key,0,255).astype('uint8');im.putalpha(Image.fromarray(a));background_method='flat-magenta-key'
    assert np.mean(a<8)>.10, f'{sid}: no substantial alpha transparency'
    # Sources need not follow exact nominal cell boundaries. Extract isolated bodies.
    labels,count=ndimage.label(a>=128); sizes=np.bincount(labels.ravel()); objects=ndimage.find_objects(labels)
    selected=[(i+1,b) for i,b in enumerate(objects) if b is not None and sizes[i+1]>1000]
    assert len(selected)==job['frames'],f'{sid}: expected isolated bodies, got {len(selected)}'
    selected.sort(key=lambda pair:pair[1][0].start)
    ordered=[]
    for row in range(job['rows']):
        group=selected[row*job['cols']:(row+1)*job['cols']]
        ordered.extend(sorted(group,key=lambda pair:pair[1][1].start))
    cells=[]; source_boxes=[]
    for label,(ys,xs) in ordered:
        box=(xs.start,ys.start,xs.stop,ys.stop)
        assert box[0]>1 and box[1]>1 and box[2]<im.width-1 and box[3]<im.height-1,f'{sid}: source clipped'
        cell=im.crop(box); cell.putalpha(Image.fromarray(np.where(labels[ys,xs]==label,255,0).astype('uint8')))
        cells.append((cell,(0,0,cell.width,cell.height)));source_boxes.append(box)
    scale=148/statistics.median(b[3]-b[1] for _,b in cells)
    paths=[]; bounds=[]
    folder=ROOT/'frames'/sid;folder.mkdir(parents=True,exist_ok=True)
    for i,(cell,box) in enumerate(cells):
        # Anchor torso centre rather than moving arm/stride extremes. One clip-wide scale.
        alpha=np.array(cell.getchannel('A')); y0=int(box[1]+(box[3]-box[1])*.30);y1=int(box[1]+(box[3]-box[1])*.53)
        _,xs=np.nonzero(alpha[y0:y1]); anchor=float(np.median(xs))
        cropped=cell.crop(box); size=(round(cropped.width*scale),round(cropped.height*scale))
        small=cropped.resize(size,Image.Resampling.LANCZOS)
        small.putalpha(small.getchannel('A').point(lambda v:255 if v>=128 else 0))
        out=Image.new('RGBA',(184,184));left=round(92-(anchor-box[0])*scale);top=172-size[1]
        assert left>=2 and top>=2 and left+size[0]<=182, f'{sid}/{i}: frame clipping'
        out.alpha_composite(small,(left,top));path=folder/f'{i:03}.png';out.save(path)
        paths.append(str(path.relative_to(ROOT)).replace('\\','/'));bounds.append(out.getbbox());contact.append((sid,i,out))
    states.append({'id':sid,'frameFiles':paths,'frameCount':len(paths),'frameDurationsMs':timings[sid], 'loop':sid!='interact-east','source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'mirrored':False,'extractionScale':scale})
    checks.append({'state':sid,'sourceSize':im.size,'backgroundMethod':background_method,'sourceBoxes':source_boxes,'transparentFraction':float(np.mean(a==0)),'bounds':bounds,'heightRange':[min(b[3]-b[1] for b in bounds),max(b[3]-b[1] for b in bounds)]})
manifest={'name':'veld-new-design-motion-pilot','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'status':'review_candidate_not_installed','palettePolicy':'Source colours retained for motion pilot; exact material palette remap remains pending.','strideDistanceCells':{'walk':.11716216216216217},'states':states}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
sheet=Image.new('RGB',(8*184,3*212),'#263038');draw=ImageDraw.Draw(sheet)
for row,state in enumerate(states):
    for i,p in enumerate(state['frameFiles']):
        frame=Image.open(ROOT/p).convert('RGBA');sheet.paste(frame,(i*184,row*212),frame);draw.text((i*184+8,row*212+188),f"{state['id']} {i}",fill='white')
sheet.save(ROOT/'contact-sheet.png')
old_root=ROOT.parent/'dr-veld-v2'
old_manifest=old_root/'packs/bare-184x184-p92.0-172.0/manifest.json'
old_data=json.loads(old_manifest.read_text(encoding='utf-8'))
preview=ROOT/'preview';preview.mkdir(exist_ok=True)
for state in states:
    frames=[Image.open(ROOT/p).convert('RGBA') for p in state['frameFiles']]
    frames[0].save(preview/f"{state['id']}-new.webp",save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,lossless=True)
    old=next(s for s in old_data['states'] if s['id']==state['id'])
    old_frames=[Image.open(old_manifest.parent/p).convert('RGBA') for p in old['frameFiles']]
    old_frames[0].save(preview/f"{state['id']}-old.webp",save_all=True,append_images=old_frames[1:],duration=[round(d) for d in old['frameDurationsMs']],loop=0,lossless=True)
print(f'Extracted {sum(s["frameCount"] for s in states)} frames in {len(states)} clips; no runtime files touched.')
