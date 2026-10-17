"""Carrying upper body plus six phase samples from accepted full east walk."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,label,binary_dilation
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
arr=np.array(upper);arr[102:]=0
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
    leg=np.array(Image.open(walkroot/walk['frameFiles'][phase]).convert('RGBA'));leg[:102]=0
    out=Image.fromarray(leg);out.alpha_composite(upper)
    # Fixed crate/face; accepted pelvis retained from belt to knees; no generated legs are selected.
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(out,(36,52));bare.append(canvas)
# Transfer only the repaired pelvis; preserve the accepted legs and carrying grip.
repair=Image.open(HERE/'hip-repair-source-v5.png').convert('RGBA')
cells=[repair.crop((round(i*repair.width/6),0,round((i+1)*repair.width/6),repair.height)) for i in range(6)]
ca=np.array(cells[0]);sy,sx=np.where(ca[:,:,3]>200);hip_scale=148/(sy.max()-sy.min()+1)
mask_image=Image.new('L',(256,256));ImageDraw.Draw(mask_image).polygon([(111,126),(126,126),(133,140),(136,149),(144,159),(155,170),(160,180),(157,185),(108,185),(104,167),(108,151)],fill=255)
hipmask=np.array(mask_image)>0;layers=[];offsets=[]
for cell,frame in zip(cells,bare):
    src=np.array(cell);r=src[:,:,:3].astype(int)
    warm=(src[:,:,3]>200)&(r[:,:,0]-r[:,:,1]>8)&(r[:,:,0]-r[:,:,2]>15)
    warm[sy.min()+round(30/hip_scale):]=False
    yy,xx=np.where(warm)
    ref=np.array(frame);r=ref[:,:,:3].astype(int)
    rw=(ref[:,:,3]>200)&(r[:,:,0]-r[:,:,1]>8)&(r[:,:,0]-r[:,:,2]>15);rw[:76]=False;rw[103:]=False
    ry,rx=np.where(rw)
    offset=(round((rx.min()+rx.max())/2-(xx.min()+xx.max())/2*hip_scale),round(ry.min()-yy.min()*hip_scale))
    layer=Image.new('RGBA',(256,256));layer.alpha_composite(cell.resize((round(cell.width*hip_scale),round(cell.height*hip_scale)),Image.Resampling.LANCZOS),offset)
    layers.append(np.array(layer));offsets.append(offset)
# Match repair cloth to the actual carrying torso above the join, with one
# shared curve for every pose. Hip-only histograms created a tonal step at the belt.
samples=[];refs=[]
for frame,layer in zip(bare,layers):
    for data,destination in [(layer,samples),(np.array(frame),refs)]:
        region=data[121:146,113:128];r=region[:,:,:3].astype(float)
        m=(region[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
        destination.extend(r[m])
knots=np.percentile(np.array(samples).mean(1),[0,15,35,55,75,90,100]);target=np.percentile(refs,[0,15,35,55,75,90,100],axis=0)
for i,layer in enumerate(layers):
    r=layer[:,:,:3].astype(float);m=hipmask&(layer[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125)
    for c in range(3):layer[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
    # Broad smooth transition through continuous side cloth, not a short horizontal cut.
    weight=hipmask.astype(float)
    for y in range(126,146):
        t=(y-126)/19;weight[y]*=t*t*(3-2*t)
    for y,w in [(182,.85),(183,.65),(184,.35),(185,.1)]:weight[y]*=w
    before=np.array(bare[i]);out=np.rint(before*(1-weight[:,:,None])+layer*weight[:,:,None]).astype('uint8')
    assert np.array_equal(out[~hipmask],before[~hipmask])
    # Tiny detached remnants of the old lowered glove beside the rear hip.
    components,count=label(out[:,:,3]>20)
    for component in range(1,count+1):
        ys,xs=np.where(components==component)
        if len(ys)<30 and xs.min()>=96 and xs.max()<112 and ys.min()>=154 and ys.max()<188:
            out[binary_dilation(components==component,iterations=2)]=0
    bare[i]=Image.fromarray(out)
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
        assert np.array_equal(np.array(frame)[:126],np.array(frames[0])[:126])
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame);rgb.append(bg)
        contact.alpha_composite(frame,(i*256,row*280+24));d.text((i*256+4,row*280+4),f'{variant} / walk phase {phases[i]}',fill='white')
    manifest=dict(original['profile']);manifest.update(name='Veld consistent east carrying '+variant,textureFilter='linear',status='staged_not_installed')
    manifest['strideDistanceCells']={'carry-east':original['profile']['strideDistanceCells']['carry-east']}
    state=dict(original['state']);state.update(frameFiles=paths,frameCount=6);manifest['states']=[state]
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    pal=Image.new('RGB',(1536,256))
    for i,im in enumerate(rgb):pal.paste(im,(256*i,0))
    palette=pal.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb]
    name=f'{variant}-carry-east-seamless-waist-v7.gif';gif[0].save(HERE/name,save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    with Image.open(HERE/name) as decoded:
        first=None
        for i,frame in enumerate(frames):
            decoded.seek(i);pix=np.array(decoded.convert('RGB')).astype(int)
            if first is None:first=pix.copy()
            assert np.array_equal(pix[:126],first[:126])
            a=np.array(frame)[:,:,3];outside=(a==0)&(distance_transform_edt(a<200)>2);assert np.abs(pix[outside]-[32,42,48]).max()<=3
contact.save(HERE/'contact.png')
(HERE/'checks.json').write_text(json.dumps({'source':'carry-source-v1.png','source_sha256':hashlib.sha256((HERE/'carry-source-v1.png').read_bytes()).hexdigest(),'generated_gait_rejected':'carry-gait-source-v2.png; repeated similar lead-leg poses','accepted_walk_phases':phases,'walk_frame_count':len(walk['frameFiles']),'fixed_upper_body_and_crate':True,'no_generated_legs_selected':True,'decoded_gif_frames_checked':12,'original_timing_and_cargo_metadata':True,'pivot':[128,224],'standingHeight':148,'scale':scale,'status':'staged_for_visual_review'},indent=2)+'\n')
checks=json.loads((HERE/'checks.json').read_text());checks.update(revision='seamless-waist-v7',hip_source='hip-repair-source-v5.png',hip_source_sha256=hashlib.sha256((HERE/'hip-repair-source-v5.png').read_bytes()).hexdigest(),hip_scale=hip_scale,hip_offsets=offsets,hip_mask_bounds=[104,126,161,186],outside_hip_patch_preserved_except_detached_glove_remnants=True)
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east carrying</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld — east cargo carrying</h1><p>Waist texture and colour matched across the belt with a broad continuous blend; steady crate grip. Shared subdued helmet. Staged for review.</p>'
for variant in ['bare','helmet']:
    html+=f'<h2>{variant}</h2>'
    for h in [256,142,93,47]:html+=f'<img src="{variant}-carry-east-seamless-waist-v7.gif" height="{h}">'
html+='<p><a href="contact.png">All phases</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('12 carrying references packaged; accepted walk phases, fixed upper body/crate, original metadata, exterior and clipping checks pass.')
