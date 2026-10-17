"""Selected native north helmet, source neck registration and bounded eyelid."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
HELM=R/'character/veld-shared-helmet-v1/frames/idle-north/000.png'
COMP=R/'character/veld-shared-helmet-v1/fitted-north.png'
NECKS=[[254,166],[782,225],[1303,350],[168,766],[609,858],[1142,858]]
ANGLES=[0,0,0,40,88,88]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reg=json.loads((P/'bare-registration.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());scale=reg['fixedRuler']
    native=Image.open(COMP).convert('RGBA');native.save(P/'sources/canonical-head.png')
    pitch=json.loads((P/'pitch-registration.json').read_text())
    first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(HELM).convert('RGBA'),(36,52));frames=[first];records=[]
    for i,r in enumerate(reg['frames'],1):
        bare=Image.open(P/m['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare)
        neck=[r['position'][j]+(NECKS[i][j]-r['box'][j])*scale for j in range(2)]
        center=[r['position'][j]+(reg['heads'][i][j]-r['box'][j])*scale for j in range(2)]
        cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<18**2
        v=b[:,:,:3].astype(float);warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.14*v[:,:,2]);b[local&warm]=0
        angle=ANGLES[i];rad=math.radians(angle);component=native;anchor=[16,32];component_source='selected rear master'
        if i in [1,2]:
            authored=pitch['heads'][i];component=Image.open(P/authored['file']).convert('RGBA');anchor=authored['anchor'];component_source=authored['file']
        rot=component.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        dx,dy=anchor[0]-component.width/2,anchor[1]-component.height/2
        ra=[rot.width/2+math.cos(rad)*dx+math.sin(rad)*dy,rot.height/2-math.sin(rad)*dx+math.cos(rad)*dy]
        pos=[round(neck[j]-ra[j]) for j in range(2)];out=Image.fromarray(b);out.alpha_composite(rot,pos);frames.append(out)
        records.append({'pose':i,'neck':neck,'headCenter':center,'sourceNeck':NECKS[i],'tiltCounterclockwise':angle,'forwardPitchDegrees':pitch['heads'][i]['pitchDegrees'] if i in [1,2] else 0,'nativeScale':1,'componentSource':component_source,'componentPosition':pos,'componentSize':list(rot.size),'eraseRadius':18,'expression':'rear hardware'})
    files=[];hashes={}
    for i,frame in enumerate(frames):
        f=P/f'frames/helmet/death-ground-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    m['name']='Veld north dry collapse canonical helmet candidate';m['equipment']='diving-helmet';m['states'][0]['frameFiles']=files
    data={'helmetIdle':HELM.relative_to(R).as_posix(),'helmetIdleSha256':sha(HELM),'nativeComponent':COMP.relative_to(R).as_posix(),'nativeComponentSha256':sha(COMP),'nativeAnchor':[16,32],'sourceNecks':NECKS,'frames':records,'pitchRegistrationSha256':sha(P/'pitch-registration.json'),'scope':'paired rear candidate with authored15/40degree depth-pitch heads; no normal selection or full-family motion acceptance'}
    for name,datum in [('helmet-manifest.json',m),('helmet-registration.json',data),('helmet-frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(datum,indent=2)+'\n')
    board=Image.new('RGB',(1536,810),'#202a30');d=ImageDraw.Draw(board)
    bare=[Image.open(P/p).convert('RGBA') for p in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
    for row,seq in enumerate([bare,frames,[first]*6]):
        for i,frame in enumerate(seq):board.paste(frame,(i*256,row*270+16),frame);d.text((i*256+8,row*270),['Bare','Helmet','Selected helmet idle'][row]+f' {i}',fill='white')
    board.save(P/'paired-contact-sheet.png')
    print(json.dumps({'helmetFrames':6,'nativeSize':list(native.size),'rearFaceVisible':False,'normalSelection':False}))
if __name__=='__main__':main()

