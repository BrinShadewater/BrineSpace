from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
COMP=R/'character/veld-shared-helmet-v1/fitted-north.png'
HELM=R/'character/veld-shared-helmet-v1/frames/idle-north/000.png'
NECKS=[[254,122],[768,244],[1267,354],[254,827],[768,878],[1268,878]]
PITCHES=[0,15,0,-35,-80,-80]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    reg=json.loads((P/'bare-registration.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());scale=reg['fixedRuler']
    native=Image.open(COMP).convert('RGBA');native.save(P/'sources/canonical-head.png')
    source=P/'sources/pitched-heads-v1.png';raw=np.array(Image.open(source).convert('RGBA'));labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
    ids=sorted(np.argsort(sizes)[-4:],key=lambda k:np.where(labs==k)[1].mean())
    # One component ruler derives from the authored upright width, never per pitch.
    x=np.where(labs==ids[0])[1];ruler=native.width/(int(x.max()-x.min())+1)
    target=np.array(native);solid=raw[:,:,3]>180;q=[0,15,35,55,75,90,100]
    knots=np.percentile(raw[:,:,:3][solid].mean(1),q);palette=np.percentile(target[:,:,:3][target[:,:,3]>180],q,axis=0);graded=raw.copy()
    for c in range(3):graded[solid,c]=np.interp(raw[:,:,:3][solid].mean(1),knots,palette[:,c]).clip(0,255).astype('uint8')
    source_anchors=[[256,606],[768,611],[1275,158],[1792,157]]
    components=[];pitch_records=[]
    for i,k in enumerate(ids):
        yy,xx=np.where(labs==k);box=[int(xx.min()-3),int(yy.min()-3),int(xx.max()+4),int(yy.max()+4)]
        keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
        head=Image.fromarray(a).crop(box);head=head.resize((round(head.width*ruler),round(head.height*ruler)),Image.Resampling.LANCZOS);components.append(head)
        file=f'sources/fitted-pitch-{i:02}.png';head.save(P/file)
        pitch_records.append({'sourceBox':box,'size':list(head.size),'anchor':[(source_anchors[i][j]-box[j])*ruler for j in range(2)],'file':file,'sha256':sha(P/file),'pitchDegrees':[0,15,-35,-80][i]})
    pitch={'generation':'exec-8a06b411-a4b4-40b6-a58b-a371e667f50b','source':'sources/pitched-heads-v1.png','sourceSha256':sha(source),'fixedRuler':ruler,'calibration':'33native pixels /500opaque authored upright width; same ruler all depth pitches','grade':{'knots':knots.tolist(),'targets':palette.tolist(),'scope':'one pooled atlas luma-to-masterRGB curve before fitting'},'heads':pitch_records}
    (P/'pitch-registration.json').write_text(json.dumps(pitch,indent=2)+'\n')
    first=Image.new('RGBA',(256,256));first.alpha_composite(Image.open(HELM).convert('RGBA'),(36,52));frames=[first];records=[]
    for i,r in enumerate(reg['frames'],1):
        bare=Image.open(P/m['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare)
        neck=[r['position'][j]+(NECKS[i][j]-r['box'][j])*scale for j in range(2)];center=[r['position'][j]+(reg['heads'][i][j]-r['box'][j])*scale for j in range(2)]
        yy,xx=np.indices(b.shape[:2]);local=(xx-center[0])**2+(yy-center[1])**2<18**2;b[local]=0
        pi={1:1,3:2,4:3,5:3}.get(i)
        component=native if pi is None else components[pi];anchor=[16,32] if pi is None else pitch_records[pi]['anchor'];pos=[round(neck[j]-anchor[j]) for j in range(2)]
        out=Image.fromarray(b);out.alpha_composite(component,pos);frames.append(out)
        records.append({'pose':i,'neck':neck,'sourceNeck':NECKS[i],'headCenter':center,'nativeScale':1,'tiltCounterclockwise':0,'forwardPitchDegrees':PITCHES[i],'componentSource':COMP.relative_to(R).as_posix() if pi is None else pitch_records[pi]['file'],'componentPosition':pos,'componentSize':list(component.size),'eraseRadius':18,'expression':'rear face hidden','pitchIndex':pi})
    files=[];hashes={}
    for i,frame in enumerate(frames):
        f=P/f'frames/helmet/lie-down-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);frame.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
    m['name']='Veld north generic rest authored rear helmet candidate';m['equipment']='diving-helmet';m['states'][0]['frameFiles']=files;m['states'][1]['frameFiles']=list(reversed(files));m['states'][2]['frameFiles']=[files[-1]]
    data={'helmetIdle':HELM.relative_to(R).as_posix(),'helmetIdleSha256':sha(HELM),'nativeComponent':COMP.relative_to(R).as_posix(),'nativeComponentSha256':sha(COMP),'nativeAnchor':[16,32],'sourceNecks':NECKS,'frames':records,'pitchRegistrationSha256':sha(P/'pitch-registration.json'),'scope':'paired generic north floor rest; authored backward depth projection, exact selected entry; no normal/furniture/life/death proof'}
    for name,d in [('helmet-manifest.json',m),('helmet-registration.json',data),('helmet-frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(d,indent=2)+'\n')
    board=Image.new('RGB',(1536,810),'#202a30');draw=ImageDraw.Draw(board)
    bare=[Image.open(P/f).convert('RGBA') for f in json.loads((P/'bare-manifest.json').read_text())['states'][0]['frameFiles']]
    for row,seq in enumerate([bare,frames,[first]*6]):
        for i,frame in enumerate(seq):board.paste(frame,(i*256,row*270+16),frame);draw.text((i*256+8,row*270),['Bare','Helmet','Selected helmet idle'][row]+f' {i}',fill='white')
    board.save(P/'paired-contact-sheet.png');print(json.dumps({'helmetFrames':6,'nativeSize':list(native.size),'pitchRuler':ruler,'pitchSizes':[list(c.size) for c in components],'normalSelection':False}))
if __name__=='__main__':main()
