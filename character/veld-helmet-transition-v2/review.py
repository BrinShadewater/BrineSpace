"""Extract fixed-scale source poses and review colour drift, without inventing motion."""
from pathlib import Path
import json,sys
import imageio.v2 as iio
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
scale=148/911/.78/.75
size=round(768*scale);offset=(92-round(384*scale),196-round(705*scale))
stem=sys.argv[1] if len(sys.argv)>1 else 'source'
reader=iio.get_reader(P/f'{stem}.mp4');raw=[a for a in reader];reader.close()
frames=[];bounds=[];stats=[]
for n,a in enumerate(raw):
 a=np.asarray(a);v=a.astype(float)
 key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 labels,_=ndimage.label(~key);counts=np.bincount(labels.ravel());counts[0]=0;mask=labels==counts.argmax()
 im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255]));f=Image.new('RGBA',(184,208));f.alpha_composite(im.resize((size,size),Image.Resampling.LANCZOS),offset);frames.append(f)
 ys,xs=np.where(mask);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
 # Stationary lower-leg fabric patch: excludes silver straps, boots, blue trim and green key.
 patch=v[530:565,333:367];neutral=(np.ptp(patch,axis=2)<24)&(patch.mean(axis=2)>25)&(patch.mean(axis=2)<145)
 pixels=patch[neutral];stats.append({'sourceFrame':n,'fabricSamplePixels':int(len(pixels)),'medianRGB':np.median(pixels,axis=0).tolist() if len(pixels) else None})
contact=Image.new('RGB',(184*8,232*3),'#263139');draw=ImageDraw.Draw(contact)
for j,n in enumerate(np.linspace(0,len(frames)-1,24).astype(int)):
 x=j%8*184;y=j//8*232;contact.paste(frames[n],(x,y+20),frames[n]);draw.text((x+5,y+4),f'Frame {n}',fill='white')
contact.save(P/f'{stem}-contact.png')
review=[]
for f in frames:
 b=Image.new('RGB',(552,624),'#263139');f=f.resize(b.size,Image.Resampling.NEAREST);b.paste(f,(0,0),f);review.append(b)
review[0].save(P/f'{stem}-review.gif',save_all=True,append_images=review[1:],duration=[round((i+1)*1000/24)-round(i*1000/24) for i in range(len(review))],loop=0,optimize=False)
(P/f'{stem}-checks.json').write_text(json.dumps({'frameCount':len(frames),'scale':scale,'offset':offset,'sourceClippedFrames':[i for i,b in enumerate(bounds) if b[0]<=0 or b[1]<=0 or b[2]>=768 or b[3]>=768],'bounds':bounds,'fabricSamples':stats,'processing':'Green key and fixed body-calibrated scaling only. Uncorrected source RGB.'},indent=2)+'\n')
print(f'{len(frames)} source frames; review written')
