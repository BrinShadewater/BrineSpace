from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent
R=P.parent.parent
BASE=R/'character/krusher-bill-base-test-v2'
EQUIP=R/'character/krusher-equipment-study-v1'
for folder in ['frames','masks','review']:(P/folder).mkdir(parents=True,exist_ok=True)
attachments=json.loads((EQUIP/'manifest.json').read_text())['fit']
attachments={r['direction']:r['attachments'] for r in attachments}
parts={name:Image.open(EQUIP/f'parts/native/{name}.png').convert('RGBA') for items in attachments.values() for name,pos in items}
records=[]; hashes={}; yy,xx=np.mgrid[:184,:184]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def register(reference,frame,direction):
    # Match the central belt, excluding swinging arms and the replaced head.
    # Only integer translation is permitted; equipment has one fixed native size.
    # Profile belts are periodically hidden by the near glove. Use the rigid
    # front chest edge there, which follows the same torso translation.
    x0,y0,x1,y1={'south':(84,78,101,87),'north':(84,77,101,86),'east':(100,60,109,74),'west':(76,60,85,74)}[direction]
    ref=reference[y0:y1,x0:x1,:3].astype(float)
    target=frame[:,:,:3].astype(float)
    candidates=[]
    for dy in range(-5,6):
        for dx in range(-4,5):
            patch=target[y0+dy:y1+dy,x0+dx:x1+dx]
            score=float(np.mean(np.abs(ref-patch)))+.08*(abs(dx)+abs(dy))
            candidates.append((score,dx,dy))
    return min(candidates)

for variant in ['bare','helmet']:
    manifest=json.loads((BASE/f'{variant}-manifest.json').read_text())
    manifest['name']=f'Krusher Dom / moving equipment / {variant} trial'
    manifest['status']='unselected attachment candidate; visual occlusion review pending'
    for state in manifest['states']:
        key=state['id'];direction=key.split('-')[-1]
        reference=np.array(Image.open(BASE/f'frames/{variant}/idle-{direction}/000.png').convert('RGBA'))
        frames=[]; state_records=[]
        (P/f'frames/{variant}/{key}').mkdir(parents=True,exist_ok=True)
        for i,path in enumerate(state['frameFiles']):
            src=BASE/path;hashes[str(src.relative_to(R))]=sha(src)
            original=Image.open(src).convert('RGBA');a=np.array(original)
            score,dx,dy=register(reference,a,direction)
            layer=Image.new('RGBA',original.size)
            for name,pos in attachments[direction]:layer.alpha_composite(parts[name],(pos[0]+dx,pos[1]+dy))
            # Preserve source forearms where they pass in front of the belt.
            # Side-view glove overlap is deliberately flagged for visual review.
            foreground=(a[:,:,3]>0)&(yy>96+dy)&(yy<132+dy)&((xx<76+dx)|(xx>111+dx)) if direction in ['south','north'] else np.zeros((184,184),bool)
            la=np.array(layer);la[foreground]=0;layer=Image.fromarray(la)
            fitted=original.copy();fitted.alpha_composite(layer)
            allowed=la[:,:,3]>0;out=np.array(fitted)
            assert np.array_equal(a[~allowed],out[~allowed])
            assert np.array_equal(a[125:],out[125:])
            output=f'frames/{variant}/{key}/{i:03}.png';mask=f'masks/{variant}-{key}-{i:03}.png'
            fitted.save(P/output);Image.fromarray(allowed.astype('uint8')*255).save(P/mask)
            record={'variant':variant,'state':key,'frame':i,'source':str(src.relative_to(R)),'output':output,'mask':mask,'translation':[dx,dy],'registrationError':round(score,3)}
            records.append(record);state_records.append(record);frames.append(fitted)
        state['frameFiles']=[r['output'] for r in state_records]
        state['provenance']='Existing Krusher Bill-base trial; generated accessory parts at fixed density; integer belt registration'
        frames[0].save(P/f'review/{variant}-{key}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
        if key.startswith('walk'):
            board=Image.new('RGB',(1200,530),'#272b2e');draw=ImageDraw.Draw(board)
            draw.text((16,12),f'KRUSHER DOM / {variant} / {key} / belt attachment sampling',fill='white')
            for k,index in enumerate(np.linspace(0,len(frames)-1,10,dtype=int)):
                x=(k%5)*240;y=(k//5)*245+35
                im=frames[index].resize((220,220),Image.Resampling.NEAREST);board.paste(im,(x,y),im)
                draw.text((x+8,y+221),f'{index:03} offset {state_records[index]["translation"]}',fill='white')
            board.save(P/f'review/{variant}-{key}-samples.png')
    (P/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report={'records':records,'sourceHashes':hashes,'partHashes':{name:sha(EQUIP/f'parts/native/{name}.png') for name in parts},'limitations':['Integer belt registration requires visual review through complete cycles','Foreground arm mask is conservative; profile glove occlusion remains unaccepted','No typing or equipment deployment action','No gameplay selection or native station acceptance']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'frames':len(records),'translationRange':{axis:[min(r['translation'][i] for r in records),max(r['translation'][i] for r in records)] for i,axis in enumerate(['x','y'])},'maxRegistrationError':max(r['registrationError'] for r in records)}))
