"""Review every raw source pose at the unchanged input inverse ruler."""
from pathlib import Path
import json,hashlib,math
import numpy as np
import imageio.v2 as iio
from scipy import ndimage
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
reader=iio.get_reader(P/'source.mp4');meta=reader.get_meta_data();fps=meta['fps']
input_image=Image.open(P/'master-input.png');sx=input_image.width/meta['size'][0]/4;sy=input_image.height/meta['size'][1]/4
assert abs(sx-sy)/sx<.01
sy=sx  # One uniform width-derived inverse factor, never stretch axes independently.
size=(round(meta['size'][0]*sx),round(meta['size'][1]*sy));assert abs(size[0]-148)<=1 and abs(size[1]-124)<=1
frames=[];records=[];(P/'frames').mkdir(exist_ok=True)
for i,rgb in enumerate(reader):
    rgb=np.asarray(rgb)
    f=rgb.astype(float);key=(f[:,:,1]>f[:,:,0]*1.3)&(f[:,:,1]>f[:,:,2]*1.3)&(f[:,:,1]>90)
    labs,_=ndimage.label(~key);counts=np.bincount(labs.ravel());counts[0]=0;mask=labs==counts.argmax()
    rgba=np.dstack((rgb,mask.astype(np.uint8)*255));rgba[~mask]=0
    small=Image.fromarray(rgba).resize(size,Image.Resampling.LANCZOS);im=Image.new('RGBA',(256,256));im.alpha_composite(small,(54,116));im.save(P/'frames'/f'{i:03}.png');frames.append(im)
    a=np.array(im);yy,xx=np.where(a[:,:,3]>192);opaque=a[:,:,3]>192;rgb2=a[:,:,:3].astype(float);r,g,b=rgb2.transpose(2,0,1)
    neutral=opaque&(np.ptp(rgb2,2)<28)&(rgb2.mean(2)>20)&(rgb2.mean(2)<110)&~((r-b>12)&(r-g>5))
    records.append({'index':i,'boundsAlpha192':[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())],'neutralMedian':np.median(rgb2[neutral],0).tolist(),'headTop':int(yy.min()),'soleBottom':int(yy.max())})
reader.close()
for start in range(0,len(frames),24):
    board=Image.new('RGB',(4*256,6*280),'#303b40');d=ImageDraw.Draw(board)
    for j,i in enumerate(range(start,min(start+24,len(frames)))):
        at=(j%4*256,j//4*280);board.paste(frames[i],(at[0],at[1]+24),frames[i]);d.text((at[0]+4,at[1]+4),'whole raw source '+str(i),fill='white')
    board.save(P/f'all-body-{start:03}.png')
for start in range(0,len(frames),64):
    board=Image.new('RGB',(8*188,8*180),'#303b40');d=ImageDraw.Draw(board)
    for j,i in enumerate(range(start,min(start+64,len(frames)))):
        crop=frames[i].crop((95,120,155,170)).resize((180,150),Image.Resampling.NEAREST);at=(j%8*188,j//8*180);board.paste(crop,(at[0],at[1]+24),crop);d.text((at[0]+4,at[1]+4),'head '+str(i),fill='white')
    board.save(P/f'all-heads-{start:03}.png')
preview=[]
for i,im in enumerate(frames):
    b=Image.new('RGB',(660,280),'#303b40');d=ImageDraw.Draw(b)
    for side,x,label in [(256,0,'fixed reference148px'),(144,270,'83px reference'),(94,420,'54px reference'),(47,530,'27px reference')]:
        s=im.resize((side,side),Image.Resampling.BILINEAR);b.paste(s,(x,24+round(224*(256-side)/256)),s);d.text((x+4,4),label,fill='white')
    d.text((4,265),'source frame '+str(i),fill='white');preview.append(b)
preview[0].save(P/'full-source-review.gif',save_all=True,append_images=preview[1:],duration=round(1000/fps),loop=0,disposal=2)
report={'frames':len(frames),'fps':fps,'sourceSha256':hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),'fixedInverseScale':[sx,sy],'offset':[54,116],'pivot':[128,224],'standingHeight':148,'additionalGrade':False,'loopSelected':False,'sourceReviewOnly':True,'records':records,'crownRange':[min(r['headTop'] for r in records),max(r['headTop'] for r in records)],'soleRange':[min(r['soleBottom'] for r in records),max(r['soleBottom'] for r in records)]}
(P/'source-review-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='records'}))
