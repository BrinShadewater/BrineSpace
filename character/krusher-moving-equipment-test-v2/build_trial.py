from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'krusher-moving-equipment-test-v1';BASE=P.parent/'krusher-bill-base-test-v2';EQUIP=P.parent/'krusher-equipment-study-v1'
from glove_foreground import glove_foreground
for folder in ['frames','masks','review']:(P/folder).mkdir(parents=True,exist_ok=True)
old=json.loads((OLD/'verification.json').read_text());parts={};attachments={r['direction']:r['attachments'] for r in json.loads((EQUIP/'manifest.json').read_text())['fit']}
for group in attachments.values():
    for name,pos in group:parts[name]=Image.open(EQUIP/f'parts/native/{name}.png').convert('RGBA')
records=[];hashes={};affected=0;restored=0
for variant in ['bare','helmet']:
    manifest=json.loads((OLD/f'{variant}-manifest.json').read_text());manifest['name']=f'Krusher Dom / glove foreground equipment trial / {variant}';manifest['status']='unselected; glove masks require visual acceptance'
    for state in manifest['states']:
        key=state['id'];direction=key.split('-')[-1];frames=[];(P/f'frames/{variant}/{key}').mkdir(parents=True,exist_ok=True)
        for i,path in enumerate(state['frameFiles']):
            record=next(r for r in old['records'] if r['variant']==variant and r['state']==key and r['frame']==i)
            src=R/record['source'];hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest();original=Image.open(src).convert('RGBA');a=np.array(original);dx,dy=record['translation']
            layer=Image.new('RGBA',(184,184))
            for name,pos in attachments[direction]:layer.alpha_composite(parts[name],(pos[0]+dx,pos[1]+dy))
            foreground,cuffs=glove_foreground(a,direction);la=np.array(layer);overlap=foreground&(la[:,:,3]>0);la[foreground]=0;fitted=original.copy();fitted.alpha_composite(Image.fromarray(la));out=np.array(fitted);mask=la[:,:,3]>0
            output=f'frames/{variant}/{key}/{i:03}.png';editmask=f'masks/{variant}-{key}-{i:03}.png';handmask=f'masks/{variant}-{key}-{i:03}-foreground.png'
            fitted.save(P/output);Image.fromarray(mask.astype('uint8')*255).save(P/editmask);Image.fromarray(foreground.astype('uint8')*255).save(P/handmask);frames.append(fitted)
            restored+=int(overlap.sum());affected+=int(overlap.any())
            records.append({'variant':variant,'state':key,'frame':i,'source':str(src.relative_to(R)),'output':output,'mask':editmask,'foregroundMask':handmask,'translation':[dx,dy],'cuffs':cuffs,'restoredOverlapPixels':int(overlap.sum()),'outsideEditExact':bool(np.array_equal(a[~mask],out[~mask])),'foregroundExact':bool(np.array_equal(a[foreground],out[foreground]))})
        frames[0].save(P/f'review/{variant}-{key}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
        if key.startswith('walk'):
            board=Image.new('RGB',(1200,530),'#272b2e');d=ImageDraw.Draw(board);d.text((12,12),f'KRUSHER / {variant} / {key} / cuff-tracked glove foreground candidate',fill='white')
            for n,index in enumerate(np.linspace(0,len(frames)-1,10,dtype=int)):
                x=n%5*240;y=n//5*245+35;im=frames[index].resize((220,220),Image.Resampling.NEAREST);board.paste(im,(x,y),im);d.text((x+8,y+221),f'pose {index:03}',fill='white')
            board.save(P/f'review/{variant}-{key}-samples.png')
    (P/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'records':records,'sourceHashes':hashes,'framesWithAccessoryGloveOverlap':affected,'restoredGloveOverlapPixels':restored,'maskMethod':'Connected bright cuffs, orientation-derived bounded glove region, neutral/green dark glove material; masks require visual acceptance','limitations':['Cuff/material segmentation may be conservative; complete-cycle visual review remains','Original equipment registration retained','No normal art selection or actor integration']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['framesWithAccessoryGloveOverlap','restoredGloveOverlapPixels']}));assert all(r['outsideEditExact'] and r['foregroundExact'] for r in records)
