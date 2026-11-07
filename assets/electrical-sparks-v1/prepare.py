from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageFilter
P=Path(__file__).resolve().parent
raw=Image.open(P/'source.png').convert('RGB');atlas=Image.new('RGBA',raw.size);records=[]
for i in range(8):
 x,y=(i%4)*384,(i//4)*512
 rgb=np.array(raw.crop((x,y,x+384,y+512)));r,g,b=rgb.astype('int16').transpose(2,0,1)
 chroma=((b-r>25)&(g-r>12))|((r-b>30)&(r-g>10))
 near=np.array(Image.fromarray(chroma.astype('uint8')*255).filter(ImageFilter.MaxFilter(7)))>0
 mask=chroma|((rgb.min(axis=2)>225)&near)
 yy,xx=np.where(mask);foot=int(yy.max());root=round(float(np.median(xx[yy>=foot-8])))
 dx,dy=192-root,472-foot
 assert xx.min()+dx>=0 and xx.max()+dx<384 and yy.min()+dy>=0 and yy.max()+dy<512
 rgba=np.zeros((512,384,4),dtype='uint8');rgba[mask,:3]=rgb[mask];rgba[mask,3]=255
 frame=Image.new('RGBA',(384,512));frame.paste(Image.fromarray(rgba),(dx,dy));atlas.paste(frame,(x,y))
 records.append({'frame':i,'translation':[dx,dy],'pixels':int(mask.sum())})
atlas.save(P/'sparks-atlas.png');small=atlas.resize((384,256),Image.Resampling.NEAREST);small.save(P/'sparks-96x128.png')
assert all(small.crop(((i%4)*96,(i//4)*128,(i%4+1)*96,(i//4+1)*128)).getbbox() for i in range(8))
(P/'manifest.json').write_text(json.dumps({'grid':[4,2],'cell':[96,128],'pivot':[48,118],'fps':12,'frames':records,'source_sha256':hashlib.sha256((P/'source.png').read_bytes()).hexdigest()},indent=2),encoding='utf-8')
print('8 nonempty registered RGBA frames; no clipping; 96x128 runtime cells.')
