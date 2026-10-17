from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;rows=[];ims=[]
for i,path in enumerate(sorted((P/'frames').glob('*.png'))):
    im=Image.open(path).convert('RGBA');ims.append(im);a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);opaque=a[:,:,3]>192;top=int(yy[opaque].min())
    skin=opaque&(yy<top+32)&(r>g+10)&(r>b+12)&(g>b+2)&(r+g+b>180)&~((g>b+15)&(r-g<15))
    cloth=opaque&(yy>=67)&(yy<145)&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<100)&~((r-b>18)&(g-b>10))
    fy,fx=np.where(opaque[155:177,100:123]);anchor=[100+int(fx.max()),155+int(fy.max())]
    rows.append({'index':i,'crown':top,'sole':int(yy[opaque].max()),'frontBoot':anchor,'skinPixels':int(skin.sum()),'skinMedian':np.median(rgb[skin],0).tolist(),'clothMedian':np.median(rgb[cloth],0).tolist()})
for name,rect,scale,cols in [('heads',(62,8,128,66),2,16),('tools',(62,54,143,124),2,16),('body',(48,8,145,180),1,12)]:
    w=(rect[2]-rect[0])*scale;h=(rect[3]-rect[1])*scale;board=Image.new('RGB',(cols*(w+8),math.ceil(len(ims)/cols)*(h+24)),'#303b40');draw=ImageDraw.Draw(board)
    for i,im in enumerate(ims):
        crop=im.crop(rect).resize((w,h),Image.Resampling.NEAREST);at=(i%cols*(w+8),i//cols*(h+24));board.paste(crop,(at[0],at[1]+22),crop);draw.text((at[0]+4,at[1]+4),str(i),fill='white')
    board.save(P/('all-source-'+name+'.png'))
(P/'source-diagnostics.json').write_text(json.dumps({'rows':rows,'scope':'Fixed extracted native ruler diagnostics; no per-frame normalization or source selection. Median samples mix material boundaries and need visual review.'},indent=2),encoding='utf-8')
print(json.dumps({'frames':len(rows),'crownRange':[min(x['crown'] for x in rows),max(x['crown'] for x in rows)],'soleRange':[min(x['sole'] for x in rows),max(x['sole'] for x in rows)],'bootAnchors':sorted({tuple(x['frontBoot']) for x in rows}),'readSamples':[{k:v for k,v in rows[i].items() if k in ['index','skinMedian','clothMedian']} for i in [65,74,78,82,86,90,98]]}))
