from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parent
jobs=[('master',R/'crew-side-masters-v1/bill-side-master-01.png',(960,5,1140,175)),('V8',R/'bill-land-water-west-v8/sources/lift-master-v2.png',(280,100,550,410)),('V9 hands',P/'sources/lift-head-hands-v3.png',(280,100,550,410)),('V9 head',P/'sources/lift-head-v4.png',(280,100,550,410))]
board=Image.new('RGB',(1600,350),'#182932');d=ImageDraw.Draw(board);records=[]
for i,(name,file,box) in enumerate(jobs):
    im=Image.open(file).convert('RGBA');a=np.array(im);x0,y0,x1,y1=box;b=a[y0:y1,x0:x1];r,g,blue=[b[:,:,k].astype(float) for k in range(3)]
    mask=(b[:,:,3]>180)&(r>=40)&(r<=160)&(r>g*1.15)&(g>blue*1.2);lab,_=label(mask);counts=np.bincount(lab.ravel());largest=lab==np.argmax(counts[1:])+1;yy,xx=np.where(largest);bounds=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    edge=bounds[0]==0 or bounds[1]==0 or bounds[2]==b.shape[1] or bounds[3]==b.shape[0]
    records.append(dict(name=name,source=file.relative_to(R).as_posix(),roi=box,largestBrownComponentBounds=bounds,width=bounds[2]-bounds[0],height=bounds[3]-bounds[1],componentTouchesROIEdge=edge,scope='Bounded brown hair/face proxy; not full head/anatomy acceptance.'))
    crop=im.crop(box);tile=Image.new('RGBA',crop.size);tile.alpha_composite(crop);board.paste(tile,(i*400,30),tile);d.text((i*400+4,4),name+' raw same1x scale; brown component',fill='white');d.rectangle((i*400+bounds[0],30+bounds[1],i*400+bounds[2]-1,30+bounds[3]-1),outline='#74c8c1')
(P/'head-audit.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');board.save(P/'head-audit.png');print(json.dumps(records))
