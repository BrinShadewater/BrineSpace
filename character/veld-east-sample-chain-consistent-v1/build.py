"""Registered crouch/rise study; one source scale, exact selected idle joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=Image.open(HERE/'kneel-source-v1.png').convert('RGBA')
original=json.loads((HERE/'original-selection.json').read_text())
bare_idle=Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA')
helmet_idle=Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA')
w,h=source.size
cells=[source.crop((round(i*w/6),0,round((i+1)*w/6),h)) for i in range(6)]
yy,xx=np.where(np.array(cells[0])[:,:,3]>200)
scale=148/(yy.max()-yy.min()+1) # fixed from standing source, never normalized per crouch
registered=[];landmarks=[]
for i,cell in enumerate(cells):
    a=np.array(cell);y,x=np.where(a[:,:,3]>200)
    raw=Image.open(original['kneel-east']['files'][i]).convert('RGBA') if i else bare_idle
    ra=np.array(raw);ry,rx=np.where(ra[:,:,3]>200)
    # Register the forward sole to original staging; stance height stays authored.
    old_sole=np.where(ra[ry.max()-5:ry.max()+1,:,3]>200)[1].max()
    new_sole=np.where(a[y.max()-5:y.max()+1,:,3]>200)[1].max()
    left=round(old_sole-(new_sole-x.min())*scale)
    height=round((y.max()-y.min()+1)*scale)
    top=172-height
    crop=cell.crop((x.min(),y.min(),x.max()+1,y.max()+1)).resize((round((x.max()-x.min()+1)*scale),height),Image.Resampling.LANCZOS)
    frame=Image.new('RGBA',(184,184));frame.alpha_composite(crop,(left,top))
    # Brown bun / face occupies upper source region; track head, not torso bbox.
    r=np.array(frame)[:,:,:3].astype(int);alpha=np.array(frame)[:,:,3]
    warm=(r[:,:,0]-r[:,:,1]>8)&(r[:,:,0]-r[:,:,2]>15)&(alpha>200)
    warm[max(top+30,0):]=False
    hy,hx=np.where(warm)
    head_x=round((hx.min()+hx.max())/2)-105
    head_y=top-24
    registered.append(frame);landmarks.append({'source_top':top,'x_shift':head_x,'y_shift':head_y,'sole_right':int(old_sole)})
registered[0]=bare_idle.copy()
# Reference-calibrated neutral suit curve shared by all five moving poses.
ref=np.array(bare_idle)[56:115,83:116,:3].reshape(-1,3).astype(float)
ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
samples=[]
for frame in registered[1:]:
    a=np.array(frame);r=a[:,:,:3].astype(float)
    m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);samples.extend(r[m].mean(1))
knots=np.percentile(samples,[0,15,35,55,75,90,100]);target=np.percentile(ref,[0,15,35,55,75,90,100],axis=0)
for i in range(1,6):
    a=np.array(registered[i]);r=a[:,:,:3].astype(float)
    m=(a[:,:,3]>0)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
    registered[i]=Image.fromarray(a)
equipped=[helmet_idle.copy()]
head=helmet_idle.crop((79,14,121,59))
for i in range(1,6):
    frame=registered[i].copy();a=np.array(frame)
    dx,dy=landmarks[i]['x_shift'],landmarks[i]['y_shift']
    # Clear bare head before fitting whole accepted head/collar; no bun protrusion.
    a[max(0,14+dy):max(0,50+dy),max(0,78+dx):min(184,122+dx)]=0
    frame=Image.fromarray(a);frame.alpha_composite(head,(79+dx,14+dy));equipped.append(frame)
contact=Image.new('RGBA',(184*6,208*2),'#202a30');d=ImageDraw.Draw(contact)
for row,(variant,frames) in enumerate([('bare',registered),('helmet',equipped)]):
    manifest={'name':'Veld consistent east crouch/rise '+variant,'status':'owner_accepted_installed','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'linear','precomposed':True,'states':[]}
    for key,indices in [('kneel-east',list(range(6))),('stand-east',list(reversed(range(6))))]:
        paths=[];rgb=[]
        for j,i in enumerate(indices):
            frame=frames[i];name=f'frames/{variant}/{key}/{j:03}.png';(HERE/name).parent.mkdir(parents=True,exist_ok=True);frame.save(HERE/name);paths.append(name)
            bg=Image.new('RGB',(184,184),'#202a30');bg.paste(frame,mask=frame);rgb.append(bg)
            a=np.array(frame);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
        palette=Image.new('RGB',(184*6,184))
        for j,im in enumerate(rgb):palette.paste(im,(j*184,0))
        pal=palette.quantize(colors=256);gif=[im.quantize(palette=pal,dither=Image.Dither.NONE) for im in rgb]
        durations=original[key]['durations'];assert len(durations)==6
        name=f'{variant}-{key}-coherent-v1.gif';gif[0].save(HERE/name,save_all=True,append_images=gif[1:],duration=durations,loop=0,optimize=False,disposal=2)
        with Image.open(HERE/name) as decoded:
            for j,i in enumerate(indices):
                decoded.seek(j);pix=np.array(decoded.convert('RGB')).astype(int);a=np.array(frames[i])[:,:,3]
                outside=(a==0)&(distance_transform_edt(a<200)>2);assert np.abs(pix[outside]-[32,42,48]).max()<=3
        manifest['states'].append({'id':key,'frameFiles':paths,'frameCount':6,'frameDurationsMs':durations,'loop':False})
    assert np.array_equal(np.array(frames[0]),np.array(bare_idle if variant=='bare' else helmet_idle))
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for i,frame in enumerate(frames):contact.alpha_composite(frame,(184*i,row*208+24));d.text((184*i+4,row*208+4),f'{variant} {i}',fill='white')
contact.save(HERE/'contact.png')
(HERE/'checks.json').write_text(json.dumps({'source_sha256':hashlib.sha256((HERE/'kneel-source-v1.png').read_bytes()).hexdigest(),'fixed_scale':scale,'registration':landmarks,'exact_idle_joins':True,'reverse_source_joins':True,'decoded_gif_frames_checked':24,'no_clipping':True,'original_timing':True,'sample_inspection_motion_pending':True},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east crouch and rise</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld — east kneel and rise</h1><p>Consistent crouching identity and suit, original staging/timing, exact idle joins. Sample-inspection motion is the next part of this chain. Staged for review.</p>'
for variant in ['bare','helmet']:
    for key in ['kneel-east','stand-east']:
        html+=f'<h2>{variant} / {key}</h2>'
        for height in [184,102,67,34]:html+=f'<img src="{variant}-{key}-coherent-v1.gif" height="{height}">'
html+='<p><a href="contact.png">All poses</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('24 crouch/rise references packaged; fixed scale, idle joins, original timing, alpha/exterior and clipping checks pass.')

# Reproduce the complete staged chain from saved sources when inspection exists.
if (HERE/'inspection-source-v1.png').exists():
    import subprocess,sys
    subprocess.run([sys.executable,str(HERE/'build_inspection.py')],check=True)
