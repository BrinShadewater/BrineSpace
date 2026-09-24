from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,sys
sys.path.insert(0,'tools')
from rebuild_bill_art import HelmetRebaker,tilted
p=Path('character/major-bill-v3/sources/north-work-identity-2026-09-21');out=Path('output/bill-north-work-identity-2026-09-21');out.mkdir(exist_ok=True)
a=np.array(Image.open(p/'work-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;raw=Image.fromarray(a)
cells=[raw.crop(((i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512)) for i in range(6)]
boxes=[cell.getbbox() for cell in cells];scale=109/(boxes[0][3]-boxes[0][1]);rows=[]
base=Image.open(p/'lowering-005.png').convert('RGBA');rects=[(81,145,108,184),(148,145,175,184)]
for i,(cell,box) in enumerate(zip(cells,boxes)):
 crop=cell.crop(box);a=np.array(crop);head_x=np.where(a[:45,:,3]>0)[1];anchor=(int(head_x.min())+int(head_x.max()))/2
 size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.LANCZOS);a=np.array(crop);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;crop=Image.fromarray(a)
 paste=(round(128-anchor*scale),115);registered=Image.new('RGBA',(256,256));registered.alpha_composite(crop,paste)
 frame=base.copy()
 if i not in (0,5):
  for rect in rects:frame.paste(registered.crop(rect),rect)
 frame.save(p/f'work-{i:03}.png');rows.append({'cell':[(i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512],'box':box,'size':size,'paste':paste})
(p/'work-registration.json').write_text(json.dumps({'source_sha256':hashlib.sha256((p/'work-source.png').read_bytes()).hexdigest(),'scale':scale,'alpha_threshold':128,'filter':'LANCZOS; binary alpha128 before and after','frames':rows,'replacement_rectangles':rects},indent=2))
kneel=[Image.open(p/f'lowering-{i:03}.png').convert('RGBA') for i in range(6)]
for v in ('bare','helmet'):
 idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(Path('character/major-bill-v3/frames')/v/'idle-north/000.png').convert('RGBA'),(36,52))
 poses={'kneel':kneel.copy(),'repair':[Image.open(p/f'work-{i:03}.png').convert('RGBA') for i in range(6)]}
 if v=='helmet':
  overlay=HelmetRebaker(None,max_height=48).overlay('north')
  for key,frames in poses.items():
   for i,frame in enumerate(frames):
    head=np.array([128,frame.getbbox()[1]+18])
    frames[i]=tilted(frame,overlay,head-[23,25],0,[*(head-[14,20]),28,34],'north')
 poses['kneel'][0]=idle;poses['stand']=list(reversed(poses['kneel']))
 for key,frames in poses.items():
  folder=out/'candidate'/v/(key+'-north');folder.mkdir(parents=True,exist_ok=True)
  for i,frame in enumerate(frames):frame.save(folder/f'{i:03}.png')
b=Image.new('RGB',(1056,420),(23,33,41))
for row,key in enumerate(['kneel','repair']):
 for i in range(6):
  f=Image.open(out/f'candidate/bare/{key}-north/{i:03}.png').crop((40,54,216,236));b.paste(f,(i*176,row*210),f);ImageDraw.Draw(b).text((i*176+8,row*210+188),key+str(i),fill='white')
b.save(out/'candidate-review.png')
