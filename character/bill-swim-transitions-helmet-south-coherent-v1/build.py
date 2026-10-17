"""Paired south helmet pitch interiors with exact matching equipment endpoints."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-transitions-south-coherent-v1'
DONOR=HERE.parent/'bill-swim-helmet-south-coherent-v1/components'
TARGET=[(128,92),(128,96),(128,100),(128,104),(128,107),(128,110)]
ENDPOINTS=['bill-tread-helmet-south-coherent-v1/frames/tread-south/000.png','bill-swim-helmet-south-coherent-v1/frames/swim-south/000.png']
def main():
    frames=[];records=[]
    for i,(hx,hy) in enumerate(TARGET):
        if i in [0,5]:
            frame=Image.new('RGBA',(256,256));frame.alpha_composite(Image.open(HERE.parent/ENDPOINTS[0 if i==0 else 1]).convert('RGBA'),(36,58) if i==0 else (24,-24));frames.append(frame);continue
        component=DONOR/f'{[0,1,2,3,3,3][i]:03}.png';head=Image.open(component).convert('RGBA')
        file=f'frames/swim-start-south/{i:03}.png';b=np.array(Image.open(BARE/file).convert('RGBA'));y,x=np.indices(b.shape[:2])
        erase=(x>=hx-12)&(x<=hx+12)&(y>=hy-2)&(y<hy+32)
        out=b.copy();out[erase]=0;position=(hx-head.width//2,hy-4);result=Image.fromarray(out);result.alpha_composite(head,position);out=np.array(result)
        foreground=(b[:,:,3]>0)&((x<hx-12)|(x>hx+12))&(y<hy+32);out[foreground]=b[foreground]
        frames.append(Image.fromarray(out));records.append({'file':file,'position':position,'head':[hx,hy],'scale':1,'rotationDegrees':0,'protectedBodyFromY':hy+32,'component':component.relative_to(HERE.parent).as_posix(),'componentSha256':hashlib.sha256(component.read_bytes()).hexdigest(),'bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
    pack=copy.deepcopy(json.loads((BARE/'manifest.json').read_text(encoding='utf-8')));pack.update(name='Bill exact south helmet south pitch candidate',equipment='diving-helmet');hashes={}
    for state in pack['states']:
        ims=frames if state['id']=='swim-start-south' else list(reversed(frames))
        for file,im in zip(state['frameFiles'],ims):
            path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
        state['provenance']='four independently authored south pitch bodies;authored pitched south shell;exact equipped loop endpoints;stop derived in reverse'
    for name,data in [('manifest.json',pack),('frame-hashes.json',hashes),('helmet-registration.json',{'method':'independently authored35/65/85degree shells with one frozen physical scale and neutral grade','endpointAuthorities':ENDPOINTS,'endpointOffsets':[[36,58],[24,-24]],'frames':records})]:
        (HERE/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    contact=Image.new('RGB',(1536,256),(29,43,51))
    for i,im in enumerate(frames):contact.paste(im,(256*i,0),im)
    contact.save(HERE/'contact-sheet.png');print('Built four south helmet pitch interiors and exact endpoints')
if __name__=='__main__':main()
