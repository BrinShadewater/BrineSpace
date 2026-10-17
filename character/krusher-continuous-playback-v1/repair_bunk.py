from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
from scipy import ndimage
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';L=json.loads((H/'library-v10.json').read_text());s=L['states']['helmet:bunk-enter-east'];pilot=H/'pilot';pilot.mkdir(exist_ok=True);report=[];board=Image.new('RGBA',(2000,800),'#303c42');d=ImageDraw.Draw(board)
for col,i in enumerate([1,2,3,4,6]):
 p=R/s['files'][i].lstrip('/');im=Image.open(p).convert('RGBA');a=np.array(im);lab,n=ndimage.label(a[:,:,3]>96);areas=np.bincount(lab.ravel());areas[0]=0;body=areas.argmax();head=next((int(k) for k in np.argsort(areas)[::-1] if k and k!=body and areas[k]>700),0);hc=lab==head;bc=lab==body;
 if i==4:
  roi=a[:,:,3]>96;roi[190:]=False;rl,_=ndimage.label(roi);ar=np.bincount(rl.ravel());ar[0]=0;hc=rl==ar.argmax();bc=(a[:,:,3]>96)&~hc
 dh=ndimage.distance_transform_edt(~hc);db=ndimage.distance_transform_edt(~bc);mask=(a[:,:,3]>0)&(dh<3)&(dh<db);layer=np.zeros_like(a);layer[mask]=a[mask];base=a.copy();base[mask]=0;candidates=[]
 for dy in range(-4,5):
  for dx in range(-4,5):
   if i!=6 and dy<0 or i==6 and dx<0:continue
   if i in [2,3] and dx!=0:continue
   if i==4 and (dx!=0 or dy!=4):continue
   moved=ndimage.shift(hc.astype('uint8'),(dy,dx),order=0,cval=0)>0;contacts=int((ndimage.binary_dilation(moved)&bc).sum());overlap=int((moved&bc).sum())
   if contacts>=7:candidates.append((dx*dx+dy*dy,overlap,-contacts,dx,dy))
 chosen=min(candidates);dx,dy=chosen[-2:];out=Image.fromarray(base);out.alpha_composite(Image.fromarray(layer),(dx,dy));arr=np.array(out);labs,_=ndimage.label(arr[:,:,3]>96);warm=(arr[:,:,0]>arr[:,:,1].astype(float)*1.1)&(arr[:,:,0]>arr[:,:,2].astype(float)*1.15)&(arr[:,:,0]>55)&(arr[:,:,3]>190);newhead=ndimage.shift(hc.astype('uint8'),(dy,dx),order=0,cval=0)>0;main=np.bincount(labs.ravel());main[0]=0;assert np.all(labs[newhead]==main.argmax()),i;dest=pilot/('bunk-helmet-%d.png'%i);out.save(dest);(H/'masks').mkdir(exist_ok=True);union=mask|(ndimage.shift(mask.astype('uint8'),(dy,dx),order=0,cval=0)>0);mp=H/'masks'/('bunk-'+str(i)+'.png');Image.fromarray(union.astype('uint8')*255).save(mp);assert np.array_equal(a[~union],arr[~union]);report.append({'mask':mp.relative_to(R).as_posix(),'slot':i,'source':s['files'][i].lstrip('/'),'output':dest.relative_to(R).as_posix(),'shift':[dx,dy],'opaqueContactPixels':-chosen[2],'overlapPixels':chosen[1]})
 for row,image in enumerate([im,out]):
  bb=im.getbbox();view=image.crop(bb);view=view.resize((view.width*2,view.height*2),Image.Resampling.NEAREST);board.alpha_composite(view,(col*400+10,row*390+30));d.text((col*400+10,row*390+5),('V10' if row==0 else 'registered '+str([dx,dy]))+' pose '+str(i),fill='white')
board.save(H/'bunk-registration-pilot.png');(H/'bunk-registration.json').write_text(json.dumps(report,indent=2));print(report)
