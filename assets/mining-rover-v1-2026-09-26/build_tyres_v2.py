"""Cylindrical rolling of authored tread detail with stationary tyre lighting."""
from pathlib import Path
import json, math, sys
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageChops
R=Path(__file__).resolve().parent
OUT=R/'tyres-v2';OUT.mkdir(exist_ok=True)
D=json.loads((R/'manifest.json').read_text())
SIZE=448

def rig(heading,padding=None):
    if padding is None:padding=8 if heading in ["east","southeast","southwest","northwest"] else 4
    meta=D['headings'][heading];base=Image.open(R/meta['pose']).convert('RGBA');a=np.array(base)
    if heading=='south':
        u=np.array([0.,1.]);hubs=[((b[0]+b[2])/2,(b[1]+b[3])/2) for b in meta['tyreBounds']]
        sizes=[((b[3]-b[1])/2,(b[2]-b[0])/2) for b in meta['tyreBounds']]
        factors=(1.05,1.06)
    else:
        u=np.array(meta['source']['axis']);hubs=meta['wheelHubs'];sizes=[np.array(meta['source']['radii'])*meta['scale']]*4
        factors=(1.20,1.25) if heading in ['north','east','west'] else (1.35,1.6)
    v=np.array([-u[1],u[0]]);Y,X=np.indices((SIZE,SIZE),dtype=float)
    # Median separates the authored small tread studs from the large fixed lighting.
    diffuse=ndimage.median_filter(a[:,:,:3],size=(9,9,1)).astype(float)
    detail=a[:,:,:3].astype(float)-diffuse
    wheels=[];union=np.zeros((SIZE,SIZE),bool)
    for hub,(l,w) in zip(hubs,sizes):
        L=l*factors[0];W=w*factors[1];cx,cy=hub
        box=(max(0,int(cx-L-W-7)),max(0,int(cy-L-W-7)),min(SIZE,int(cx+L+W+8)),min(SIZE,int(cy+L+W+8)))
        x0,y0,x1,y1=box;x=X[y0:y1,x0:x1];y=Y[y0:y1,x0:x1]
        du=(x-cx)*u[0]+(y-cy)*u[1];dv=(x-cx)*v[0]+(y-cy)*v[1]
        plate=diffuse[y0:y1,x0:x1];lum=plate.mean(2);neutral=plate.max(2)-plate.min(2)
        interior=(abs(du)<L)&(abs(dv)<W)&(lum>23)&(lum<115)&(neutral<40)&(a[y0:y1,x0:x1,3]>245)
        interior=ndimage.binary_fill_holes(interior)
        weight=ndimage.gaussian_filter(interior.astype(float),.65)*np.clip(np.minimum(L-abs(du),W-abs(dv)),0,1)
        weight*=a[y0:y1,x0:x1,3]>245
        union[y0:y1,x0:x1]|=weight>0
        # Steering moves the rubber shell only, around its axle; yokes stay fixed.
        part=(abs(du/(L+padding))**8+abs(dv/(W+padding))**8<1)&(a[y0:y1,x0:x1,3]>0)
        pm=Image.new('L',(SIZE,SIZE));pm.paste(Image.fromarray((part*255).astype('uint8')),(x0,y0))
        local=a[y0:y1,x0:x1,:3].astype(float)
        residue=detail[y0:y1,x0:x1]
        candidates=(residue.mean(2)>25)&((local.max(2)-local.min(2))<35)&interior
        labels,count=ndimage.label(candidates);studs=np.zeros(candidates.shape,bool)
        for label in range(1,count+1):
            ys,xs=np.where(labels==label)
            if 3<=len(xs)<=65 and max(np.ptp(xs)+1,np.ptp(ys)+1)/max(1,min(np.ptp(xs)+1,np.ptp(ys)+1))<2.8:
                studs|=labels==label
        studmask=ndimage.binary_dilation(studs,iterations=2).astype(float)*weight
        isolated=residue*studmask[:,:,None]
        clean=local-isolated
        wheels.append(dict(box=box,du=du,dv=dv,L=L,W=W,hub=hub,weight=weight,part=pm,detail=isolated,clean=clean))
    front=sorted(range(4),key=lambda i:np.dot(np.subtract(hubs[i],(224,224)),u),reverse=True)[:2]
    def roll(phase):
        out=a.copy()
        for wheel in wheels:
            x0,y0,x1,y1=wheel['box'];du=wheel['du'];dv=wheel['dv'];L=wheel['L'];cx,cy=wheel['hub'];weight=wheel['weight'][:,:,None]
            theta=np.arcsin(np.clip(du/L,-1,1));angle=(theta-phase*math.pi+math.pi/2)%math.pi-math.pi/2
            sample=L*np.sin(angle);sx=cx+sample*u[0]+dv*v[0];sy=cy+sample*u[1]+dv*v[1]
            moved=np.stack([ndimage.map_coordinates(wheel['detail'][:,:,c],[sy-y0,sx-x0],order=1,mode='constant',cval=0) for c in range(3)],axis=2)
            candidate=wheel['clean']+moved
            out[y0:y1,x0:x1,:3]=np.clip(np.rint(a[y0:y1,x0:x1,:3]*(1-weight)+candidate*weight),0,255).astype('uint8')
        return Image.fromarray(out)
    def steer(im,angle):
        out=im.copy()
        for i in front:
            wheel=wheels[i];pm=wheel['part'];part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),pm))
            out.putalpha(ImageChops.multiply(out.getchannel('A'),ImageChops.invert(pm)))
            out.alpha_composite(part.rotate(angle,resample=Image.Resampling.BICUBIC,center=wheel['hub']))
        # Remove only small detached scraps introduced by the cutout rotation.
        ar=np.array(out);labels,count=ndimage.label(ar[:,:,3]>128);counts=np.bincount(labels.ravel())
        scraps=np.isin(labels,[i for i in range(1,count+1) if counts[i]<128])
        ar[ndimage.binary_dilation(scraps,iterations=1),3]=0
        out=Image.fromarray(ar)
        return out
    return base,roll,steer,union,wheels

