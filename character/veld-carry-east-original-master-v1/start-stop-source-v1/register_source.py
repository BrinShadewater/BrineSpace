"""Whole generated start/stop cells, one standing ruler and per-row shared baseline."""
from pathlib import Path
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
raw=P/'raw-start-stop-v1.png';original=Image.open(raw).convert('RGBA');cells=[]
for row in range(2):
    for col in range(6):
        box=(round(col*original.width/6),round(row*original.height/2),round((col+1)*original.width/6),round((row+1)*original.height/2))
        cell=original.crop(box);a=np.array(cell);a[a[:,:,3]==0,:3]=0;cells.append(Image.fromarray(a))
first=np.array(cells[0]);y,x=np.where(first[:,:,3]>200);estimate=round(cells[0].height*148/(y.max()-y.min()+1))
for delta in [0,1,-1,2,-2,3,-3]:
    h=estimate+delta;scale=h/cells[0].height
    test=cells[0].resize((round(cells[0].width*scale),h),Image.Resampling.LANCZOS);yy,xx=np.where(np.array(test)[:,:,3]>200)
    if int(yy.max()-yy.min()+1)==148:break
else:raise AssertionError('No first standing original148 ruler')
resized=[c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.LANCZOS) for c in cells]
baseline_offsets=[]
for anchor in [0,11]:
    ay,ax=np.where(np.array(resized[anchor])[:,:,3]>200);baseline_offsets.append(223-int(ay.max()))
rows=[];board=Image.new('RGB',(2048,640),'#202a30');d=ImageDraw.Draw(board)
for i,cell in enumerate(resized):
    a=np.array(cell);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1]
    offset=(round(123.5-(hx.min()+hx.max())/2),baseline_offsets[i//6])
    out=Image.new('RGBA',(256,256));out.alpha_composite(cell,offset);path=P/f'diagnostic-frames/{i:03d}.png';path.parent.mkdir(exist_ok=True);out.save(path)
    z=np.array(out);yy,xx=np.where(z[:,:,3]>200);clip=bool(np.any(np.concatenate([z[0,:,3],z[-1,:,3],z[:,0,3],z[:,-1,3]])>20))
    item={'pose':i,'row':'start' if i<6 else 'stop','height':int(yy.max()-yy.min()+1),'headRegionWidth':int(hx.max()-hx.min()+1),'floor':int(yy.max()),'top':int(yy.min()),'offset':list(offset),'clipped':clip}
    rows.append(item);xy=((i%6)*256,(i//6)*310+28);board.paste(out,xy,out);d.text((xy[0]+3,xy[1]-20),f"{i} H{item['height']} head{item['headRegionWidth']} floor{item['floor']}",fill='white')
for row in range(2):
    for col,(name,path) in enumerate([('Original held',R/'character/veld-east-held-original-master-v1/frames/bare/000.png'),('Current full-source stride',P.parent/'continuous-video-v3-white/clip-frames/bare/018.png')]):
        im=Image.open(path).convert('RGBA');xy=((6+col)*256,row*310+28);board.paste(im,xy,im);d.text((xy[0]+3,xy[1]-20),name,fill='white')
board.save(P/'source-master-review.png')
report={'generationId':'d6b09dfb-3571-48a7-b3eb-bd432af7cd7a','rawSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceSize':list(original.size),'grid':[6,2],'sourceScale':scale,'perRowCommonYOffset':baseline_offsets,'standingAnchors':[0,11],'rows':rows,'scope':'Single ruler matched first complete neutral standing pose to148; each row has one shared Y offset based on its standing endpoint. Whole X head-axis registration only. No per-pose resizing, floor correction, anatomy edits or RGB grading. Diagnostic source/identity/transition review; no runtime admission.'}
(P/'source-registration.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'headWidths':[r['headRegionWidth'] for r in rows],'heights':[r['height'] for r in rows],'floors':[r['floor'] for r in rows],'clipped':sum(r['clipped'] for r in rows),'scale':scale}))
