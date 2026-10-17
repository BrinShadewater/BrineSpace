from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=Image.open(P/'raw-unload-v1.png').convert('RGBA');a=np.array(raw)
occupied=(a[:,:,3]>200).any(0);bounds=[0]
for i in range(1,6):
    nominal=round(i*raw.width/6);possible=np.where(~occupied[max(0,nominal-45):nominal+46])[0]+max(0,nominal-45)
    assert len(possible),('No gutter',i)
    bounds.append(int(possible[np.argmin(np.abs(possible-nominal))]))
bounds.append(raw.width)
cells=[np.array(raw.crop((bounds[i],0,bounds[i+1],raw.height))) for i in range(6)]
ys,xs=np.where(cells[0][:,:,3]>200);scale=148/(ys.max()-ys.min()+1)
rows=[];board=Image.new('RGB',(1536,584),'#202a30');draw=ImageDraw.Draw(board)
(P/'ungraded-unload').mkdir(exist_ok=True)
for i,cell in enumerate(cells):
    labels,n=label(cell[:,:,3]>200);sizes=np.bincount(labels.ravel());sizes[0]=0
    body_id=int(np.argmax(sizes));body=labels==body_id
    if i>=3:
        keep=binary_dilation(body,iterations=2);cell=cell.copy();cell[~keep,3]=0
    # The hand-held floor-contact case can touch the glove/body component.
    # Restrict that contact row to the boot side of the cell rather than
    # treating a connected foreground component as an anatomical landmark.
    yy,xx=np.where(body);floor=int(yy.max())
    footmask=body[max(0,floor-7):floor+1].copy()
    if i in [2,5]:footmask[:,:round(cell.shape[1]*.43)]=False
    by,bx=np.where(footmask);center=(bx.min()+bx.max())/2
    offset=(round(128-center*scale),round(224-floor*scale))
    im=Image.fromarray(cell);out=Image.new('RGBA',(256,256))
    out.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),offset)
    out.save(P/f'ungraded-unload/{i:03}.png')
    oa=np.array(out);oy,ox=np.where(oa[:,:,3]>128);_,hx=np.where(oa[oy.min():oy.min()+20,:,3]>128)
    rows.append({'pose':i,'sourceCell':[bounds[i],0,bounds[i+1],raw.height],'bodyComponent':body_id,'sourceBootFloor':floor,'sourceBootCenter':float(center),'bootContactExclusionLeftFraction':.43 if i in [2,5] else 0,'offset':list(offset),'headTop':int(oy.min()),'top20pxWidth':int(hx.max()-hx.min()+1),'visibleHeight':int(oy.max()-oy.min()+1),'releasedCaseRemoved':i in [3,4],'authoredIdleIgnoredForPackage':i==5})
    old=Image.open(R/f'character/veld-unload-west-consistent-v1/frames/bare/{i:03}.png').convert('RGBA')
    for row,(name,frame) in enumerate([('Selected unload',old),('New ungraded body',out)]):
        board.paste(frame,(i*256,row*292+24),frame);draw.text((i*256+4,row*292+4),name+' '+str(i),fill='white')
board.save(P/'unload-source-comparison.png')
case_box=(1082,552,1204,656)
case=raw.crop(case_box)
case.resize((round(case.width*scale),round(case.height*scale)),Image.Resampling.LANCZOS).save(P/'floor-case.png')
(P/'unload-extraction.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256((P/'raw-unload-v1.png').read_bytes()).hexdigest(),'scale':scale,'gutterBounds':bounds,'rows':rows,'unobstructedCaseSourceBox':list(case_box),'scope':'singlefirst-standing148ruler; physical boot contact translations; released standalone case component separated only; no body anatomy or per-pose scale edits','visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'gutterBounds':bounds,'headWidths':[x['top20pxWidth'] for x in rows],'scale':scale,'bootFloors':[x['sourceBootFloor'] for x in rows]}))
