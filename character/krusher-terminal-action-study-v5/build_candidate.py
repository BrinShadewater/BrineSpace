from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;V4=P.parent/'krusher-terminal-action-study-v4'
for folder in ['frames','review']:(P/folder).mkdir(parents=True,exist_ok=True)
m=json.loads((V4/'action-manifest.json').read_text());master=P.parent/'krusher-moving-equipment-test-v2/frames/bare/idle-west/000.png';canonical=Image.open(master).convert('RGBA');a=np.array(canonical)
yy,xx=np.mgrid[:184,:184];mask=(xx>=49)&(xx<115)&(yy>=62)&(yy<110);weight=np.clip((yy-62)/4,0,1)*mask
Image.fromarray(mask.astype('uint8')*255).save(P/'action-mask.png')
images={'frames/idle.png':canonical};shutil.copyfile(master,P/'frames/idle.png');records=[];hashes={}
sources={f'key-{i:03}':P.parent/f'krusher-terminal-action-study-v1/registered/{i:03}.png' for i in range(1,8)}
sources.update({f'close-{i:03}':P.parent/f'krusher-terminal-action-study-v2/registered/{i:03}.png' for i in [4,6]});sources['open']=P.parent/'krusher-terminal-action-study-v3/registered/open.png'
for name,src in sources.items():
    b=np.array(Image.open(src).convert('RGBA'));out=np.round(a*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8');im=Image.fromarray(out);path=f'frames/{name}.png';im.save(P/path);images[path]=im;hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest();records.append({'output':path,'source':str(src.relative_to(R)),'mask':'action-mask.png','outsideMaskExact':bool(np.array_equal(out[~mask],a[~mask]))})
# Existing authored release mask only; exact corrected hip device and glove
# foreground pixels outside that mask remain from the new shared idle master.
release_mask=np.array(Image.open(V4/'release-mask.png'))>0;b=np.array(Image.open(V4/'frames/release.png').convert('RGBA'));out=a.copy();out[release_mask]=b[release_mask];im=Image.fromarray(out);im.save(P/'frames/release.png');images['frames/release.png']=im;shutil.copyfile(V4/'release-mask.png',P/'release-mask.png')
src=V4/'frames/release.png';hashes[str(src.relative_to(R))]=hashlib.sha256(src.read_bytes()).hexdigest();records.append({'output':'frames/release.png','source':str(src.relative_to(R)),'mask':'release-mask.png','outsideMaskExact':bool(np.array_equal(out[~release_mask],a[~release_mask]))})
for state in m['states']:
    frames=[images[path] for path in state['frameFiles']];frames[0].save(P/f'review/{state["id"]}.png',save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=1,blend=0)
m['name']='Krusher Dom / west terminal action with glove-corrected shared master';m['canonicalIdleSource']=str(master.relative_to(R));m['canonicalIdleSha256']=hashlib.sha256(master.read_bytes()).hexdigest();m['patchBounds']=[49,62,115,110];m['status']='unselected; shared idle/held joins packaged, visual polish pending';m['limitations']=['Action arm/waist patch now extends to y110 using original registered source art; small transition band needs visual review','West bare only; no continuous-motion/native station or owner acceptance','No newly generated anatomy in this revision; lower pose remains derived reuse during raise']
(P/'action-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
report={'records':records,'sourceHashes':hashes,'master':m['canonicalIdleSource'],'masterSha256':m['canonicalIdleSha256'],'sharedIdleFileExact':hashlib.sha256((P/'frames/idle.png').read_bytes()).hexdigest()==m['canonicalIdleSha256'],'method':'Recomposite existing authored pose sources onto corrected equipment idle; four-row seam feather; unchanged fixed canvas/pivot/durations'}
(P/'provenance.json').write_text(json.dumps(report,indent=2)+'\n')
board=Image.new('RGB',(1000,400),'#272b2e');d=ImageDraw.Draw(board);d.text((14,12),'KRUSHER / SHARED IDLE - TERMINAL HOLD - RELEASE / CORRECTED GLOVE FOREGROUND',fill='white')
for i,path in enumerate(['frames/idle.png','frames/key-004.png','frames/release.png']):
    im=images[path].resize((300,300),Image.Resampling.NEAREST);board.paste(im,(i*330+15,40),im);d.text((i*330+20,350),path,fill='white')
board.save(P/'review/shared-master.png');print(json.dumps({'uniqueFrames':len(images),'sharedIdleFileExact':report['sharedIdleFileExact'],'protectedPixelsExact':all(r['outsideMaskExact'] for r in records)}))
