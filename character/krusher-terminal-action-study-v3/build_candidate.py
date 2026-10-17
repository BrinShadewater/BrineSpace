from pathlib import Path
import hashlib,json,copy
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'krusher-terminal-action-study-v2'
for folder in ['registered','frames','review']:(P/folder).mkdir(parents=True,exist_ok=True)
m=json.loads((OLD/'action-manifest.json').read_text());canonical=Image.open(R/m['canonicalIdleSource']).convert('RGBA');a=np.array(canonical)
yy,xx=np.mgrid[:184,:184];mask=(xx>=49)&(xx<115)&(yy>=62)&(yy<106);weight=np.clip((yy-62)/4,0,1)*mask
Image.fromarray(mask.astype('uint8')*255).save(P/'patch-mask.png')
paths=set(path for s in m['states'] for path in s['frameFiles']);hashes={};images={}
for path in paths:
    src=OLD/path;images[path]=Image.open(src).convert('RGBA');images[path].save(P/path);hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest()
records=[]
for kind in ['lift','open','release']:
    file=P/f'source-{kind}.png';source=Image.open(file).convert('RGBA');raw=np.array(source);sy,sx=np.where(raw[:,:,3]>100)
    bounds=[int(sx.min()),int(sy.min()),int(sx.max())+1,int(sy.max())+1];height=bounds[3]-bounds[1];scale=148/height
    by,bx=np.where((raw[:,:,3]>100)&(np.indices(raw.shape[:2])[0]>bounds[3]-height*.15));boot_axis=(bx.min()+bx.max())/2
    dest=(round(90-boot_axis*scale),round(172-bounds[3]*scale))
    reg=Image.new('RGBA',(184,184));reg.alpha_composite(source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS),dest);reg.save(P/f'registered/{kind}.png')
    b=np.array(reg);out=np.round(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8')
    if kind=='release':
        # The hardware is already stowed; reuse the exact canonical hip device.
        # This is deterministic attachment reuse, not a new generated device.
        out[90:106,88:96]=a[90:106,88:96]
    im=Image.fromarray(out);path=f'frames/{kind}.png'
    if kind=='open':im.save(P/path);images[path]=im
    else:im.save(P/f'review/rejected-{kind}.png')
    records.append({'kind':kind,'source':f'source-{kind}.png','sourceSha256':hashlib.sha256(file.read_bytes()).hexdigest(),'alphaRange':list(source.getchannel('A').getextrema()),'standingScale':scale,'registration':list(dest),'sourceBounds':bounds,'outsidePatchExact':bool(np.array_equal(out[~mask],a[~mask])),'admitted':kind=='open','rejection':{'lift':'Device too high instead of between hip and waist','release':'Clipped device silhouette drift and hand boundary discontinuity'}.get(kind)})
states=[('terminal-raise-west',['idle','key-001','key-007','key-002','open','key-003'],[100,100,100,100,120,180],False),('terminal-type-west',['key-003','key-004','key-005','key-004','key-005','key-003'],[180,160,160,160,160,180],True),('terminal-lower-west',['key-003','close-004','key-006','key-007','close-006','idle'],[100,120,120,140,140,120],False)]
m['name']='Krusher Dom / west terminal action isolated intermediate revision';m['states']=[];m['status']='unselected candidate; equipment and full motion review pending'
for key,names,times,loop in states:
    framefiles=[f'frames/{name}.png' for name in names];frames=[images[p] for p in framefiles]
    m['states'].append({'id':key,'frameCount':len(names),'frameFiles':framefiles,'frameDurationsMs':times,'loop':loop})
    frames[0].save(P/f'review/{key}.png',save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=1,blend=0)
m['limitations']=['One isolated partial-opening source admitted provisionally; generated lift/release rejected after native review','Raise reuses existing lowered-terminal key-007 pose; no new lift artwork claimed','West bare only; no full-motion/native station acceptance, other directions or helmet']
(P/'action-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
provenance={'records':records,'sourceHashes':hashes,'generationExecutionIds':{'lift':'0596a086-701f-4fa3-9a25-df82189ab170','open':'a662834d-7ddf-40f3-a654-bd4f1787a5dd','release':'8eb6a970-af5b-4377-8c93-ca82069a70ec'},'generationMethod':'builtin imagegen isolated adjacent-pose references','rawSourceAdmission':'Only open admitted provisionally; lift/release rejected after native review','derivedPoseReuse':'Existing key-007 lowering pose reused during raise; no mirror or invented interpolation','patchBounds':m['patchBounds']}
(P/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
board=Image.new('RGB',(1400,540),'#272b2e');d=ImageDraw.Draw(board);d.text((12,10),'KRUSHER / PARTIAL OPENING AND REUSED LIFT TRANSITION CANDIDATE',fill='white')
for j,sequence in enumerate([states[0][1],states[2][1]]):
    for i,name in enumerate(sequence):
        im=images[f'frames/{name}.png'];board.paste(im,(i*200+8,j*250+30),im);d.text((i*200+12,j*250+220),name,fill='white')
board.save(P/'review/transition-sequences.png');print(json.dumps({'uniqueFrames':len(images),'newAdmittedIntermediateSources':sum(r['admitted'] for r in records),'protectedPixelsExact':all(r['outsidePatchExact'] for r in records)}))
