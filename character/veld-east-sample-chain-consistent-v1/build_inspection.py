"""Transfer generated inspection forearms onto the exact accepted kneeling body."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent
source=Image.open(HERE/'inspection-source-v1.png').convert('RGBA')
reference=Image.open(HERE/'frames/bare/kneel-east/005.png').convert('RGBA')
ref=np.array(reference);ry,rx=np.where(ref[:,:,3]>200)
ref_foot=np.where(ref[ry.max()-5:ry.max()+1,:,3]>200)[1].mean()
w,h=source.size
cells=[source.crop((round(i*w/6),0,round((i+1)*w/6),h)) for i in range(6)]
y,x=np.where(np.array(cells[0])[:,:,3]>200)
scale=(ry.max()-ry.min()+1)/(y.max()-y.min()+1)
points=[(110,118),(119,114),(127,108),(134,97),(140,90),(148,84),(156,87),(158,113),(148,126),(134,134),(119,137),(110,130)]
mask_im=Image.new('L',(184,184));ImageDraw.Draw(mask_im).polygon(points,fill=255)
area=np.array(mask_im)>0
arms=[];registration=[]
for i in range(1,5):
    cell=cells[i];a=np.array(cell);y,x=np.where(a[:,:,3]>200)
    foot=np.where(a[y.max()-5:y.max()+1,:,3]>200)[1].mean()
    left=round(ref_foot-foot*scale);top=round(ry.max()-y.max()*scale)
    scaled=cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS)
    registered=Image.new('RGBA',(184,184));registered.alpha_composite(scaled,(left,top))
    a=np.array(registered);a[~area]=0
    a[a[:,:,3]<60]=0
    # Sleeve/glove region contains no skin; remove colored edge contamination.
    rgb=a[:,:,:3].astype(float)
    edge=(a[:,:,3]>0)&(a[:,:,3]<220)&(np.ptp(rgb,axis=2)>35)
    a[edge,:3]=np.rint(rgb[edge].mean(1))[:,None].astype('uint8')
    arms.append(a);registration.append({'cell':i,'offset':[left,top]})
# Match one neutral sleeve curve to the accepted elbow/forearm, all cells together.
ref_rgb=ref[114:130,110:136,:3].reshape(-1,3).astype(float)
ref_rgb=ref_rgb[(np.ptp(ref_rgb,axis=1)<24)&(ref_rgb.mean(1)>15)&(ref_rgb.mean(1)<125)]
samples=[]
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);samples.extend(r[m].mean(1))
knots=np.percentile(samples,[0,15,35,55,75,90,100]);target=np.percentile(ref_rgb,[0,15,35,55,75,90,100],axis=0)
for a in arms:
    r=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
contact=Image.new('RGBA',(1104,416),'#202a30');d=ImageDraw.Draw(contact)
original=json.loads((HERE/'original-selection.json').read_text())
durations=original['repair-east']['durations']
for row,variant in enumerate(['bare','helmet']):
    idle=Image.open(HERE/f'frames/{variant}/kneel-east/005.png').convert('RGBA')
    base=np.array(idle);base[area]=0
    frames=[idle.copy()]
    for arm in arms:
        im=Image.fromarray(base.copy());im.alpha_composite(Image.fromarray(arm));frames.append(im)
    frames.append(idle.copy())
    assert len({hashlib.sha256(np.array(im).tobytes()).hexdigest() for im in frames[1:5]})==4
    paths=[];rgb=[]
    for i,im in enumerate(frames):
        assert np.array_equal(np.array(im)[~area],np.array(idle)[~area])
        assert not np.array_equal(np.array(im),np.array(idle)) or i in [0,5]
        name=f'frames/{variant}/repair-east/{i:03}.png';(HERE/name).parent.mkdir(parents=True,exist_ok=True);im.save(HERE/name);paths.append(name)
        bg=Image.new('RGB',(184,184),'#202a30');bg.paste(im,mask=im);rgb.append(bg)
        contact.alpha_composite(im,(i*184,row*208+24));d.text((i*184+4,row*208+4),f'{variant} {i}',fill='white')
    assert np.array_equal(np.array(frames[0]),np.array(frames[-1]))
    pal_sheet=Image.new('RGB',(1104,184))
    for i,im in enumerate(rgb):pal_sheet.paste(im,(i*184,0))
    palette=pal_sheet.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb]
    name=f'{variant}-repair-east-inspection-v1.gif';gif[0].save(HERE/name,save_all=True,append_images=gif[1:],duration=durations,loop=0,optimize=False,disposal=2)
    with Image.open(HERE/name) as decoded:
        first=None
        for i,frame in enumerate(frames):
            decoded.seek(i);pix=np.array(decoded.convert('RGB')).astype(int)
            if first is None:first=pix.copy()
            assert np.array_equal(pix[~area],first[~area])
            alpha=np.array(frame)[:,:,3];outside=(alpha==0)&(distance_transform_edt(alpha<200)>2)
            assert np.abs(pix[outside]-[32,42,48]).max()<=3
    path=HERE/f'{variant}-manifest.json';manifest=json.loads(path.read_text())
    manifest['states']=[s for s in manifest['states'] if s['id']!='repair-east']
    manifest['states'].append({'id':'repair-east','frameFiles':paths,'frameCount':6,'frameDurationsMs':durations,'loop':True})
    path.write_text(json.dumps(manifest,indent=2)+'\n')
contact.save(HERE/'inspection-contact.png')
(HERE/'inspection-checks.json').write_text(json.dumps({'source_sha256':hashlib.sha256((HERE/'inspection-source-v1.png').read_bytes()).hexdigest(),'fixed_scale':scale,'registration':registration,'arm_mask':points,'outside_arm_pixel_exact':True,'exact_kneel_stand_joins':True,'original_timing':durations,'decoded_gif_frames_checked':12,'neutral_curve':{'source':knots.tolist(),'reference':target.tolist()},'status':'owner_accepted_installed'},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld sample inspection</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld — sample inspection</h1><p>Lift, turn and adjust the vial, then return to the accepted kneeling hold. Face, shoulder patch, body and legs fixed. Exact kneel/inspect/stand joins. Accepted and installed.</p>'
for variant in ['bare','helmet']:
    html+=f'<h2>{variant}</h2>'
    for height in [184,102,67,34]:html+=f'<img src="{variant}-repair-east-inspection-v1.gif" height="{height}">'
html+='<p><a href="inspection-contact.png">Inspection poses</a> / <a href="contact.png">Accepted crouch poses</a></p>'
(HERE/'index.html').write_text(html,encoding='utf-8')
print('12 inspection references staged: fixed body/head, four distinct interiors, exact joins, timing and decoded GIF checks pass.')
