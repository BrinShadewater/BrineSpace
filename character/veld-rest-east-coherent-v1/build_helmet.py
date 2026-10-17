"""Selected native east helmet, source neck registration and bounded eyelid."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
HELM=R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'
COMP=R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png'
NECKS=[[215,180],[746,381],[1110,413],[117,844],[635,881],[1143,881]]
ANGLES=[0,0,0,12,70,70]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reg=json.loads((P/'bare-registration.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());scale=reg['fixedRuler']
    native=Image.open(COMP).convert('RGBA');native.save(P/'sources/canonical-head.png');closed_native=Image.open(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png').convert('RGBA');closed_native.save(P/'sources/canonical-head-closed.png')
    first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(HELM).convert('RGBA'),(36,52));frames=[first];records=[]
    for i,r in enumerate(reg['frames'],1):
        bare=Image.open(P/m['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare)
        neck=[r['position'][j]+(NECKS[i][j]-r['box'][j])*scale for j in range(2)]
        center=[r['position'][j]+(reg['heads'][i][j]-r['box'][j])*scale for j in range(2)]
        cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<18**2
        # The gray hairband is head material too; warm-only masks leave its arc.
        b[local]=0
        angle=ANGLES[i];rad=math.radians(angle);component=closed_native if i>=4 else native;anchor=[19,36];component_source='canonical closed' if i>=4 else 'canonical open'
        rot=component.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        dx,dy=anchor[0]-component.width/2,anchor[1]-component.height/2
        ra=[rot.width/2+math.cos(rad)*dx+math.sin(rad)*dy,rot.height/2-math.sin(rad)*dx+math.cos(rad)*dy]
        pos=[round(neck[j]-ra[j]) for j in range(2)];out=Image.fromarray(b);out.alpha_composite(rot,pos);frames.append(out)
        records.append({'pose':i,'neck':neck,'headCenter':center,'sourceNeck':NECKS[i],'tiltCounterclockwise':angle,'forwardPitchDegrees':0,'nativeScale':1,'componentSource':component_source,'componentPosition':pos,'componentSize':list(rot.size),'eraseRadius':18,'expression':'closed' if i>=4 else 'open'})
    files=[];hashes={}
    for i,frame in enumerate(frames):
        f=P/f'frames/helmet/lie-down-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    m['name']='Veld east generic rest canonical helmet candidate';m['equipment']='diving-helmet';m['states'][0]['frameFiles']=files;m['states'][1]['frameFiles']=list(reversed(files));m['states'][2]['frameFiles']=[files[-1]]
    data={'helmetIdle':HELM.relative_to(R).as_posix(),'helmetIdleSha256':sha(HELM),'nativeComponent':COMP.relative_to(R).as_posix(),'nativeComponentSha256':sha(COMP),'nativeAnchor':[19,36],'sourceNecks':NECKS,'frames':records,'closedComponent': 'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png','closedComponentSha256':sha(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png'),'scope':'paired generic floor rest candidate; canonical native component and closed expression; no normal selection or furniture/life/death proof'}
    for name,datum in [('helmet-manifest.json',m),('helmet-registration.json',data),('helmet-frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(datum,indent=2)+'\n')
    board=Image.new('RGB',(1536,810),'#202a30');d=ImageDraw.Draw(board)
    bare=[Image.open(P/p).convert('RGBA') for p in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
    for row,seq in enumerate([bare,frames,[first]*6]):
        for i,frame in enumerate(seq):board.paste(frame,(i*256,row*270+16),frame);d.text((i*256+8,row*270),['Bare','Helmet','Selected helmet idle'][row]+f' {i}',fill='white')
    board.save(P/'paired-contact-sheet.png')
    print(json.dumps({'helmetFrames':6,'nativeSize':list(native.size),'visibleFace':True,'normalSelection':False}))
if __name__=='__main__':main()



