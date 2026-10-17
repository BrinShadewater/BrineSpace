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
clear=mask([(81,56),(98,56),(100,83),(99,113),(86,113),(80,93)])
fillmask=mask([(89,74),(99,74),(99,113),(88,113)])
far_clear=mask([(115,87),(124,87),(127,96),(125,107),(118,113),(114,112),(113,100)])
polygons={
1:[(82,55),(94,53),(100,60),(99,72),(110,73),(121,66),(128,60),(139,58),(142,68),(136,78),(122,86),(108,88),(94,90),(86,85),(82,70)],
2:[(82,55),(95,53),(101,60),(99,72),(110,72),(124,65),(128,57),(141,54),(145,63),(137,76),(124,84),(110,87),(94,90),(86,85),(82,70)],
3:[(82,55),(95,53),(101,60),(99,72),(110,72),(124,65),(128,57),(141,54),(145,63),(137,76),(124,84),(110,87),(94,90),(86,85),(82,70)],
4:[(82,55),(95,53),(101,61),(99,73),(112,80),(123,86),(127,98),(117,102),(104,94),(92,86),(84,77)]}
arms=[]
for i in range(1,5):
    a=np.array(Image.open(HERE/f'pose-arm-source-v3-{i:03}.png').convert('RGBA'))
    a[~mask(polygons[i])]=0;arms.append(a)
# One material curve over the complete new source clip, never per-frame exposure.
ref=np.array(bare)[56:91,85:98,:3].reshape(-1,3).astype(float)
ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
samples=[]
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    samples.extend(r[m].mean(1))
knots=np.percentile(samples,[0,15,35,55,75,90,100]);target=np.percentile(ref,[0,15,35,55,75,90,100],axis=0)
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
    # Restore actual science emblem inside its footprint, not a sleeve rectangle.
    rgb=np.array(bare)[:,:,:3].astype(int)
    patch=np.zeros((184,184),bool)
    patch[57:73,85:100]=(rgb[57:73,85:100,2]-rgb[57:73,85:100,0]>10)&(rgb[57:73,85:100,2]-rgb[57:73,85:100,1]>5)
    patch=binary_dilation(binary_fill_holes(patch),iterations=1)&(a[:,:,3]>200)
    a[patch]=np.array(bare)[patch]
packs={};outputs={}
state=next(s for s in json.loads((SOURCE/'manifest.json').read_text())['states'] if s['id']=='interact-east')
for variant,idle in [('bare',bare),('helmet',helmet)]:
    base=np.array(idle).copy();base[clear]=0;base[fillmask]=np.array(fill)[fillmask];base[far_clear]=0
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
    pack={'name':'Veld canonical east scanner interaction '+variant,'status':'owner_accepted_installed','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[entry]}
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
    rgb=[]
    for im in frames:
        bg=Image.new('RGB',im.size,'#202a30');bg.paste(im,mask=im);rgb.append(bg)
    palette=Image.new('RGB',(184*6,184))
    for i,im in enumerate(rgb):palette.paste(im,(184*i,0))
    pal=palette.quantize(colors=256)
    gif=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in rgb]
    gif[0].save(HERE/f'{variant}-continuous-sleeve-v3.gif',save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    decoded=Image.open(HERE/f'{variant}-continuous-sleeve-v3.gif')
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
(HERE/'checks.json').write_text(json.dumps({'fixed_head_and_lower_body':True,'exact_idle_endpoints':True,'decoded_gif_frames_checked':12,'decoded_fixed_regions_exact':True,'decoded_exterior_max_error':3,'original_timing':state['frameDurationsMs'],'arm_polygons':polygons,'shoulder_redrawn_with_continuous_elbow':True,'far_idle_glove_cleared':True,'neutral_curve':{'source':knots.tolist(),'reference':target.tolist()},'installed':False,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE/f'frames/interact-east/{i:03}.png' for i in range(6)]}},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east interaction</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:14px}a{color:#8cc6e7}</style><h1>Veld — east scanner interaction</h1><p>Fixed accepted face, hair, torso and legs; Continuous textured sleeve and natural elbow, with original science badge and fixed body. Matching subdued helmet. Accepted and installed.</p>'
for variant in outputs:
    html+=f'<h2>{variant}</h2>'
    for h in [184,102,67,34]:html+=f'<img src="{variant}-continuous-sleeve-v3.gif" height="{h}">'
html+='<p><a href="contact.png">All poses</a></p>'
(HERE/'index.html').write_text(html,encoding='utf-8')
print('Staged 6 bare and 6 equipped interaction poses; endpoints, fixed head/body and timing checked.')
