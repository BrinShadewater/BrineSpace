"""Paired rear helmet pitch interiors with exact matching equipment endpoints."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-transitions-north-coherent-v1'
DONOR=HERE.parent/'bill-swim-helmet-north-coherent-v1/sources/canonical-head.png'
TARGET=[(128,92),(128,95),(128,98),(128,100),(128,102),(128,104)]
ENDPOINTS=['bill-tread-helmet-north-coherent-v1/frames/tread-north/000.png','bill-swim-helmet-north-coherent-v1/frames/swim-north/000.png']
def main():
    head=Image.open(DONOR).convert('RGBA');frames=[];records=[]
    for i,(hx,hy) in enumerate(TARGET):
        if i in [0,5]:
            frame=Image.new('RGBA',(256,256));frame.alpha_composite(Image.open(HERE.parent/ENDPOINTS[0 if i==0 else 1]).convert('RGBA'),(36,58) if i==0 else (24,56));frames.append(frame);continue
        file=f'frames/swim-start-north/{i:03}.png';b=np.array(Image.open(BARE/file).convert('RGBA'));y,x=np.indices(b.shape[:2])
        erase=(x>=hx-12)&(x<=hx+12)&(y>=hy-2)&(y<hy+19)
        out=b.copy();out[erase]=0;position=(hx-20,hy-9);result=Image.fromarray(out);result.alpha_composite(head,position);out=np.array(result)
        foreground=(b[:,:,3]>0)&((x<hx-12)|(x>hx+12))&(y<hy+21);out[foreground]=b[foreground]
        frames.append(Image.fromarray(out));records.append({'file':file,'position':position,'head':[hx,hy],'scale':1,'rotationDegrees':0,'protectedBodyFromY':hy+25,'bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
    pack=copy.deepcopy(json.loads((BARE/'manifest.json').read_text(encoding='utf-8')));pack.update(name='Bill exact rear helmet north pitch candidate',equipment='diving-helmet');hashes={}
    for state in pack['states']:
        ims=frames if state['id']=='swim-start-north' else list(reversed(frames))
        for file,im in zip(state['frameFiles'],ims):
            path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
        state['provenance']='four independently authored north pitch bodies;selected native rear shell;exact equipped loop endpoints;stop derived in reverse'
    for name,data in [('manifest.json',pack),('frame-hashes.json',hashes),('helmet-registration.json',{'donor':DONOR.relative_to(HERE.parent).as_posix(),'donorSha256':hashlib.sha256(DONOR.read_bytes()).hexdigest(),'endpointAuthorities':ENDPOINTS,'endpointOffsets':[[36,58],[24,56]],'frames':records})]:
        (HERE/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    contact=Image.new('RGB',(1536,256),(29,43,51))
    for i,im in enumerate(frames):contact.paste(im,(256*i,0),im)
    contact.save(HERE/'contact-sheet.png');print('Built four rear helmet pitch interiors and exact endpoints')
if __name__=='__main__':main()