def main():
    pilot='--pilot' in sys.argv
    headings=['south','northwest'] if pilot else list(D['headings'])
    report=[];samples={}
    for heading in headings:
        base,roll,steer,mask,wheels=rig(heading);a=np.array(base)
        rolling=[roll(n/60) for n in range(60)]
        assert rolling[0].tobytes()==base.tobytes(), (heading,'rolling phase zero must match source')
        if not pilot:
            wheelatlas=Image.new('RGBA',(448*6,448*10))
            for n,frame in enumerate(rolling):
                patch=np.array(frame);patch[:,:,3]=np.where(mask,255,0)
                wheelatlas.paste(Image.fromarray(patch),(n%6*448,n//6*448))
            wp=OUT/'atlases'/f'wheel-layer-{heading}.png';wp.parent.mkdir(exist_ok=True)
            wheelatlas.save(wp,compress_level=3)
            D['headings'][heading]['wheelAtlas']={'path':wp.relative_to(R).as_posix(),'columns':6,'frameCount':60}
        for state in ['drive','reverse','steer-left','steer-right']:
            entry=next(e for e in D['states'] if e['id']==state+'-'+heading)
            frames=[];paths=[];atlas=Image.new('RGBA',(448*6,448*10))
            for n in range(60):
                im=rolling[(-n if state=='reverse' else n)%60].copy()
                if state.startswith('steer'):
                    im=steer(im,(1 if state.endswith('left') else -1)*6*math.sin(math.pi*n/60)**2)
                bounds=im.getbbox();assert min(bounds[:2])>0 and max(bounds[2:])<448
                if state in ['drive','reverse']:
                    ar=np.array(im);assert np.array_equal(ar[:,:,3],a[:,:,3]);assert np.array_equal(ar[~mask],a[~mask])
                folder=OUT/('pilot' if pilot else 'frames')/entry['id'];folder.mkdir(parents=True,exist_ok=True)
                path=folder/f'{n:03}.png';im.save(path,compress_level=3);paths.append(path.relative_to(R).as_posix());frames.append(im)
                atlas.paste(im,(n%6*448,n//6*448))
            if not pilot:
                ap=OUT/'atlases'/f"{entry['id']}.png";ap.parent.mkdir(exist_ok=True);atlas.save(ap,compress_level=3)
                entry['frameFiles']=paths;entry['atlas']={'path':ap.relative_to(R).as_posix(),'columns':6}
                entry['tyreRevision']='v3-phase-zero-and-shared-work-wheels'
                entry['travelWorldUnitsPerSecond']=float(np.mean([w['L'] for w in wheels])*math.pi/2*D['worldUnitsPerPixel'])
                D['headings'][heading]['tyreTravelWorldUnitsPerSecond']=entry['travelWorldUnitsPerSecond']
            samples[heading,state]=frames
            report.append({'clip':entry['id'],'frames':60,'clipping':'pass','staticOutsideTyres':state in ['drive','reverse']})
        print(heading,'complete',flush=True)
    review=[]
    for n in range(0,60,2):
        b=Image.new('RGBA',(896,950),'#17272e');draw=ImageDraw.Draw(b)
        for i,(h,state) in enumerate([('south','drive'),('northwest','drive'),('south','steer-left'),('northwest','steer-left')]):
            x=i%2*448;y=i//2*475;draw.text((x+12,y+9),h+' / '+state,fill='white');b.alpha_composite(samples[h,state][n],(x,y+27))
        review.append(b.convert('RGB'))
    review[0].save(OUT/'review.gif',save_all=True,append_images=review[1:],duration=67,loop=0)
    review[7].save(OUT/'review.png')
    (OUT/'checks.json').write_text(json.dumps(report,indent=2))
    if not pilot:
        old=OUT/'manifest-before.json'
        if not old.exists():old.write_bytes((R/'manifest.json').read_bytes())
        (R/'manifest.json').write_text(json.dumps(D,indent=2))

if __name__=='__main__':main()
