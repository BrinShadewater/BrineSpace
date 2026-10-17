from pathlib import Path
from PIL import Image,ImageDraw
import imageio.v2 as iio,numpy as np,json,sys
from scipy import ndimage
P=Path(__file__).resolve().parent
for direction in sys.argv[1:]:
 raw=[np.asarray(x) for x in iio.get_reader(P/f'{direction}-padded-source.mp4')];small=[];clipped=[]
 sheet=Image.new('RGB',(1280,400),'#263139');draw=ImageDraw.Draw(sheet)
 for j,idx in enumerate(range(0,min(len(raw),144),9)):
  im=Image.fromarray(raw[idx]).resize((160,160));sheet.paste(im,((j%8)*160,(j//8)*200+20));draw.text(((j%8)*160+5,(j//8)*200+4),str(idx),fill='white')
 sheet.save(P/f'{direction}-padded-contact.png')
 for a in raw:
  v=a.astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90);lab,n=ndimage.label(~key);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();y,x=np.where(mask);clipped.append(x.min()==0 or y.min()==0 or x.max()==767 or y.max()==767)
  im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255]));sm=np.array(im.resize((96,96),Image.Resampling.LANCZOS)).astype(float)/255;small.append(sm[:,:,:3]*sm[:,:,3:4])
 scores=[]
 for start in range(25,95):
  for length in range(24,53):
   end=start+length
   if end+2>=len(raw) or any(clipped[start:end]):continue
   score=sum(np.mean((small[start+k][36:]-small[end+k][36:])**2) for k in [-2,-1,0,1,2])/5;scores.append((float(score),start,length))
 scores.sort();(P/f'{direction}-padded-cycles.json').write_text(json.dumps(scores[:30],indent=2));print(direction,scores[:5], 'clipped',sum(clipped))
