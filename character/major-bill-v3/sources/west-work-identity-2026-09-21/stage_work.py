from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,sys
sys.path.insert(0,'tools')
from rebuild_bill_art import HelmetRebaker,tilted
p=Path('character/major-bill-v3/sources/west-work-identity-2026-09-21');out=Path('output/bill-west-work-identity-2026-09-21')
a=np.array(Image.open(p/'work-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;raw=Image.fromarray(a)
cells=[raw.crop(((i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512)) for i in range(6)];boxes=[x.getbbox() for x in cells];scale=110/(boxes[0][3]-boxes[0][1]);rows=[]
polygon=[(99,145),(128,145),(130,156),(147,156),(153,159),(169,158),(172,173),(160,180),(139,179),(121,171),(99,170)]
mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon(polygon,fill=255)
base=Image.open(p/'lowering-005.png').convert('RGBA')
for i,(cell,box) in enumerate(zip(cells,boxes)):
 crop=cell.crop(box);a=np.array(crop);head_x=np.where(a[:70,:,3]>0)[1];anchor=(head_x.min()+head_x.max())/2
 size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.LANCZOS);a=np.array(crop);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;crop=Image.fromarray(a)
 paste=(round(149-anchor*scale),113);registered=Image.new('RGBA',(256,256));registered.alpha_composite(crop,paste)
 frame=base.copy()
 if i not in (0,5):frame.paste(registered,(0,0),mask)
 frame.save(p/f'work-{i:03}.png');rows.append({'cell':[(i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512],'box':box,'size':size,'paste':paste})
(p/'work-registration.json').write_text(json.dumps({'source_sha256':hashlib.sha256((p/'work-source.png').read_bytes()).hexdigest(),'scale':scale,'alpha_threshold':128,'filter':'LANCZOS; binary alpha128 before and after','frames':rows,'replacement_polygon':polygon},indent=2))
kneel=[Image.open(p/f'lowering-{i:03}.png').convert('RGBA') for i in range(6)];heads=[]
for frame in kneel:
 a=np.array(frame);top=frame.getbbox()[1];xs=np.where(a[top:top+18,:,3]>0)[1];heads.append([round((xs.min()+xs.max())/2),top+18])
fit={'overlay_size':[48,56],'overlay_anchor_offset':[23,25],'normal_shell_cap':48,'head_anchors':[{'folder':folder,'frame':i,'head':heads[i] if folder=='lowering' else heads[-1]} for folder in ['lowering','repair'] for i in range(6)]};(p/'helmet-registration.json').write_text(json.dumps(fit,indent=2))
for variant in ['bare','helmet']:
 poses={'kneel':kneel.copy(),'repair':[Image.open(p/f'work-{i:03}.png').convert('RGBA') for i in range(6)]}
 if variant=='helmet':
  overlay=HelmetRebaker(None,max_height=48).overlay('west')
  for key,frames in poses.items():
   for i,frame in enumerate(frames):
    head=np.array(heads[i] if key=='kneel' else heads[-1]);frames[i]=tilted(frame,overlay,head-[23,25],0,[*(head-[14,20]),28,34],'west')
 idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(Path('character/major-bill-v3/frames')/variant/'idle-west/000.png').convert('RGBA'),(36,52));poses['kneel'][0]=idle;poses['stand']=list(reversed(poses['kneel']))
 for key,frames in poses.items():
  folder=out/'candidate'/variant/(key+'-west');folder.mkdir(parents=True,exist_ok=True)
  for i,frame in enumerate(frames):frame.save(folder/f'{i:03}.png')
b=Image.new('RGB',(1056,420),(23,33,41))
for row,key in enumerate(['kneel','repair']):
 for i in range(6):
  f=Image.open(out/f'candidate/bare/{key}-west/{i:03}.png').crop((40,54,216,236));b.paste(f,(i*176,row*210),f);ImageDraw.Draw(b).text((i*176+8,row*210+188),key+str(i),fill='white')
b.save(out/'candidate-review.png')
