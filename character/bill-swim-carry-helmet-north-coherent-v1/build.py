"""Fit the selected rear shell at native scale; preserve all water body artwork."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-carry-north-coherent-v1'
DONOR=HERE.parent/'bill-cargo-helmet-north-v1/sources/canonical-head.png'
HEAD=(104,48)
def main():
    head=Image.open(DONOR).convert('RGBA').crop((0,0,40,34))
    contour=Image.new('L',head.size);ImageDraw.Draw(contour).polygon([(0,0),(40,0),(40,22),(33,30),(29,34),(11,34),(7,30),(0,22)],fill=255)
    a=np.array(head);a[:,:,3]=np.minimum(a[:,:,3],np.array(contour));head=Image.fromarray(a)
    (HERE/'sources').mkdir(parents=True,exist_ok=True);head.save(HERE/'sources/canonical-head.png')
    manifest=copy.deepcopy(json.loads((BARE/'manifest.json').read_text(encoding='utf-8')))
    manifest.update(name='Bill native rear helmet north swimming cargo candidate',equipment='diving-helmet')
    hashes={};records=[];images=[];hx,hy=HEAD;position=(hx-20,hy-9)
    for state in manifest['states']:
        for file in state['frameFiles']:
            original=Image.open(BARE/file).convert('RGBA');b=np.array(original);y,x=np.indices(b.shape[:2])
            erase=(x>=hx-12)&(x<=hx+12)&(y>=hy-2)&(y<hy+19)
            out=b.copy();out[erase]=0;result=Image.fromarray(out);result.alpha_composite(head,position);out=np.array(result)
            foreground=(b[:,:,3]>0)&(((x<hx-12)|(x>hx+12))&(y<hy+21)|(y<hy))
            out[foreground]=b[foreground]
            result=Image.fromarray(out);path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);result.save(path);images.append(result)
            hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
            records.append({'file':file,'position':position,'scale':1,'rotationDegrees':0,'eraseBox':[hx-12,hy-2,hx+13,hy+19],'foregroundOutsideHeadFromX':[hx-12,hx+12],'foregroundBelowY':hy+21,'protectedCaseAboveY':hy,'protectedBodyFromY':hy+25,'bareSha256':hashlib.sha256((BARE/file).read_bytes()).hexdigest()})
        state['provenance']='independently authored rear water body;exact selected rear shell crop at native scale; original collar/backpack/arms retained'
    for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('helmet-registration.json',{'donor':DONOR.relative_to(HERE.parent).as_posix(),'donorSha256':hashlib.sha256(DONOR.read_bytes()).hexdigest(),'crop':[0,0,40,34],'contour':[(0,0),(40,0),(40,22),(33,30),(29,34),(11,34),(7,30),(0,22)],'frames':records})]:
        (HERE/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    w,h=manifest['frameWidth'],manifest['frameHeight'];contact=Image.new('RGB',(w*6,h*2),(29,43,51))
    for i,im in enumerate(images):contact.paste(im,(i*w,0),im);bare=Image.open(BARE/manifest['states'][0]['frameFiles'][i]);contact.paste(bare,(i*w,h),bare)
    contact.save(HERE/'contact-sheet.png');print('Built six north canonical rear shell poses')
if __name__=='__main__':main()
