"""Selected native west helmet, source neck registration and bounded eyelid."""
from pathlib import Path
import math,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
HELM=R/'character/veld-shared-helmet-v1/frames/idle-west/000.png'
COMP=R/'character/veld-shared-helmet-v1/fitted-west.png'
NECKS=[[254,160],[689,225],[1191,356],[161,800],[606,845],[1116,854]]
ANGLES=[0,20,38,50,85,88]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reg=json.loads((P/'bare-registration.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());scale=reg['fixedRuler']
    native=Image.open(COMP).convert('RGBA');a=np.array(native);closed=a.copy()
    source=P/'sources/expression/closed-v1.png';expression=Image.open(source).convert('RGBA');patch=np.array(expression.crop((204,612,308,670)).resize((4,2),Image.Resampling.LANCZOS))
    skin=a[20:23,5:10,:3].reshape(-1,3).astype(float);ps=np.array(expression.crop((310,710,400,820)))[:,:,:3].reshape(-1,3).astype(float)
    gain=np.median(skin,axis=0)/np.median(ps,axis=0);closed[17:19,5:9,:3]=np.clip(patch[:,:,:3]*gain,0,255).astype('uint8')
    closed_native=Image.fromarray(closed);native.save(P/'sources/canonical-head.png');closed_native.save(P/'sources/canonical-head-closed.png')
    compboard=Image.new('RGB',(816,456),'#202a30')
    for i,head in enumerate([native,closed_native]):
        large=head.resize((408,456),Image.Resampling.NEAREST);compboard.paste(large,(i*408,0),large)
    compboard.save(P/'sources/expression/closed-eye-native-comparison.png')
    first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(HELM).convert('RGBA'),(36,52));frames=[first];records=[]
    for i,r in enumerate(reg['frames'],1):
        bare=Image.open(P/m['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare)
        neck=[r['position'][j]+(NECKS[i][j]-r['box'][j])*scale for j in range(2)]
        center=[r['position'][j]+(reg['heads'][i][j]-r['box'][j])*scale for j in range(2)]
        cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<18**2
        v=b[:,:,:3].astype(float);warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.14*v[:,:,2]);b[local&warm]=0
        angle=ANGLES[i];rad=math.radians(angle);component=closed_native if i>=4 else native;rot=component.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
        anchor=[17,35];dx,dy=anchor[0]-native.width/2,anchor[1]-native.height/2
        ra=[rot.width/2+math.cos(rad)*dx+math.sin(rad)*dy,rot.height/2-math.sin(rad)*dx+math.cos(rad)*dy]
        pos=[round(neck[j]-ra[j]) for j in range(2)];out=Image.fromarray(b);out.alpha_composite(rot,pos);frames.append(out)
        records.append({'pose':i,'neck':neck,'headCenter':center,'sourceNeck':NECKS[i],'tiltCounterclockwise':angle,'nativeScale':1,'componentPosition':pos,'componentSize':list(rot.size),'eraseRadius':18,'expression':'closed' if i>=4 else 'master'})
    files=[];hashes={}
    for i,frame in enumerate(frames):
        f=P/f'frames/helmet/death-ground-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    m['name']='Veld west dry collapse canonical helmet candidate';m['equipment']='diving-helmet';m['states'][0]['frameFiles']=files
    data={'helmetIdle':HELM.relative_to(R).as_posix(),'helmetIdleSha256':sha(HELM),'nativeComponent':COMP.relative_to(R).as_posix(),'nativeComponentSha256':sha(COMP),'nativeAnchor':[17,35],'sourceNecks':NECKS,'frames':records,'expression':{'generation':'exec-93010918-558a-4ddd-83f9-9c1735b99eb6','source':source.relative_to(P).as_posix(),'sourceSha256':sha(source),'sourceCrop':[204,612,308,670],'sourceSkinReference':[310,710,400,820],'nativeRegion':[5,17,9,19],'gain':gain.tolist(),'affectedFrames':[4,5],'protected':'all original component alpha and RGB outside8pixel eye region'},'scope':'paired candidate only, no normal selection'}
    for name,datum in [('helmet-manifest.json',m),('helmet-registration.json',data),('helmet-frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(datum,indent=2)+'\n')
    board=Image.new('RGB',(1536,810),'#202a30');d=ImageDraw.Draw(board)
    bare=[Image.open(P/p).convert('RGBA') for p in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
    for row,seq in enumerate([bare,frames,[first]*6]):
        for i,frame in enumerate(seq):board.paste(frame,(i*256,row*270+16),frame);d.text((i*256+8,row*270),['Bare','Helmet','Selected helmet idle'][row]+f' {i}',fill='white')
    board.save(P/'paired-contact-sheet.png')
    print(json.dumps({'helmetFrames':6,'nativeSize':list(native.size),'eyeRGBPixels':8,'normalSelection':False}))
if __name__=='__main__':main()
