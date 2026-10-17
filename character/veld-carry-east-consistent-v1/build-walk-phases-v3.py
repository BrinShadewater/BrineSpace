"""Carrying upper body plus six phase samples from accepted full east walk."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
original=json.loads((HERE/'original-selection.json').read_text())
source=Image.open(HERE/'carry-source-v1.png').convert('RGBA')
cell=source.crop((0,0,round(source.width/6),source.height))
a=np.array(cell);ys,xs=np.where(a[:,:,3]>200)
scale=148/(ys.max()-ys.min()+1)
crop=cell.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
crop=crop.resize((round(crop.width*scale),148),Image.Resampling.LANCZOS)
# Shoulder center follows accepted near arm; crop x includes the trailing boot.
upper=Image.new('RGBA',(184,184));upper.alpha_composite(crop,(54,24))
arr=np.array(upper);arr[113:]=0
# One neutral cloth calibration for the frozen upper body.
idle=Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA')
ref=np.array(idle)[56:110,83:116,:3].reshape(-1,3).astype(float)
ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
r=arr[:,:,:3].astype(float);material=(arr[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
knots=np.percentile(r[material].mean(1),[0,15,35,55,75,90,100]);target=np.percentile(ref,[0,15,35,55,75,90,100],axis=0)
for c in range(3):arr[material,c]=np.interp(r[material].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
upper=Image.fromarray(arr)
walkroot=ROOT/'character/crew-runtime-matte-v1/veld'
walk=next(s for s in json.loads((walkroot/'manifest.json').read_text())['states'] if s['id']=='walk-east')
phases=[round(i*len(walk['frameFiles'])/6)%len(walk['frameFiles']) for i in range(6)]
bare=[]
for phase in phases:
    leg=np.array(Image.open(walkroot/walk['frameFiles'][phase]).convert('RGBA'));leg[:113]=0
    out=Image.fromarray(leg);out.alpha_composite(upper)
    # Fixed crate/face and two-row waist overlap; no generated legs are selected.
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(out,(36,52));bare.append(canvas)
helmet=[]
head=Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((79,14,121,59))
for frame in bare:
    a=np.array(frame);a[66:102,114:158]=0
    out=Image.fromarray(a);out.alpha_composite(head,(115,66));helmet.append(out)
contact=Image.new('RGBA',(256*6,280*2),'#202a30');d=ImageDraw.Draw(contact)
for row,(variant,frames) in enumerate([('bare',bare),('helmet',helmet)]):
    paths=[];rgb=[]
    for i,frame in enumerate(frames):
        path=f'frames/{variant}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);frame.save(HERE/path);paths.append(path)
        a=np.array(frame);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
        assert np.array_equal(np.array(frame)[:165],np.array(frames[0])[:165])
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame);rgb.append(bg)
        contact.alpha_composite(frame,(i*256,row*280+24));d.text((i*256+4,row*280+4),f'{variant} / walk phase {phases[i]}',fill='white')
    manifest=dict(original['profile']);manifest.update(name='Veld consistent east carrying '+variant,textureFilter='linear',status='staged_not_installed')
    manifest['strideDistanceCells']={'carry-east':original['profile']['strideDistanceCells']['carry-east']}
    state=dict(original['state']);state.update(frameFiles=paths,frameCount=6);manifest['states']=[state]
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    pal=Image.new('RGB',(1536,256))
    for i,im in enumerate(rgb):pal.paste(im,(256*i,0))
    palette=pal.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb]
    name=f'{variant}-carry-east-walk-phases-v3.gif';gif[0].save(HERE/name,save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    with Image.open(HERE/name) as decoded:
        first=None
        for i,frame in enumerate(frames):
            decoded.seek(i);pix=np.array(decoded.convert('RGB')).astype(int)
            if first is None:first=pix.copy()
            assert np.array_equal(pix[:165],first[:165])
            a=np.array(frame)[:,:,3];outside=(a==0)&(distance_transform_edt(a<200)>2);assert np.abs(pix[outside]-[32,42,48]).max()<=3
contact.save(HERE/'contact.png')
(HERE/'checks.json').write_text(json.dumps({'source':'carry-source-v1.png','source_sha256':hashlib.sha256((HERE/'carry-source-v1.png').read_bytes()).hexdigest(),'generated_gait_rejected':'carry-gait-source-v2.png; repeated similar lead-leg poses','accepted_walk_phases':phases,'walk_frame_count':len(walk['frameFiles']),'fixed_upper_body_and_crate':True,'no_generated_legs_selected':True,'decoded_gif_frames_checked':12,'original_timing_and_cargo_metadata':True,'pivot':[128,224],'standingHeight':148,'scale':scale,'status':'staged_for_visual_review'},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east carrying</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld — east cargo carrying</h1><p>Matched carrying body and steady crate grip; legs sampled from the accepted full walk cycle. Shared subdued helmet. Staged for review.</p>'
for variant in ['bare','helmet']:
    html+=f'<h2>{variant}</h2>'
    for h in [256,142,93,47]:html+=f'<img src="{variant}-carry-east-walk-phases-v3.gif" height="{h}">'
html+='<p><a href="contact.png">All phases</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('12 carrying references packaged; accepted walk phases, fixed upper body/crate, original metadata, exterior and clipping checks pass.')
