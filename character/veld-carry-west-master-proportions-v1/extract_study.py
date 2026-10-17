from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy.ndimage import label,find_objects
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
version=sys.argv[1] if len(sys.argv)>1 else '1'
assert version in ['1','2']
raw=P/('raw-v'+version+'.png');outdir=P if version=='1' else P/'v2-study'
outdir.mkdir(exist_ok=True)
im=Image.open(raw).convert('RGBA');a=np.array(im)
labels,count=label(a[:,:,3]>200);boxes=[]
for n,slices in enumerate(find_objects(labels),1):
    if slices and np.count_nonzero(labels[slices]==n)>10000:
        y,x=slices;boxes.append((x.start,y.start,x.stop,y.stop))
boxes.sort();assert len(boxes)==6,boxes
first=boxes[0];scale=148/(first[3]-first[1]);floor=first[3]-1
board=Image.new('RGB',(1536,900),'#202a30');draw=ImageDraw.Draw(board)
rows=[];(outdir/'study-frames').mkdir(exist_ok=True)
for i,box in enumerate(boxes):
    x0,y0,x1,y1=box
    bounds=(max(0,x0-2),max(0,y0-2),min(im.width,x1+2),min(im.height,y1+2))
    crop=im.crop(bounds);pixels=np.asarray(crop)
    row=round((y0+(y1-y0)*.59)-bounds[1])
    _,px=np.where(pixels[max(0,row-2):row+3,:,3]>200)
    pelvis=(px.min()+px.max())/2
    out=Image.new('RGBA',(256,256));resized=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    offset=(round(128-pelvis*scale),round(224-(floor-bounds[1])*scale))
    out.alpha_composite(resized,offset);out.save(outdir/f'study-frames/{i:03}.png')
    source=np.array(out);ys,xs=np.where(source[:,:,3]>128);_,hx=np.where(source[ys.min():ys.min()+20,:,3]>128)
    width=int(hx.max()-hx.min()+1)
    rows.append({'pose':i,'sourceBox':list(box),'cropBox':list(bounds),'offset':list(offset),'top20pxWidth':width,'visibleHeight':int(ys.max()-ys.min()+1)})
    old=Image.open(R/f'character/veld-carry-west-consistent-v1/frames/bare/{i:03}.png').convert('RGBA')
    master=Image.open(R/'character/veld-side-foundation-v1/west-standing.png').convert('RGBA');m=Image.new('RGBA',(256,256));m.alpha_composite(master,(36,52))
    for j,(name,frame) in enumerate([('Original master',m),('Selected carry',old),('New ungraded study',out)]):
        board.paste(frame,(i*256,j*300+22),frame);draw.text((i*256+3,j*300+3),name+' pose'+str(i),fill='white')
board.save(outdir/'source-comparison.png')
(outdir/'study-registration.json').write_text(json.dumps({'scale':scale,'sourceFloor':floor,'rows':rows,'status':'ungraded source study, no runtime/helmet/admission','sourceSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'scope':'single148pxstanding ruler from first pose, no per-frame scaling/grade; coarse top20px width includes bun/collar, not skull measurement'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'scale':scale,'top20pxWidths':[r['top20pxWidth'] for r in rows],'sourceBoxes':boxes}))
