"""Stage independently authored distress; never change selected bindings."""
from pathlib import Path
import hashlib, json, copy
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

H = Path(__file__).resolve().parent
R = H.parents[1]
KEY = 'swim-distress-west'
REF = R/'character/veld-water-west-coherent-v1/frames/bare/swim-west/000.png'
HELM = R/'character/veld-shared-helmet-v1/fitted-west.png'
SOURCE = H/'sources/distress-v1.png'
# Source-crop foreground glove outlines; restore original authored pixels only.
# These are occlusion masks, not painted anatomy or mirrored east equipment.
GLOVES={
    1:[(169,131),(187,128),(205,135),(215,147),(221,172),(207,178),(175,172),(164,159),(163,146)],
    2:[(169,117),(175,109),(181,108),(193,123),(199,126),(206,124),(216,134),(215,146),(207,161),(194,169),(182,160),(172,143),(164,133)],
    3:[(128,113),(143,113),(151,123),(156,132),(163,128),(174,136),(171,151),(166,170),(150,170),(133,158),(122,143),(123,135),(119,129),(125,121)]}

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def face(a):
    v = a[:,:,:3].astype(float)
    m = (a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)
    lab,n = label(m); sizes = np.bincount(lab.ravel())
    assert n, 'No face landmark'
    return lab == (1+np.argmax(sizes[1:]))
def box(mask):
    y,x = np.where(mask)
    return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def materials(a):
    v=a[:,:,:3].astype(float); fb=box(face(a)); f=fb[3]-fb[1]
    Y,X=np.indices(a.shape[:2]); opaque=a[:,:,3]>200
    head=(Y<fb[3])&(X>fb[0]-f*.12)&(X<fb[2]+f*1.35)
    hair=head&opaque&(v[:,:,0]>v[:,:,1]*1.13)&(v[:,:,1]>v[:,:,2]*1.12)&~face(a)
    return {'skin':face(a),'hair':hair,
        'cloth':~head&opaque&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),
        'patch':~head&opaque&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)}

