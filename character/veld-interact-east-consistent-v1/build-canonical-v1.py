"""Bounded east scanner interaction, canonical body with preserved arm motion."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import map_coordinates,binary_fill_holes,binary_dilation
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
FIT=ROOT/'character/veld-helmet-fitting-east-v2'
SOURCE=ROOT/'character/veld-shared-helmet-actions-east-v1'

def mask(points):
    im=Image.new('L',(184,184));ImageDraw.Draw(im).polygon(points,fill=255)
    return np.array(im)>0

bare=Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA')
helmet=Image.open(FIT/'frames/equipped-idle-east/000.png').convert('RGBA')
# Same accepted torso underlay as fitting; only formerly occluded side used.
under=Image.open(FIT/'body-underlay-source.png').convert('RGBA')
ys,xs=np.where(np.array(under)[:,:,3]>200);scale=148/(ys.max()-ys.min()+1)
under=under.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)).resize((round((xs.max()-xs.min()+1)*scale),148),Image.Resampling.LANCZOS)
fill=Image.new('RGBA',(184,184));fill.alpha_composite(under,(81,24))
clear=mask([(81,56),(96,56),(99,76),(99,113),(86,113),(80,93)])
fillmask=mask([(89,71),(99,71),(99,113),(88,113)])
polygons={
1:[(84,56),(96,51),(102,57),(105,65),(119,72),(126,66),(139,53),(147,55),(149,64),(139,76),(126,84),(112,86),(100,84),(89,80),(82,70)],
2:[(82,55),(93,52),(101,57),(106,66),(119,68),(127,63),(139,54),(146,55),(147,63),(140,74),(129,81),(115,84),(100,82),(90,78),(82,68)],
3:[(82,55),(93,52),(101,57),(106,66),(119,68),(127,63),(139,54),(146,55),(147,63),(140,74),(129,81),(115,84),(100,82),(90,78),(82,68)],
4:[(83,55),(96,53),(102,62),(104,73),(114,82),(121,84),(123,93),(115,98),(105,96),(95,89),(86,80),(82,68)]}
arms=[]
for i in range(1,5):
    a=np.array(Image.open(SOURCE/f'frames/interact-east/{i:03}.png').convert('RGBA'))
    a[~mask(polygons[i])]=0;arms.append(a)
# One fixed curve for this source clip's neutral sleeve material.
ref=np.array(bare)[56:91,85:98,:3].reshape(-1,3).astype(float)
ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
samples=[]
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    samples.extend(r[m].mean(1))
knots=np.percentile(samples,[0,15,35,55,75,90,100])
target=np.percentile(ref,[0,15,35,55,75,90,100],axis=0)
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
    # Accepted blue science patch; explicit small shoulder region.
    patch=np.array(bare)[57:72,85:100]
    yy,xx=np.mgrid[:184,:184]
    matrix=[];rhs=[]
    for (x,y),(u,v) in zip([(86,55),(96,56),(98,68),(85,67)],[(0,0),(14,0),(14,14),(0,14)]):
        matrix.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);rhs.extend([u,v])
    h=np.linalg.solve(matrix,rhs);den=h[6]*xx+h[7]*yy+1
    u=(h[0]*xx+h[1]*yy+h[2])/den;v=(h[3]*xx+h[4]*yy+h[5])/den
    prgb=patch[:,:,:3].astype(int)
    footprint=binary_dilation(binary_fill_holes((prgb[:,:,2]-prgb[:,:,0]>10)&(prgb[:,:,2]-prgb[:,:,1]>5)),iterations=1)
    region=(u>=0)&(u<=14)&(v>=0)&(v<=14)&(a[:,:,3]>200)
    mapped=map_coordinates(footprint.astype(float),[v,u],order=0,mode='constant')>0
    region &= mapped
    for c in range(3):a[region,c]=map_coordinates(patch[:,:,c].astype(float),[v[region],u[region]],order=1,mode='nearest').astype('uint8')
packs={};outputs={}
state=next(s for s in json.loads((SOURCE/'manifest.json').read_text())['states'] if s['id']=='interact-east')
for variant,idle in [('bare',bare),('helmet',helmet)]:
    base=np.array(idle).copy();base[clear]=0;base[fillmask]=np.array(fill)[fillmask]
    frames=[idle.copy()]
    for a in arms:
        out=Image.fromarray(base.copy());out.alpha_composite(Image.fromarray(a));frames.append(out)
    frames.append(idle.copy());outputs[variant]=frames
    paths=[]
    for i,im in enumerate(frames):
        name=f'frames/{variant}/{i:03}.png';(HERE/name).parent.mkdir(parents=True,exist_ok=True);im.save(HERE/name);paths.append(name)
        assert np.array_equal(np.array(im)[115:],np.array(idle)[115:])
        assert np.array_equal(np.array(im)[:51],np.array(idle)[:51])
    entry=dict(state,frameFiles=paths,frameCount=6)
    pack={'name':'Veld canonical east scanner interaction '+variant,'status':'staged_not_installed','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[entry]}
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
    rgb=[]
    for im in frames:
        bg=Image.new('RGB',im.size,'#202a30');bg.paste(im,mask=im);rgb.append(bg)
    palette=Image.new('RGB',(184*6,184))
    for i,im in enumerate(rgb):palette.paste(im,(184*i,0))
    pal=palette.quantize(colors=256)
    gif=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in rgb]
    gif[0].save(HERE/f'{variant}-canonical-v1.gif',save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    decoded=Image.open(HERE/f'{variant}-canonical-v1.gif')
    for i,im in enumerate(frames):
        decoded.seek(i);pixels=np.array(decoded.convert('RGB')).astype(int)
        if i==0: first=pixels.copy()
        assert np.array_equal(pixels[115:],first[115:])
        assert np.array_equal(pixels[:51],first[:51])
        alpha=np.array(im)[:,:,3]
        exterior=(alpha==0)&(distance_transform_edt(alpha<200)>2)
        assert np.abs(pixels[exterior]-[32,42,48]).max()<=3
contact=Image.new('RGBA',(184*6,208*2),'#202a30');d=ImageDraw.Draw(contact)
for row,(variant,frames) in enumerate(outputs.items()):
    for i,im in enumerate(frames):contact.alpha_composite(im,(184*i,row*208+24));d.text((184*i+4,row*208+4),f'{variant} {i}',fill='white')
contact.save(HERE/'contact.png')
(HERE/'checks.json').write_text(json.dumps({'fixed_head_and_lower_body':True,'exact_idle_endpoints':True,'decoded_gif_frames_checked':12,'decoded_fixed_regions_exact':True,'decoded_exterior_max_error':3,'original_timing':state['frameDurationsMs'],'arm_polygons':polygons,'neutral_curve':{'source':knots.tolist(),'reference':target.tolist()},'installed':False,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE/f'frames/interact-east/{i:03}.png' for i in range(6)]}},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east interaction</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:14px}a{color:#8cc6e7}</style><h1>Veld — east scanner interaction</h1><p>Fixed accepted face, hair, torso and legs; isolated scanner arm motion. Matching subdued helmet. Staged for review.</p>'
for variant in outputs:
    html+=f'<h2>{variant}</h2>'
    for h in [184,102,67,34]:html+=f'<img src="{variant}-canonical-v1.gif" height="{h}">'
html+='<p><a href="contact.png">All poses</a></p>'
(HERE/'index.html').write_text(html,encoding='utf-8')
print('Staged 6 bare and 6 equipped interaction poses; endpoints, fixed head/body and timing checked.')
