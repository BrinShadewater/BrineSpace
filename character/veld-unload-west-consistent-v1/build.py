"""Matched west unloading candidate; preserved full-body source and exact idle exit."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
profile=json.loads((ROOT/'character/veld-carry-west-consistent-v1/original-selection.json').read_text())['profile']
original=json.loads((HERE/'original-state.json').read_text());source=Image.open(HERE/'source-v1.png').convert('RGBA')
cells=[source.crop((round(i*source.width/6),0,round((i+1)*source.width/6),source.height)) for i in range(6)]
a=np.array(cells[0]);yy,xx=np.where(a[:,:,3]>200);scale=148/(yy.max()-yy.min()+1)
boot_centers=[195,215,225,237,210,225];bare=[];landmarks=[];offsets=[]
for cell,center,floor in zip(cells,boot_centers,[677,672,672,672,672,678]):
 offset=(round(128-center*scale),round(224-floor*scale));offsets.append(offset)
 out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),offset);bare.append(out)
# Shared fixed material curve to the newly accepted carry. Preserve warm skin/hair.
refs=[];samples=[]
for i,frame in enumerate(bare):
 for im,dest in [(np.array(frame),samples),(np.array(Image.open(ROOT/f'character/veld-carry-west-consistent-v1/frames/bare/{i:03}.png').convert('RGBA')),refs)]:
  r=im[:,:,:3].astype(float);m=(im[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);m[:75]=False;m[90:,:110]=False;dest.extend(r[m])
knots=np.percentile(np.array(samples).mean(1),[0,15,35,55,75,90,100]);target=np.percentile(refs,[0,15,35,55,75,90,100],axis=0)
head=Image.open(ROOT/'character/veld-shared-helmet-v1/frames/idle-west/000.png').convert('RGBA').crop((64,14,108,60));helmet=[]
for i,frame in enumerate(bare):
 a=np.array(frame);r=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(r,axis=2)<24)&(r.mean(2)>15)&(r.mean(2)<125);m[:75]=False;m[90:,:110]=False
 for c in range(3):a[m,c]=np.interp(r[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
 bare[i]=Image.fromarray(a.copy())
 warm=(a[:,:,3]>200)&(r[:,:,0]-r[:,:,1]>8)&(r[:,:,0]-r[:,:,2]>15);warm[205:]=False
 yy,xx=np.where(warm);top=int(yy.min());center=round((xx.min()+xx.max())/2)-3;landmarks.append([center,top])
 a[top:top+24,xx.min()-2:xx.max()+3]=0
 out=Image.fromarray(a);fitted=head.rotate([0,12,18,16,8,0][i],resample=Image.Resampling.BICUBIC,expand=True);out.alpha_composite(fitted,(round(center+2-fitted.width/2),round(top+13-fitted.height/2)));helmet.append(out)
# Lock the deposited object for floor-contact/release/idle poses.
case=bare[5].crop((72,197,106,225))
for frames in [bare,helmet]:
 for i in [3,4,5]:
  a=np.array(frames[i]);a[197:225,68:110]=0
  out=Image.fromarray(a);out.alpha_composite(case,(72,197));frames[i]=out
# Exact standing identity/stance at exit; deposited case stays in front of her.
for frames,path,position in [(bare,'character/crew-runtime-matte-v1/veld/frames/idle-west-transition-matte-v1/000.png',(36,52)),(helmet,'character/veld-shared-helmet-v1/frames/idle-west/000.png',(36,52))]:
 out=Image.new('RGBA',(256,256));out.alpha_composite(case,(72,197));out.alpha_composite(Image.open(ROOT/path).convert('RGBA'),position);frames[5]=out
contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact)
for row,(variant,frames) in enumerate([('bare',bare),('helmet',helmet)]):
 paths=[];rgb=[]
 for i,frame in enumerate(frames):
  path=f'frames/{variant}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);frame.save(HERE/path);paths.append(path)
  a=np.array(frame);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20)
  bg=Image.new('RGB',(256,256),'#202a30');bg.paste(frame,mask=frame);rgb.append(bg);contact.alpha_composite(frame,(i*256,row*280+24));draw.text((i*256+4,row*280+4),f'{variant} / unload {i}',fill='white')
 manifest=dict(profile);manifest.update(name='Veld master matched west unloading '+variant,status='owner_accepted_installed',textureFilter='linear',strideDistanceCells={})
 state=dict(original);state.update(frameFiles=paths,frameCount=6);manifest['states']=[state];(HERE/f'{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 pal=Image.new('RGB',(1536,256))
 for i,im in enumerate(rgb):pal.paste(im,(i*256,0))
 palette=pal.quantize(colors=256);gif=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in rgb]
 # Review playback pauses on the exact idle exit before restarting the action.
 gif[0].save(HERE/f'{variant}-unload-west-master-v1.gif',save_all=True,append_images=gif[1:],duration=[140,180,200,200,180,700],loop=0,disposal=2,optimize=False)
contact.save(HERE/'contact.png')
checks={'source':'source-v1.png','sha256':hashlib.sha256((HERE/'source-v1.png').read_bytes()).hexdigest(),'scale':scale,'offsets':offsets,'helmet_landmarks':landmarks,'original_nonloop_timing':True,'exact_idle_body_exit':True,'deposited_case_locked_frames':[3,4,5],'staged':False,'owner_accepted_installed':True,'cloth_midtones_lift':0}
(HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld west unloading</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld - west cargo unloading</h1><p>West unloading from the high-resolution master: bend, floor contact, release and exact accepted idle exit. Owner accepted; installed; review playback slowed, runtime remains520ms.</p>'
for v in ['bare','helmet']:
 html+=f'<h2>{v}</h2>'
 for height in [256,142,93,47]:html+=f'<img src="{v}-unload-west-master-v1.gif" height="{height}">'
html+='<p><a href="contact.png">All poses</a></p>'; (HERE/'index.html').write_text(html,encoding='utf-8')
print('12 west unload references packaged; original520ms non-loop timing, clipping and idle exit preserved.')
