"""Deterministic crew-base derivation trial from existing owner-approved artwork."""
from pathlib import Path
import copy,hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_dilation,binary_fill_holes

P=Path(__file__).resolve().parent;R=P.parent.parent
BASE=R/'character/crew-runtime-matte-v1/bill/manifest.json'
GEAR=R/'character/bill-shared-helmet-runtime-v2/manifest.json'
CONCEPT=R/'character/krusher-concept-v1/concept-04-krusher-dom.png'
for folder in ['sources','frames/bare','frames/helmet','masks','review']:(P/folder).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={str(p.relative_to(R)):sha(p) for p in [BASE,GEAR,CONCEPT]}
base=json.loads(BASE.read_text());gear=json.loads(GEAR.read_text());gearstates={s['id']:s for s in gear['states']}
yy,xx=np.mgrid[:184,:184];records=[];outputs={};heads={}
sheet=Image.open(CONCEPT).convert('RGBA')
crops={'south':[630,274,720,383],'east':[901,274,1006,385],'north':[1175,276,1275,365],'west':[1457,275,1552,387]}
density=None
for direction,rect in crops.items():
    im=sheet.crop(rect);a=np.array(im);rgb=a[:,:,:3].astype(float)
    warm=(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.045)
    labs,n=label(warm);part=max(range(1,n+1),key=lambda k:int((labs==k).sum()))
    alpha=binary_dilation(binary_fill_holes(labs==part),iterations=2)
    a[:,:,3]=alpha.astype('uint8')*255;a[~alpha]=0
    im=Image.fromarray(a);im.save(P/f'sources/{direction}-head-crop.png');im=im.crop(im.getbbox())
    if direction=='south':density=28/im.height
    im=im.resize((round(im.width*density),round(im.height*density)),Image.Resampling.LANCZOS)
    # Keep the already reviewed South head component exactly as the first trial.
    if direction=='south':im=Image.open(R/'character/krusher-bill-base-test-v1/sources/krusher-head-native.png').convert('RGBA')
    im.save(P/f'sources/{direction}-head-native.png');heads[direction]=im

def recolour(a):
    rgb=a[:,:,:3].astype(float)
    mask=(a[:,:,3]>0)&(yy>52)&(yy<112)&(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,0]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>35)
    target=np.array([82.,124.,128.]);lum=rgb@np.array([.2126,.7152,.0722]);tl=float(target@np.array([.2126,.7152,.0722]))
    out=a.copy();colours=np.minimum(255,np.rint(lum[:,:,None]/tl*target)).astype('uint8');out[mask,:3]=colours[mask]
    return out,mask

def registration(a,direction):
    rgb=a[:,:,:3].astype(float)
    top=int(np.where((a[:,:,3]>180)&(xx>70)&(xx<115)&(yy<60))[0].min())
    crown=(a[:,:,3]>180)&(xx>70)&(xx<115)&(yy>=top)&(yy<top+14)
    cy,cx=np.where(crown);axis=round((int(cx.min())+int(cx.max()))/2)
    limit=top+(24 if direction=='north' else 27)
    warm=(a[:,:,3]>150)&(xx>=axis-15)&(xx<=axis+15)&(yy<limit)&(rgb[:,:,0]>rgb[:,:,1]*1.035)&(rgb[:,:,0]>rgb[:,:,2]*1.04)
    labs,n=label(warm);part=max(range(1,n+1),key=lambda k:int((labs==k).sum()));mask=labs==part
    ys,xs=np.where(mask);bottom=int(ys.max())
    erase=binary_dilation(binary_fill_holes(mask),iterations=1)&(yy<=bottom+1)&(yy<limit)
    erase&=~((rgb.max(2)-rgb.min(2)<10)&(yy>bottom-3))
    return axis,bottom,erase

