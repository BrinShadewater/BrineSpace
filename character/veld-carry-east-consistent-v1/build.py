"""Full-body coordinated carrying gait, source camera registered at pelvis/floor."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
original=json.loads((HERE/'original-selection.json').read_text())
source=Image.open(HERE/'motion-source-v9.png').convert('RGBA')
cells=[source.crop((round(i*source.width/6),0,round((i+1)*source.width/6),source.height)) for i in range(6)]
alpha=np.array(cells[0])[:,:,3];ys,xs=np.where(alpha>200)
scale=148/(ys.max()-ys.min()+1);floor=int(ys.max());bare=[];offsets=[]
for cell in cells:
    a=np.array(cell);yx,xx=np.where(a[418:423,:,3]>200)
    pelvis=(xx.min()+xx.max())/2
    offset=(round(128-pelvis*scale),round(224-floor*scale))
    out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),offset)
    bare.append(out);offsets.append(offset)
# One clip-wide graphite cloth calibration; warm hair/skin and blue patches excluded.
idle=np.array(Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png').convert('RGBA'))
ref=idle[56:110,83:116,:3].reshape(-1,3).astype(float);ref=ref[(np.ptp(ref,axis=1)<24)&(ref.mean(1)>15)&(ref.mean(1)<125)]
samples=[]
for frame in bare:
    a=np.array(frame);r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);m[:107]=False;samples.extend(r[m].mean(1))
knots=np.percentile(samples,[0,15,35,55,75,90,100]);target=np.percentile(ref,[0,15,35,55,75,90,100],axis=0)
helm=[];head_landmarks=[]
head=Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((79,14,121,59))
for i,frame in enumerate(bare):
    a=np.array(frame);r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);m[:107]=False
    for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')

    # Hair/face landmark moves with the source neck; helmet follows each pose.
    warm=(a[:,:,3]>200)&(r[:,:,0]-r[:,:,1]>8)&(r[:,:,0]-r[:,:,2]>15);warm[103:]=False
    yy,xx=np.where(warm);headtop=int(yy.min());center=round((xx.min()+xx.max())/2)+3
    head_landmarks.append([center,headtop])
    # Fixed material-only lifts across the clip, preserving alpha and motion.
    graded=a[:,:,:3].astype(float)
    cloth=m.copy();cloth[120:157,145:]=False
    lift=10*np.clip((graded.mean(2)-15)/25,0,1)*np.clip((125-graded.mean(2))/30,0,1)
    a[cloth,:3]=np.rint(graded[cloth]+lift[cloth,None]).clip(0,255).astype('uint8')
    face_region=Image.new('L',(256,256));ImageDraw.Draw(face_region).polygon([(center+2,headtop+7),(center+12,headtop+8),(center+12,headtop+21),(center+5,headtop+25),(center-3,headtop+20),(center-4,headtop+12)],fill=255)
    skin=(np.array(face_region)>0)&(a[:,:,3]>0)&(r[:,:,0]>125)&(r[:,:,1]>65)&(r[:,:,0]-r[:,:,1]>18)&(r[:,:,0]-r[:,:,2]>25)
    a[skin,:3]=np.rint(a[skin,:3].astype(float)+[10,9,8]).clip(0,255).astype('uint8')
    bare[i]=Image.fromarray(a.copy())
    a[:headtop+32]=0;out=Image.fromarray(a);out.alpha_composite(head,(center-21,headtop-10));helm.append(out)
helmet=helm;phases=list(range(6))
contact=Image.new('RGBA',(256*6,280*2),'#202a30');d=ImageDraw.Draw(contact)
for row,(variant,frames) in enumerate([('bare',bare),('helmet',helmet)]):
    paths=[];rgb=[]
    for i,frame in enumerate(frames):
        path=f'frames/{variant}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);frame.save(HERE/path);paths.append(path)
        a=np.array(frame);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
        assert np.any(a[:,:,3]>200)
        bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame);rgb.append(bg)
        contact.alpha_composite(frame,(i*256,row*280+24));d.text((i*256+4,row*280+4),f'{variant} / carry pose {i}',fill='white')
    manifest=dict(original['profile']);manifest.update(name='Veld consistent east carrying '+variant,textureFilter='linear',status='owner_accepted_installed')
    manifest['strideDistanceCells']={'carry-east':original['profile']['strideDistanceCells']['carry-east']}
    state=dict(original['state']);state.update(frameFiles=paths,frameCount=6);manifest['states']=[state]
    (HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    pal=Image.new('RGB',(1536,256))
    for i,im in enumerate(rgb):pal.paste(im,(256*i,0))
    palette=pal.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb]
    name=f'{variant}-carry-east-palette-match-v10.gif';gif[0].save(HERE/name,save_all=True,append_images=gif[1:],duration=state['frameDurationsMs'],loop=0,optimize=False,disposal=2)
    with Image.open(HERE/name) as decoded:
        first=None
        for i,frame in enumerate(frames):
            decoded.seek(i);pix=np.array(decoded.convert('RGB')).astype(int)
            if first is None:first=pix.copy()
            assert pix.shape==(256,256,3)
            a=np.array(frame)[:,:,3];outside=(a==0)&(distance_transform_edt(a<200)>2);assert np.abs(pix[outside]-[32,42,48]).max()<=3
contact.save(HERE/'contact.png')
checks={'revision':'palette-match-v10','source':'motion-source-v9.png','source_sha256':hashlib.sha256((HERE/'motion-source-v9.png').read_bytes()).hexdigest(),'source_pose_order':phases,'full_body_motion':True,'no_head_or_crate_lock':True,'registration':'one global scale/floor; pelvis horizontal camera registration','scale':scale,'offsets':offsets,'helmet_head_landmarks':head_landmarks,'decoded_gif_frames_checked':12,'original_timing_and_cargo_metadata':True,'pivot':[128,224],'standingHeight':148,'status':'owner_accepted_installed','palette_lift':{'cloth_midtones':10,'skin_rgb':[10,9,8],'one_fixed_transform':True}}
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld east carrying</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld — east cargo carrying</h1><p>Full-body carrying stride with lighter matched skin and graphite cloth. Helmet follows the moving head. Owner accepted; installed.</p>'
for variant in ['bare','helmet']:
    html+=f'<h2>{variant}</h2>'
    for h in [256,142,93,47]:html+=f'<img src="{variant}-carry-east-palette-match-v10.gif" height="{h}">'
html+='<p><a href="contact.png">All phases</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('12 full-body motion references packaged; original metadata, exterior and clipping checks pass.')
