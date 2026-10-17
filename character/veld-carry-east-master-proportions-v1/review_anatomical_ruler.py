"""Compare independent poses by crown-to-cylinder-bottom anatomy, never pose height."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
# Landmarks manually reviewed on raw source pixels. Hip-mounted cylinder bottom
# is stable upper-body anatomy; knee/boot positions deliberately excluded.
specs=[
 ('Held master',R/'character/veld-cargo-turns-master-family-v1/corrected-east-held-density-reference.png',None,311),
 ('Near contact V1:0',P/'raw-v1.png',0,327),
 ('Near support V1:1',P/'raw-v1.png',1,327),
 ('Far swing V10',P/'raw-far-swing-v10.png',None,766),
 ('Opposite contact V5',P/'raw-opposite-contact-v5.png',None,775),
 ('Far support V8',P/'raw-passing-v8.png',None,690),
 ('Near swing V9',P/'raw-swing-v9.png',None,658),
 ('Opposite V13 pouch',P/'raw-opposite-contact-v13.png',None,827),
 ('Opposite V14 clean',P/'raw-opposite-contact-v14.png',None,768),
]
board=Image.new('RGB',(len(specs)*256,830),'#202a30');draw=ImageDraw.Draw(board)
draw.text((8,8),'ANATOMICAL RULER STUDY: same crown-to-cylinder span; physical opaque boot floor 224; original grade.',fill='white')
rows=[];target=None;frames=[]
for i,(name,path,index,hip_y) in enumerate(specs):
 im=Image.open(path).convert('RGBA');a=np.array(im)
 ids,_=label(a[:,:,3]>200);sizes=np.bincount(ids.ravel());sizes[0]=0
 components=[]
 for n,sl in enumerate(find_objects(ids),1):
  if sl and sizes[n]>3000:
   y,x=sl;components.append((x.start,n,sl))
 components.sort()
 n,sl=(max(components,key=lambda c:sizes[c[1]])[1:] if index is None else components[index][1:])
 y,x=sl;crown=y.start;floor=y.stop-1
 if target is None: target=(hip_y-crown)*148/(y.stop-y.start)
 scale=target/(hip_y-crown)
 keep=binary_dilation(ids==n,iterations=2);a[~keep]=0
 bounds=(max(0,x.start-2),max(0,y.start-2),min(im.width,x.stop+2),min(im.height,y.stop+2))
 crop=Image.fromarray(a).crop(bounds)
 # Horizontal center uses suit/hip cross-section beneath the fixed cylinders.
 row=min(hip_y+15,im.height-1);_,px=np.where(a[row-2:row+3,:,3]>200)
 center=(px.min()+px.max())/2
 resized=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(256,256));offset=(round(128-(center-bounds[0])*scale),round(224-(floor-bounds[1])*scale))
 frame.alpha_composite(resized,offset)
 frames.append(frame)
 fy=224-(floor-crown)*scale;hy=224-(floor-hip_y)*scale
 draw.text((i*256+5,32),name,fill='white');draw.text((i*256+5,49),f'crown {fy:.1f} hip {hy:.1f}',fill='#cbd5db')
 board.paste(frame,(i*256,40),frame)
 for yy in [fy,hy,224]: draw.line((i*256+7,40+yy,i*256+249,40+yy),fill='#406272')
 upper=frame.crop((55,64,215,164)).resize((256,160),Image.Resampling.NEAREST)
 board.paste(upper,(i*256,320),upper)
 lower=frame.crop((45,155,225,233)).resize((256,111),Image.Resampling.NEAREST)
 board.paste(lower,(i*256,500),lower)
 # Raw landmark plate validates measurement independently of the scaled frames.
 raw=crop.copy();rd=ImageDraw.Draw(raw)
 for yy in [crown,hip_y,floor]:rd.line((0,yy-bounds[1],crop.width,yy-bounds[1]),fill='#ff7040',width=max(1,round(crop.height/400)))
 raw.thumbnail((220,185),Image.Resampling.LANCZOS);board.paste(raw,(i*256+18,634),raw)
 rows.append({'label':name,'source':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'componentIndex':index,'box':[x.start,y.start,x.stop,y.stop],'crownY':crown,'cylinderBottomY':hip_y,'opaqueFootFloor':floor,'scale':scale,'registeredCrown':fy,'registeredCylinderBottom':hy,'position':offset})
out=P/'anatomical-ruler-v1';out.mkdir(exist_ok=True)
board.save(out/'comparison.png')
for i,frame in enumerate(frames[1:7]):frame.save(out/f'phase-{i:03}.png')
preview=[]
for frame in frames[1:7]:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(frame);preview.append(bg)
preview[0].save(out/'diagnostic-cycle.png',save_all=True,append_images=preview[1:],duration=140,loop=0,disposal=0,blend=0)
replacement=frames[1:7];replacement[3]=frames[-1]
replacement_preview=[]
for frame in replacement:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(frame);replacement_preview.append(bg)
replacement_preview[0].save(out/'diagnostic-cycle-v14.png',save_all=True,append_images=replacement_preview[1:],duration=140,loop=0,disposal=0,blend=0)
(out/'registration.json').write_text(json.dumps({'scope':'Diagnostic rigid body registration study, not a gait export. Manual anatomical landmarks require visual verification. No recolor/anatomy edits.','targetCrownToCylinderSpan':target,'rows':rows},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'targetSpan':target,'crownRange':[min(r['registeredCrown'] for r in rows),max(r['registeredCrown'] for r in rows)],'rows':[{k:r[k] for k in ('label','scale','registeredCrown','registeredCylinderBottom')} for r in rows]}))
