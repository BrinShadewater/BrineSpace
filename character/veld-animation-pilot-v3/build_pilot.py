"""Deterministic source extraction only; never draws or invents animation poses."""
from pathlib import Path
import hashlib
import json
import statistics
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from brightness import measure, match
from materials import apply as apply_materials

ROOT=Path(__file__).resolve().parent
jobs=json.loads((ROOT/'prompts.json').read_text(encoding='utf-8'))
states=[]; checks=[]; contact=[]; targets=None; brightness_checks=[]; material_checks=[]
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
    if targets is None:
        measured=[measure(cell) for cell,_ in cells]
        targets={k:statistics.median(m[k] for m in measured) for k in measured[0]}
    paths=[]; bounds=[]; scales=[]
    folder=ROOT/'frames'/sid;folder.mkdir(parents=True,exist_ok=True)
    for i,(cell,box) in enumerate(cells):
        # Standing inspection source rows have inconsistent drawing scale, not a crouch.
        # Correct those stationary figures to 148px; retain clip-wide scale for gait.
        frame_scale=148/cell.height if sid in ('idle-south','interact-east') else scale
        scales.append(frame_scale)
        cell,brightness_report=match(cell,targets)
        brightness_checks.append({'state':sid,'frame':i,**brightness_report})
        cell,mask,report=apply_materials(cell)
        mask_folder=ROOT/'material-masks'/sid;mask_folder.mkdir(parents=True,exist_ok=True)
        mask.save(mask_folder/f'{i:03}.png')
        material_checks.append({'state':sid,'frame':i,**report})
        # Head band excludes moving arms; neck/head registration avoids arm-induced drift.
        alpha=np.array(cell.getchannel('A')); y0=int(cell.height*.05);y1=int(cell.height*.14)
        _,xs=np.nonzero(alpha[y0:y1]); anchor=float(np.median(xs))
        cropped=cell.crop(box); size=(round(cropped.width*frame_scale),round(cropped.height*frame_scale))
        small=cropped.resize(size,Image.Resampling.LANCZOS)
        small.putalpha(small.getchannel('A').point(lambda v:255 if v>=128 else 0))
        out=Image.new('RGBA',(184,184));left=round((92 if sid=='idle-south' else 100)-(anchor-box[0])*frame_scale);top=172-size[1]
        assert left>=2 and top>=2 and left+size[0]<=182, f'{sid}/{i}: frame clipping'
        out.alpha_composite(small,(left,top));path=folder/f'{i:03}.png';out.save(path)
        paths.append(str(path.relative_to(ROOT)).replace('\\','/'));bounds.append(out.getbbox());contact.append((sid,i,out))
    states.append({'id':sid,'frameFiles':paths,'frameCount':len(paths),'frameDurationsMs':timings[sid], 'loop':sid!='interact-east','source':str(source.relative_to(ROOT)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'mirrored':False,'extractionScales':scales})
    checks.append({'state':sid,'sourceSize':im.size,'backgroundMethod':background_method,'sourceBoxes':source_boxes,'transparentFraction':float(np.mean(a==0)),'bounds':bounds,'heightRange':[min(b[3]-b[1] for b in bounds),max(b[3]-b[1] for b in bounds)]})
manifest={'name':'veld-new-design-motion-pilot','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'status':'review_candidate_not_installed','palettePolicy':'Brightness matched to idle, then skin/blue/neutral cloth mapped along locked material ramps preserving luminance. Other materials retained; not whole-cast 24-swatch quantization.','strideDistanceCells':{'walk':.11716216216216217},'states':states}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'material-checks.json').write_text(json.dumps(material_checks,indent=2)+'\n',encoding='utf-8')
(ROOT/'brightness-checks.json').write_text(json.dumps({'targets':targets,'frames':brightness_checks},indent=2)+'\n',encoding='utf-8')
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
    old=next(s for s in json.loads((ROOT.parent/'veld-animation-pilot-v2/manifest.json').read_text())['states'] if s['id']==state['id'])
    old_frames=[Image.open(ROOT.parent/'veld-animation-pilot-v2'/p).convert('RGBA') for p in old['frameFiles']]
    old_frames[0].save(preview/f"{state['id']}-old.webp",save_all=True,append_images=old_frames[1:],duration=[round(d) for d in old['frameDurationsMs']],loop=0,lossless=True)
print(f'Extracted {sum(s["frameCount"] for s in states)} frames in {len(states)} clips; no runtime files touched.')
