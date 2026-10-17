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
clear=mask([(84,82),(99,82),(100,94),(99,113),(86,113),(82,94)])
fillmask=mask([(89,82),(99,82),(99,113),(88,113)])
far_clear=mask([(115,87),(124,87),(127,96),(125,107),(118,113),(114,112),(113,100)])
polygons={
1:[(88,74),(99,73),(108,76),(119,72),(126,66),(139,53),(147,55),(149,64),(139,76),(126,84),(112,86),(100,84),(90,81)],
2:[(88,74),(98,72),(108,72),(119,68),(127,63),(139,54),(146,55),(147,63),(140,74),(129,81),(115,84),(100,82),(90,79)],
3:[(88,74),(98,72),(108,72),(119,68),(127,63),(139,54),(146,55),(147,63),(140,74),(129,81),(115,84),(100,82),(90,79)],
4:[(87,74),(98,73),(104,77),(114,82),(121,84),(123,93),(115,98),(105,96),(95,89),(88,81)]}
arms=[]
for i in range(1,5):
    a=np.array(Image.open(SOURCE/f'frames/interact-east/{i:03}.png').convert('RGBA'))
    a[~mask(polygons[i])]=0;arms.append(a)
# One fixed curve for this source clip's neutral sleeve material.
ref=np.array(bare)[56:91,85:98,:3].reshape(-1,3).astype(float)
ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
saved=json.loads((HERE/'neutral-curve-canonical-v1.json').read_text())
knots=np.array(saved['source']);target=np.array(saved['reference'])
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
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
        assert np.array_equal(np.array(im)[54:72,82:99],np.array(idle)[54:72,82:99])
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
    gif[0].save(HERE/f'{variant}-arm-attachment-v2.gif',save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    decoded=Image.open(HERE/f'{variant}-arm-attachment-v2.gif')
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
(HERE/'checks.json').write_text(json.dumps({'fixed_head_and_lower_body':True,'exact_idle_endpoints':True,'decoded_gif_frames_checked':12,'decoded_fixed_regions_exact':True,'decoded_exterior_max_error':3,'original_timing':state['frameDurationsMs'],'arm_polygons':polygons,'shoulder_preserved':True,'far_idle_glove_cleared':True,'neutral_curve':{'source':knots.tolist(),'reference':target.tolist()},'installed':False,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE/f'frames/interact-east/{i:03}.png' for i in range(6)]}},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east interaction</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:14px}a{color:#8cc6e7}</style><h1>Veld — east scanner interaction</h1><p>Fixed accepted face, hair, torso and legs; Accepted shoulder and patch retained; repaired elbow/forearm attachment and cleared idle glove. Matching subdued helmet. Staged for review.</p>'
for variant in outputs:
    html+=f'<h2>{variant}</h2>'
    for h in [184,102,67,34]:html+=f'<img src="{variant}-arm-attachment-v2.gif" height="{h}">'
html+='<p><a href="contact.png">All poses</a></p>'
(HERE/'index.html').write_text(html,encoding='utf-8')
print('Staged 6 bare and 6 equipped interaction poses; endpoints, fixed head/body and timing checked.')
