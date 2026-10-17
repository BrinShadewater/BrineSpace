from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; C=P.parent
cycles={'bill':{'south':2,'east':1,'north':1,'west':2},'branforth':{'south':3,'east':2,'north':1,'west':2},'veld':dict.fromkeys(['south','east','north','west'],1)}
replacements={'walk-south':'bill-video-south-v3','walk-north':'bill-video-north-v5'}
clips={};checks=[];hashes={}
for who in ['bill','veld','branforth']:
    root=C/'crew-darker-suits-v1'/who;m=json.loads((root/'manifest.json').read_text());dst=P/who;states=[];strides={}
    for entry in m['states']:
        s=dict(entry);key=s['id'];direction=key.split('-')[-1];source=root
        if who=='bill' and key in replacements:
            source=C/replacements[key];s=dict(json.loads((source/'manifest.json').read_text())['states'][0])
        paths=[];ims=[]
        for n,f in enumerate(s['frameFiles']):
            sf=source/f
            if who=='bill' and key in ['idle-south','idle-north']:sf=C/replacements[key.replace('idle','walk')]/'master-standing.png'
            hashes[str(sf.relative_to(C))]=hashlib.sha256(sf.read_bytes()).hexdigest();im=Image.open(sf).convert('RGBA')
            dest=dst/'frames'/key/f'{n:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);paths.append(dest.relative_to(dst).as_posix());ims.append(im)
        # One fixed material correction per clip. Preserve head, alpha, bright
        # metal and saturated patches; never increase a pixel's mean brightness.
        samples=[]
        for im in ims:
            a=np.array(im);v=a[:,:,:3].astype(float);yy=np.indices(a.shape[:2])[0];top=np.where(a[:,:,3]>=128)[0].min()
            mask=(a[:,:,3]>=128)&(yy>=top+27)&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<110)
            samples.append(np.median(v[mask],axis=0))
        base=np.median(samples,axis=0);target=np.array([58.,57.,58.]);target*=min(1,base.mean()/target.mean());gain=target/base
        for n,im in enumerate(ims):
            a=np.array(im);v=a[:,:,:3].astype(float);yy=np.indices(a.shape[:2])[0];top=np.where(a[:,:,3]>=128)[0].min();value=v.mean(axis=2)
            weight=np.clip((32-np.ptp(v,axis=2))/16,0,1)*np.clip((130-value)/35,0,1)*(yy>=top+27)*(a[:,:,3]>0)
            corrected=v*gain;corrected*=np.minimum(1,value/np.maximum(corrected.mean(axis=2),.001))[:,:,None]
            b=a.copy();b[:,:,:3]=np.rint(v+(corrected-v)*weight[:,:,None]).clip(0,255).astype('uint8')
            assert np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[yy<top+27],b[yy<top+27])
            assert np.max(b[:,:,:3].mean(axis=2)-v.mean(axis=2))<=.50001
            ims[n]=Image.fromarray(b);ims[n].save(dst/paths[n])
        original=list(s['frameDurationsMs']);s['frameFiles']=paths
        if key.startswith('walk-'):
            count=cycles[who][direction];total=1500*count;dur=[round((i+1)*total/len(ims))-round(i*total/len(ims)) for i in range(len(ims))]
            s.update(frameDurationsMs=dur,gaitCycles=count);strides[key]=69/384*count
        s['provenance']=dict(source=str(source.relative_to(C)),sourceDurationsMs=original,neutralGain=gain.tolist(),method='Latest accepted motion, fixed per-clip neutral-body correction; head and alpha unchanged. No pixel mean brightening beyond rounding. Matched 1500ms per gait cycle.')
        states.append(s);clips[who,key]=(ims,s['frameDurationsMs'])
        bs=[];cols=[]
        for im in ims:
            a=np.array(im);v=a[:,:,:3].astype(float);ys,xs=np.where(a[:,:,3]>=128);bs.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
            mask=(a[:,:,3]>=128)&(np.ptp(v,axis=2)<24)&(v.mean(axis=2)>25)&(v.mean(axis=2)<145);cols.append(np.median(v[mask],axis=0))
        checks.append(dict(character=who,state=key,count=len(ims),heightRange=[min(b[3]-b[1] for b in bs),max(b[3]-b[1] for b in bs)],soleRange=[min(b[3] for b in bs),max(b[3] for b in bs)],clipped=sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bs),neutralMedian=np.median(cols,axis=0).tolist()))
    (dst/'manifest.json').write_text(json.dumps(dict(name=who+' accepted bare idle/walk override',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,strideDistanceCells=strides,states=states),indent=2))
def at(ims,durs,t):
    t%=sum(durs)
    for im,d in zip(ims,durs):
        if t<d:return im
        t-=d
    return ims[-1]
for transition in [False,True]:
    out=[]
    for tick in range(120):
        bg=Image.new('RGB',(828,1016),'#263139');d=ImageDraw.Draw(bg);t=tick*50
        for col,who in enumerate(['bill','veld','branforth']):
            for row,direction in enumerate(['south','east','north','west']):
                state='idle' if transition and (t<750 or t>=5250) else 'walk';im=at(*clips[who,state+'-'+direction],max(0,t-750) if transition else t);x=col*276;y=row*254
                d.text((x+8,y+5),f'{who.upper()} {direction} / {state}',fill='white');big=im.resize((230,230),Image.Resampling.NEAREST);bg.paste(big,(x+5,y+22),big);small=im.resize((65,65),Image.Resampling.LANCZOS);bg.paste(small,(x+208,y+177),small)
        out.append(bg)
    out[0].save(P/('transitions.gif' if transition else 'cast.gif'),save_all=True,append_images=out[1:],duration=50,loop=0,optimize=False)
for f,h in hashes.items():assert hashlib.sha256((C/f).read_bytes()).hexdigest()==h
(P/'checks.json').write_text(json.dumps(checks,indent=2));(P/'source-hashes.json').write_text(json.dumps(hashes,indent=2))
assert sum(c['clipped'] for c in checks)==0
print(f'{len(checks)} states; {sum(c["count"] for c in checks)} frames; zero clipping; source files unchanged')
