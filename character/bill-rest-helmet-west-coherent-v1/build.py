from pathlib import Path
import json,hashlib,math,copy
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];B=P.parent/'bill-rest-west-coherent-v1';D=P.parent/'bill-seated-helmet-west-coherent-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((B/'manifest.json').read_text());reg=json.loads((B/'registration.json').read_text())
    source=D/'sources/canonical-head.png';canonical=P/'sources/canonical-head.png';canonical.parent.mkdir(parents=True,exist_ok=True);canonical.write_bytes(source.read_bytes())
    head=Image.open(canonical).convert('RGBA');closed=Image.open(P/'sources/canonical-closed-eye.png').convert('RGBA')
    idle=D/'frames/sit-down-west/000.png';frames=[Image.open(idle).convert('RGBA')];yy,xx=np.indices((256,256));records=[]
    rows=reg['loweringFrames']+reg['frames']
    necks=[(526,278),(1355,459),(881,321),(1422,357),(432,818),(922,860),(1432,860)]
    centers=[(499,188),(1327,375),(866,278),(1414,311),(421,768),(958,857),(1466,857)]
    angles=[5,5,5,15,40,90,90]
    for i,row in enumerate(rows,1):
        path=R/m['states'][0]['frameFiles'][i][6:];bare=np.array(Image.open(path).convert('RGBA'));rgb=bare[:,:,:3].astype(float)
        sx,sy=row['scale'];bx,by=row['box'][:2];px,py=row['position'];nx,ny=necks[i-1]
        neck=[px+(nx-bx)*sx,py+(ny-by)*sy];angle=angles[i-1];component=closed if i>=6 else head
        rotated=component.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True);rad=math.radians(angle)
        dx=16-head.width/2;dy=29-head.height/2
        anchor=[rotated.width/2+math.cos(rad)*dx-math.sin(rad)*dy,rotated.height/2+math.sin(rad)*dx+math.cos(rad)*dy]
        pos=[round(neck[0]-anchor[0]),round(neck[1]-anchor[1])]
        if i==7:pos=records[-1]["position"].copy()
        hx,hy=centers[i-1];center=[px+(hx-bx)*sx,py+(hy-by)*sy]
        local=((xx-center[0])/17)**2+((yy-center[1])/19)**2<1
        warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);erase=local&(bare[:,:,3]>0)
        out=bare.copy();out[erase]=0;im=Image.fromarray(out);im.alpha_composite(rotated,pos);frames.append(im)
        records.append({'frame':i,'sourceNeck':list(necks[i-1]),'neck':neck,'tilt':angle,'position':pos,'nativeScale':1,'closedEye':i>=6,'componentSize':list(rotated.size),'bareSha256':sha(path),'eraseEllipse':{'center':center,'radii':[17,19]}})
    mapping={};hashes={}
    for i,im in enumerate(frames):
        path=P/f'frames/lie-down-west/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
        original=m['states'][0]['frameFiles'][i];mapping[original]='res://'+path.relative_to(R).as_posix();hashes[mapping[original]]=sha(path)
    for state in m['states']:state['frameFiles']=[mapping[f] for f in state['frameFiles']]
    m.update(name='Bill west generic rest with shared helmet candidate',equipment='diving-helmet')
    for name,data in [('manifest.json',m),('helmet-registration.json',{'canonicalSha256':sha(canonical),'closedSha256':sha(P/'sources/canonical-closed-eye.png'),'endpoint':idle.relative_to(R).as_posix(),'endpointSha256':sha(idle),'bareRegistrationSha256':sha(B/'registration.json'),'frames':records,'scope':'native component rotation/neck registration; body remains paired; furniture/motion/normal selection unproven'}),('frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(2048,768),(34,52,62))
    for i,im in enumerate(frames):
        board.paste(im,(i*256,0),im);bare=Image.open(R/json.loads((B/'manifest.json').read_text())['states'][0]['frameFiles'][i][6:]);board.paste(bare,(i*256,256),bare);board.paste(frames[0],(i*256,512),frames[0])
    board.save(P/'contact-sheet.png');print('Built paired west helmet rest3 states/8 slots, native hardware and exact equipped idle')
if __name__=='__main__':main()
