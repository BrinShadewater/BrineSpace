from pathlib import Path
import imageio.v2 as iio,numpy as np,json
from scipy import ndimage
P=Path(__file__).resolve().parent
r=iio.get_reader(P/'source.mp4');rows=[]
for n,a in enumerate(r):
 v=np.asarray(a).astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90);lab,_=ndimage.label(~key);c=np.bincount(lab.ravel());c[0]=0;m=lab==c.argmax();yy,xx=np.where(m);top=yy.min();hy,hx=np.where(m[top:top+60]);rows.append([n,int(top),int(yy.max()-top+1),int(hx.max()-hx.min()+1)])
r.close();(P/'scale-audit.json').write_text(json.dumps(rows,indent=2));print('frame, top, height, headwidth',rows[::20],rows[-1])
