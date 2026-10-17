"""Package authored stationary turn with adjacent planted boots throughout."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
original=json.loads((HERE/'original-states.json').read_text())
source=Image.open(HERE/'source-v1.png').convert('RGBA');cells=[]
for row in range(2):
 cells.append([source.crop((round(i*source.width/6),round(row*source.height/2),round((i+1)*source.width/6),round((row+1)*source.height/2))) for i in range(6)])
alpha=np.array(cells[0][0])[:,:,3];yy,xx=np.where(alpha>200);scale=148/(yy.max()-yy.min()+1)
offsets=[];frames={}
for row,v in enumerate(['bare','helmet']):
 local=[]
 for cell in cells[row]:
  a=np.array(cell);y,x=np.where(a[:,:,3]>200);floor=y.max();boots=(a[:,:,3]>200)&(np.indices(a.shape[:2])[0]>floor-30);by,bx=np.where(boots)
  center=(bx.min()+bx.max())/2;offset=(round(128-center*scale),round(224-floor*scale));out=Image.new('RGBA',(256,256));out.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),offset);local.append(out);offsets.append(offset)
 # A single material transform pooled across the clip, never a per-frame grade.
 samples=[];refs=[]
 for f in local:
  a=np.array(f);rgb=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>18)&(rgb.mean(2)<130);m[:110]=False;samples.extend(rgb[m].mean(1))
 for direction in ['north','west']:
  f=Image.open(ROOT/f'character/veld-carry-{direction}-consistent-v1/frames/{v}/000.png').convert('RGBA');a=np.array(f);rgb=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>18)&(rgb.mean(2)<130);m[:110]=False;refs.extend(rgb[m])
 knots=np.percentile(samples,[0,15,35,55,75,90,100]);target=np.percentile(refs,[0,15,35,55,75,90,100],axis=0)
 for i,f in enumerate(local):
  a=np.array(f);rgb=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>18)&(rgb.mean(2)<130);m[:110]=False
  for c in range(3):a[m,c]=np.interp(rgb[m].mean(1),knots,target[:,c]).clip(0,255).astype('uint8')
  local[i]=Image.fromarray(a)
 # Owner requested stationary feet together, including authored endpoints.
 # Do not replace these with split-stride locomotion frames.
 frames[v]=local
contact=Image.new('RGBA',(1536,1120),'#202a30');draw=ImageDraw.Draw(contact)
for vi,v in enumerate(['bare','helmet']):
 profile=json.loads((ROOT/f'character/veld-carry-north-consistent-v1/{v}-manifest.json').read_text());profile.update(name='Veld north/west cargo turns '+v,status='staged_not_installed',strideDistanceCells={});states=[]
 for si,direction in enumerate(['north-west','west-north']):
  state=dict(original[si]);sequence=frames[v] if si==0 else frames[v][::-1];paths=[];rgb=[]
  for i,f in enumerate(sequence):
   path=f'frames/{v}/carry-turn-{direction}/{i:03}.png';(HERE/path).parent.mkdir(parents=True,exist_ok=True);f.save(HERE/path);paths.append(path);contact.alpha_composite(f,(i*256,(vi*2+si)*280+24));draw.text((i*256+4,(vi*2+si)*280+4),f'{v} / {direction} / {i}',fill='white');bg=Image.new('RGB',(256,256),'#202a30');bg.paste(f,mask=f);rgb.append(bg)
  state.update(frameFiles=paths,frameCount=6);states.append(state);pal=Image.new('RGB',(1536,256))
  for i,f in enumerate(rgb):pal.paste(f,(i*256,0))
  palette=pal.quantize(colors=256);gif=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in rgb];gif[0].save(HERE/f'{v}-{direction}-v1.gif',save_all=True,append_images=gif[1:],duration=[450,180,210,240,240,650],loop=0,disposal=2,optimize=False)
 profile['states']=states;(HERE/f'{v}-manifest.json').write_text(json.dumps(profile,indent=2)+'\n')
contact.save(HERE/'contact.png');(HERE/'checks.json').write_text(json.dumps({'source_sha256':hashlib.sha256((HERE/'source-v1.png').read_bytes()).hexdigest(),'scale':scale,'offsets':offsets,'exact_carry_frame_zero_endpoints':False,'stationary_authored_endpoints':True,'feet_together':True,'reverse_derived':True,'fixed_clip_material_grade':True,'staged':True,'owner_accepted_installed':False},indent=2)+'\n')
html='<meta charset="utf-8"><title>Veld north/west cargo turns</title><style>body{background:#202a30;color:#e1e7eb;font:16px sans-serif;margin:28px}img{margin:12px}a{color:#8cc6e7}</style><h1>Veld - north/west cargo turns</h1><p>Stationary turn with feet together and planted throughout, including the endpoints. Both directions, bare and helmet. Staged for review; preview slowed, runtime remains800ms.</p>'
for v in ['bare','helmet']:
 for direction in ['north-west','west-north']:
  html+=f'<h2>{v} / {direction}</h2>'
  for h in [256,142,93,47]:html+=f'<img src="{v}-{direction}-v1.gif" height="{h}">'
html+='<p><a href="contact.png">All poses</a></p>'; (HERE/'index.html').write_text(html)
print('24 stationary cargo turn frames packaged; original800ms nonloop metadata.')