for state in base['states']:
    key=state['id'];direction=key.split('-')[-1];head=heads[direction]
    for variant in ['bare','helmet']:(P/f'frames/{variant}/{key}').mkdir(parents=True,exist_ok=True)
    outputs[key]={'bare':[],'helmet':[],'original':[]}
    for i,(path,gpath) in enumerate(zip(state['frameFiles'],gearstates[key]['frameFiles'])):
        src=BASE.parent/path;gsrc=GEAR.parent/gpath
        for p in [src,gsrc]:hashes[str(p.relative_to(R))]=sha(p)
        a=np.array(Image.open(src).convert('RGBA'));ga=np.array(Image.open(gsrc).convert('RGBA'))
        axis,bottom,erase=registration(a,direction)
        # Profile heads anchor by the neck-facing half, not the protruding nose.
        alpha=np.array(head.getchannel('A'));hy,hx=np.where((alpha>150)&(np.indices(alpha.shape)[0]>=head.height-5))
        headanchor=round((int(hx.min())+int(hx.max()))/2) if direction in ['east','west'] else head.width//2
        dest=(axis-headanchor,bottom+1-head.height)
        body,markings=recolour(a);body[erase]=0;bare=Image.fromarray(body);bare.alpha_composite(head,dest)
        allowed=erase|markings;allowed[dest[1]:dest[1]+head.height,dest[0]:dest[0]+head.width]=True
        Image.fromarray(allowed.astype('uint8')*255).save(P/f'masks/{key}-{i:03}-bare.png')
        equipped,gear_markings=recolour(ga);face_mask=np.zeros((184,184),bool)
        if direction!='north':
            rgb=ga[:,:,:3].astype(float)
            face=(ga[:,:,3]>180)&(xx>axis-20)&(xx<axis+20)&(yy<61)&(rgb[:,:,0]>rgb[:,:,1]*1.10)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb.mean(2)>40)
            labs,n=label(face)
            if not n:raise ValueError(f'No helmet face {key}/{i}')
            part=max(range(1,n+1),key=lambda k:int((labs==k).sum()));face_mask=binary_fill_holes(labs==part)
            fy,fx=np.where(face_mask);box=(int(fx.min()),int(fy.min()),int(fx.max())+1,int(fy.max())+1)
            # Existing visor silhouette is retained exactly; only its face pixels change.
            face_source=head.crop((0,max(0,round(head.height*.18)),head.width,head.height))
            scale=min((box[2]-box[0])/face_source.width,(box[3]-box[1])/face_source.height)
            face_source=face_source.resize((max(1,round(face_source.width*scale)),max(1,round(face_source.height*scale))),Image.Resampling.LANCZOS)
            layer=Image.new('RGBA',(184,184));layer.alpha_composite(face_source,(round((box[0]+box[2]-face_source.width)/2),box[3]-face_source.height))
            la=np.array(layer);paint=face_mask&(la[:,:,3]>60);equipped[paint,:3]=la[paint,:3]
        helmet=Image.fromarray(equipped);gear_allowed=face_mask|gear_markings
        Image.fromarray(gear_allowed.astype('uint8')*255).save(P/f'masks/{key}-{i:03}-helmet.png')
        for variant,image,original,mask in [('bare',bare,a,allowed),('helmet',helmet,ga,gear_allowed)]:
            file=f'frames/{variant}/{key}/{i:03}.png';image.save(P/file);outputs[key][variant].append(image)
            records.append({'state':key,'variant':variant,'frame':i,'source':str((src if variant=='bare' else gsrc).relative_to(R)),'output':file,'editMask':f'masks/{key}-{i:03}-{variant}.png','outsideMaskExact':bool(np.array_equal(original[~mask],np.array(image)[~mask])),'headPaste':list(dest),'headAxis':axis,'headBottom':bottom})
        outputs[key]['original'].append(Image.fromarray(a))

for variant in ['bare','helmet']:
    m=copy.deepcopy(base);m['name']=f'Krusher Dom / Bill base cardinal {variant} trial';m['status']='unselected derived candidate'
    for s in m['states']:
        s['frameFiles']=[f'frames/{variant}/{s["id"]}/{i:03}.png' for i in range(len(s['frameFiles']))]
        s['provenance']='Existing Bill body/gait, matte cyan markings; independently extracted Krusher cardinal concept heads'
    (P/f'{variant}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    for s in m['states']:
        frames=outputs[s['id']][variant];frames[0].save(P/f'review/{variant}-{s["id"]}.png',save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0,disposal=1,blend=0)

board=Image.new('RGB',(1000,780),'#272b2e');d=ImageDraw.Draw(board)
d.text((20,16),'KRUSHER DOM / FOUR-DIRECTION BILL BASE TRIAL',fill='white')
for k,direction in enumerate(['south','east','north','west']):
    for j,variant in enumerate(['bare','helmet']):
        im=outputs['idle-'+direction][variant][0].resize((230,230),Image.Resampling.NEAREST)
        board.paste(im,(k*250+10,j*290+55),im);d.text((k*250+30,j*290+290),f'{direction} / {variant}',fill='white')
    small=outputs['idle-'+direction]['bare'][0].resize((92,92),Image.Resampling.LANCZOS);board.paste(small,(k*250+80,660),small)
board.save(P/'review/cardinal-comparison.png')
report={'frames':len(records),'statesPerVariant':len(base['states']),'records':records,'sourceHashes':hashes,'headCrops':crops,'densityScale':density,'headSizes':{k:list(v.size) for k,v in heads.items()},'failures':[r['output'] for r in records if not r['outsideMaskExact']],'inputsUnchanged':all(sha(R/p)==h for p,h in hashes.items()),'limitations':['No new terminal equipment/action','No expression/blink animation','No normal runtime selection or actor integration','Helmet retains original shell/visor silhouette; face only replaced']}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['frames','statesPerVariant','headSizes','failures','inputsUnchanged']}))
assert not report['failures'] and report['inputsUnchanged']
