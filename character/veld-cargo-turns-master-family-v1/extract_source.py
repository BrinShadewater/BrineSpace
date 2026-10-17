from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
version=int(sys.argv[1]) if len(sys.argv)>1 else 1
pair=sys.argv[2] if len(sys.argv)>2 else 'south-west'
assert pair in ['south-west','north-west','north-east','east-south']
dest=(P if version==1 else P/f'v{version}-study') if pair=='south-west' else P/f'{pair}-v{version}-study'
dest.mkdir(exist_ok=True)
rawpath=P/f'raw-{pair}-v{version}.png'
raw=Image.open(rawpath).convert('RGBA');a=np.array(raw)
labels,n=label(a[:,:,3]>200);boxes=[]
for component,slices in enumerate(find_objects(labels),1):
    if slices and np.count_nonzero(labels[slices]==component)>20000:
        ys,xs=slices;boxes.append({'component':component,'box':[xs.start,ys.start,xs.stop,ys.stop]})
boxes.sort(key=lambda x:x['box'][0]);assert len(boxes)==6,boxes
scale=148/(boxes[0]['box'][3]-boxes[0]['box'][1]);rows=[]
(dest/'ungraded'/pair).mkdir(parents=True,exist_ok=True)
board=Image.new('RGB',(1536,876),'#202a30');draw=ImageDraw.Draw(board)
for i,item in enumerate(boxes):
    x0,y0,x1,y1=item['box'];box=(max(0,x0-2),max(0,y0-2),min(raw.width,x1+2),min(raw.height,y1+2))
    keep=binary_dilation(labels==item['component'],iterations=2);pixels=a.copy();pixels[~keep,3]=0
    floor=y1-1;_,xx=np.where(keep[max(0,floor-10):floor+1]& (a[max(0,floor-10):floor+1,:,3]>200));center=(xx.min()+xx.max())/2
    crop=Image.fromarray(pixels).crop(box);offset=(round(128-(center-box[0])*scale),round(224-(floor-box[1])*scale))
    out=Image.new('RGBA',(256,256));out.alpha_composite(crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS),offset)
    out.save(dest/f'ungraded/{pair}/{i:03}.png')
    arr=np.array(out);yy,hx=np.where(arr[:,:,3]>128);_,xx=np.where(arr[yy.min():yy.min()+20,:,3]>128)
    rows.append({'pose':i,'component':item['component'],'sourceBox':list(box),'sourceFloor':floor,'sourceBootCenter':float(center),'offset':list(offset),'top20pxWidth':int(xx.max()-xx.min()+1),'visibleHeight':int(yy.max()-yy.min()+1)})
    old=Image.open(R/f'character/veld-carry-turn-{pair}-consistent-v1/frames/bare/carry-turn-{pair}/{i:03}.png').convert('RGBA')
    for row,(name,im) in enumerate([('Selected turn',old),('New ungraded turn',out)]):
        board.paste(im,(i*256,row*292+24),im);draw.text((i*256+4,row*292+4),name+' '+str(i),fill='white')
    held=Image.open(R/'character/veld-cargo-west-master-family-v1/frames/bare/unload-west/000.png').convert('RGBA')
    board.paste(held,(i*256,608),held);draw.text((i*256+4,588),'Corrected West held join',fill='white')
board.save(dest/f'{pair}-source-comparison.png')
(dest/f'{pair}-extraction.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'scale':scale,'rows':rows,'scope':'single first cardinal standing148ruler, physical boot-floor translation, two-pixel connected alpha edge extraction; no per-pose rescale/grade/anatomy manipulation','visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'sourceFigures':6,'scale':scale,'headWidths':[r['top20pxWidth'] for r in rows]}))