def main():
    raw=np.array(Image.open(SOURCE).convert('RGBA'))
    lab,n=label(raw[:,:,3]>160); sizes=np.bincount(lab.ravel())
    ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:6]
    assert len(ids)==6 and all(sizes[k]>10000 for k in ids)
    ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/3)),np.where(lab==k)[1].mean()))
    crops=[]; records=[]
    for i,k in enumerate(ids):
        b=box(lab==k); b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2]
        assert b[0]>=0 and b[1]>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0]
        cut=raw.copy(); cut[~binary_dilation(lab==k,iterations=2)]=0
        im=Image.fromarray(cut).crop(b); a=np.array(im); fb=box(face(a))
        crops.append(a); records.append({'slot':i,'crop':b,'face':fb})
        p=H/f'sources/crops/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True); im.save(p)
    ref=np.array(Image.open(REF).convert('RGBA')); rv=ref[:,:,:3].astype(float)
    rm=materials(ref); q=[0,15,35,55,75,90,100]
    curves={}
    for key,mask in rm.items():
        pooled=np.concatenate([a[:,:,:3][materials(a)[key]] for a in crops]).astype(float)
        assert len(pooled)>30 and np.count_nonzero(mask)>5, key
        curves[key]={'knots':np.percentile(pooled.mean(1),q),'targets':np.percentile(rv[mask],q,axis=0)}
    face_height=box(face(ref))[3]-box(face(ref))[1]
    scale=face_height/float(np.median([r['face'][3]-r['face'][1] for r in records]))
    rfb=box(face(ref)); target=[rfb[0],rfb[3]]
    head=Image.open(HELM).convert('RGBA').rotate(16,resample=Image.Resampling.BICUBIC,expand=True)
    hfb=box(face(np.array(head))); headpos=(target[0]-hfb[0],target[1]-hfb[3])
    images={'bare':[],'helmet':[]}; checks=0
    for a,record in zip(crops,records):
        graded=a.copy(); v=a[:,:,:3].astype(float)
        for key,mask in materials(a).items():
            for c in range(3): graded[mask,c]=np.interp(v[mask].mean(1),curves[key]['knots'],curves[key]['targets'][:,c]).clip(0,255).astype('uint8')
        im=Image.fromarray(graded); im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
        fb=record['face']; pos=(round(target[0]-fb[0]*scale),round(target[1]-fb[3]*scale))
        bare=Image.new('RGBA',(256,256)); bare.alpha_composite(im,pos)
        clear=(target[0]-2,target[1]-34,target[0]+34,target[1]+1)
        helmet=bare.copy(); helmet.paste((0,0,0,0),clear); helmet.alpha_composite(head,headpos)
        if record['slot'] in GLOVES:
            mask=Image.new('L',(a.shape[1],a.shape[0]));ImageDraw.Draw(mask).polygon(GLOVES[record['slot']],fill=255)
            mask=mask.resize(im.size,Image.Resampling.LANCZOS)
            native_mask=Image.new('L',(256,256));native_mask.paste(mask,pos)
            foreground=(np.array(native_mask)>127)&(np.array(bare)[:,:,3]>20)
            ar=np.array(helmet);original=np.array(bare);ar[foreground]=original[foreground];helmet=Image.fromarray(ar)
            native_mask.save(H/f'sources/crops/glove-mask-{record["slot"]:03}.png')
            assert np.array_equal(np.array(helmet)[foreground],original[foreground]);checks+=1
            record['foregroundGloveSourcePolygon']=GLOVES[record['slot']]
            record['foregroundPixelCount']=int(foreground.sum())
        # Protect all body pixels outside the native head operation.
        before=np.array(bare); after=np.array(helmet); protected=np.ones((256,256),bool)
        protected[clear[1]:clear[3],clear[0]:clear[2]]=False
        protected[headpos[1]:headpos[1]+head.height,headpos[0]:headpos[0]+head.width]=False
        assert np.array_equal(before[protected],after[protected]);checks+=1
        record.update(scale=scale,bodyPosition=pos,headPosition=headpos,clear=clear)
        for gear,image in [('bare',bare),('helmet',helmet)]:
            ar=np.array(image)
            assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
            file=H/f'frames/{gear}/{KEY}/{record["slot"]:03}.png';file.parent.mkdir(parents=True,exist_ok=True);image.save(file)
            images[gear].append(image)
    for gear in images:
        parent=R/f'character/dr-veld-v2/packs/{gear}-256x256-p128.0-128.0/manifest.json'
        inherited=json.loads(parent.read_text()); state=copy.deepcopy(next(s for s in inherited['states'] if s['id']==KEY))
        state['frameFiles']=[f'frames/{gear}/{KEY}/{i:03}.png' for i in range(6)]
        manifest={**inherited,'name':'Veld authored west swimming distress '+gear,'states':[state],
            'status':'staged_candidate_pending_native_lifecycle_clearance_and_motion_review'}
        (H/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        # Preview cumulative timing is rounded once, avoiding per-slot GIF drift.
        durations=[160]*6
        bg=[]
        for im in images[gear]:
            canvas=Image.new('RGBA',im.size,'#202a30');canvas.alpha_composite(im);bg.append(canvas.convert('RGB'))
        bg[0].save(H/f'{gear}-distress.gif',save_all=True,append_images=bg[1:],duration=durations,loop=0,disposal=2)
    board=Image.new('RGBA',(7*256,2*280),'#202a30'); d=ImageDraw.Draw(board)
    for row,gear in enumerate(images):
        reference=Image.open(R/f'character/veld-water-west-coherent-v1/frames/{gear}/swim-west/000.png').convert('RGBA')
        board.alpha_composite(reference,(0,row*280+24));d.text((8,row*280+4),gear+' selected swim',fill='white')
        for i,im in enumerate(images[gear]):
            board.alpha_composite(im,((i+1)*256,row*280+24));d.text(((i+1)*256+8,row*280+4),'distress '+str(i),fill='white')
    board.save(H/'paired-contact.png')
    native=Image.new('RGBA',(7*142,2*165),'#202a30'); d=ImageDraw.Draw(native)
    for row,gear in enumerate(images):
        refim=Image.open(R/f'character/veld-water-west-coherent-v1/frames/{gear}/swim-west/000.png').convert('RGBA')
        for i,im in enumerate([refim]+images[gear]):
            native.alpha_composite(im.resize((142,142),Image.Resampling.LANCZOS),(i*142,row*165+20))
            d.text((i*142+3,row*165+2),gear+(' master' if i==0 else ' '+str(i-1)),fill='white')
    native.save(H/'station-scale-contact.png')
    detail=Image.new('RGBA',(1440,480),'#202a30')
    for row,gear in enumerate(images):
        for i,im in enumerate(images[gear]):
            detail.alpha_composite(im.crop((66,90,146,170)).resize((240,240),Image.Resampling.NEAREST),(i*240,row*240))
    detail.save(H/'collar-glove-detail.png')
    evidence={'checks':checks,'failures':0,'selected':False,'sourceSha256':digest(SOURCE),
        'references':{p.relative_to(R).as_posix():digest(p) for p in [REF,HELM]},'records':records,
        'curves':{k:{name:value.tolist() for name,value in c.items()} for k,c in curves.items()},
        'frameHashes':{p.relative_to(H).as_posix():digest(p) for p in sorted((H/'frames').rglob('*.png'))},
        'scope':'fixed atlas face ruler; pooled four-material grade; native master helmet; protected body and borders. No runtime/lifecycle/clearance or owner acceptance proof.'}
    (H/'build-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (H/'index.html').write_text('<meta charset="utf-8"><title>Veld west swimming distress candidate</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:24px}img{max-width:100%}</style><h1>Veld west swimming distress — candidate</h1><p>Independent authored collar-touch/weak-scull loop, selected swimming ruler and pooled matte material grade. Six160ms slots. Native entry resets to frame zero at two visual-clock offsets; subsequent slots use cosmetic time. Staged: real-room clearance, disk restoration and full motion/handoff review remain. Existing runtime selection is unchanged.</p><h2>Station scale comparison with selected swimming</h2><img src="station-scale-contact.png"><h2>Motion</h2><img src="bare-distress.gif"><img src="helmet-distress.gif"><p><a href="paired-contact.png">Full-density contact</a> · <a href="collar-glove-detail.png">Collar/glove detail</a></p>')
    print(f'{checks} protected-body/border checks PASS;12candidate frames. Frozen scale {scale:.6f}; native face target {target}.')

if __name__=='__main__': main()
