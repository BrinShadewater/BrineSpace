from pathlib import Path
from PIL import Image, ImageDraw
from scipy.ndimage import label
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parent
jobs=[('Original',R/'crew-side-masters-v1/bill-side-master-01.png',(960,5,1140,175)),('Prone v1',P/'sources/prone-master-v1.png',(330,100,560,390)),('Head v2',P/'sources/prone-head-v2.png',(330,100,560,390))]
flat=P/'sources/prone-flat-v3.png'
if flat.exists():jobs.append(('Flat v3',flat,(330,100,560,390)))
board=Image.new('RGB',(len(jobs)*400,350),'#182932');d=ImageDraw.Draw(board);records=[]
for i,(name,path,roi) in enumerate(jobs):
    crop=Image.open(path).convert('RGBA').crop(roi);a=np.array(crop);r,g,b=a[:,:,0].astype(float),a[:,:,1].astype(float),a[:,:,2].astype(float)
    mask=(a[:,:,3]>180)&(r>=40)&(r<=160)&(r>g*1.15)&(g>b*1.2)
    lab,_=label(mask);counts=np.bincount(lab.ravel());part=lab==np.argmax(counts[1:])+1;y,x=np.where(part)
    box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
    edge=box[0]==0 or box[1]==0 or box[2]==crop.width or box[3]==crop.height
    records.append(dict(name=name,source=path.relative_to(R).as_posix(),roi=roi,bounds=box,width=box[2]-box[0],height=box[3]-box[1],componentTouchesROIEdge=edge,scope='Bounded brown head proxy at common source density, not complete anatomy acceptance.'))
    board.paste(crop,(i*400+15,50),crop);d.text((i*400+4,4),name+' / same1x source density',fill='white');d.rectangle((i*400+15+box[0],50+box[1],i*400+15+box[2],50+box[3]),outline='#7ac0bf')
(P/'head-audit.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');board.save(P/'head-audit.png')
print(json.dumps([dict(name=r['name'],width=r['width'],height=r['height'],edge=r['componentTouchesROIEdge']) for r in records]))
