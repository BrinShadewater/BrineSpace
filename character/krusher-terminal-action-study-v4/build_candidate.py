from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'krusher-terminal-action-study-v3'
for folder in ['frames','review']:(P/folder).mkdir(parents=True,exist_ok=True)
m=json.loads((OLD/'action-manifest.json').read_text());canonical=Image.open(R/m['canonicalIdleSource']).convert('RGBA');a=np.array(canonical)
source=Image.open(P/'source-release.png').convert('RGBA');raw=np.array(source);sy,sx=np.where(raw[:,:,3]>100);bounds=[int(sx.min()),int(sy.min()),int(sx.max())+1,int(sy.max())+1];height=bounds[3]-bounds[1];scale=148/height
gy,gx=np.where((raw[:,:,3]>100)&(np.indices(raw.shape[:2])[0]>bounds[3]-height*.15));axis=(gx.min()+gx.max())/2
dest=(round(90-axis*scale),round(172-bounds[3]*scale));registered=Image.new('RGBA',(184,184));registered.alpha_composite(source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS),dest);registered.save(P/'registered-release.png')
yy,xx=np.mgrid[:184,:184]
arm=(xx>=91)&(xx<106)&(yy>=84)&(yy<110)
hardware=(xx>=88)&(xx<96)&(yy>=92)&(yy<108)
mask=arm&~hardware;weight=np.clip((yy-84)/3,0,1)*mask
b=np.array(registered);out=np.round(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8');release=Image.fromarray(out);release.save(P/'frames/release.png');Image.fromarray(mask.astype('uint8')*255).save(P/'release-mask.png')
hashes={};images={'frames/release.png':release}
for path in set(path for state in m['states'] for path in state['frameFiles']):
    src=OLD/path;images[path]=Image.open(src).convert('RGBA');images[path].save(P/path);hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest()
lower=m['states'][2];lower['frameFiles'].insert(-1,'frames/release.png');lower['frameDurationsMs']=[100,120,120,120,100,100,120];lower['frameCount']=len(lower['frameFiles'])
for state in m['states']:
    frames=[images[path] for path in state['frameFiles']];frames[0].save(P/f'review/{state["id"]}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
m['name']='Krusher Dom / west terminal tight release revision';m['status']='unselected representative action; full motion and equipment polish pending';m['releasePatch']='Only near forearm/glove (91,84)-(106,110), excluding exact hip hardware (88,92)-(96,108); three-row upper seam feather'
m['limitations']=['Release near-forearm/glove patch requires visual acceptance; source-wide changes discarded','West bare only; shared equipment continuity, full motion and native station review remain','Existing lowered-terminal pose reused during raise; no new lift art claimed']
(P/'action-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
provenance={'source':'source-release.png','sourceSha256':hashlib.sha256((P/'source-release.png').read_bytes()).hexdigest(),'sourceHashes':hashes,'executionId':'e6d8fd2c-5193-437b-8536-113aecc4f23c','method':'builtin imagegen tight edit, deterministic masked compositing','sourceAlphaRange':list(source.getchannel('A').getextrema()),'sourceBounds':bounds,'scale':scale,'destination':list(dest),'reference':'reference-idle-4x.png','referenceMethod':'canonical idle enlarged 4x nearest neighbour for generation input only','outsideReleaseMaskExact':bool(np.array_equal(out[~mask],a[~mask])),'hipHardwareExact':bool(np.array_equal(out[hardware],a[hardware])),'headAndBootsExact':bool(np.array_equal(out[:84],a[:84]) and np.array_equal(out[110:],a[110:]))}
(P/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
board=Image.new('RGB',(1000,400),'#272b2e');d=ImageDraw.Draw(board);d.text((16,12),'KRUSHER / RECLIP - EMPTY HAND RELEASE - ORIGINAL IDLE',fill='white')
for i,path in enumerate(['frames/close-006.png','frames/release.png','frames/idle.png']):
    im=images[path].resize((300,300),Image.Resampling.NEAREST);board.paste(im,(i*330+15,40),im);d.text((i*330+20,350),path,fill='white')
board.save(P/'review/release-join.png');print(json.dumps({k:provenance[k] for k in ['outsideReleaseMaskExact','hipHardwareExact','headAndBootsExact','scale','destination']}))
