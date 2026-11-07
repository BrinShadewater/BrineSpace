from pathlib import Path
import re,json,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
S=Path('character/crew-side-gameplay-review-v6');P=Path('character/crew-edge-finish-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);L=np.array([.2126,.7152,.0722]);Y=np.indices((184,184))[0];report={};sheet=Image.new('RGB',(736,880),'#303b40');draw=ImageDraw.Draw(sheet)
def fabric(a):
 r=a[:,:,:3].astype(float);v=r@L;return (a[:,:,3]>240)&(Y>60)&(Y<153)&(np.ptp(r,axis=2)<28)&(v>25)&(v<110)
def finish(a,gain):
 r=a[:,:,:3].astype(float);alpha=a[:,:,3];dist=distance_transform_edt(alpha>16);edge=(alpha>0)&((dist<=2)|(alpha<240));excess=np.maximum(r[:,:,1]-np.maximum(r[:,:,0],r[:,:,2]),0);spill=edge&(excess>0);b=a.copy();out=r.copy();out[:,:,1][spill]-=excess[spill];v=r.mean(2);w=np.clip((38-np.ptp(r,axis=2))/12,0,1)*np.clip((Y-51)/10,0,1)*(alpha>0);out*=1+w[:,:,None]*(gain-1);b[:,:,:3]=np.clip(np.rint(out),0,255).astype('uint8');assert np.array_equal(alpha,b[:,:,3]);assert np.array_equal(a[(~spill)&(w*(gain-1)==0)],b[(~spill)&(w*(gain-1)==0)]);return b,int(spill.sum())
for j,t in enumerate(tracks):
 idle=np.array(Image.open(S/t['idle']).convert('RGBA'));arr=[np.array(Image.open(S/f).convert('RGBA')) for f in t['files']];gain=1.
 if t['label'].startswith('James'):
  iv=np.median(idle[:,:,:3][fabric(idle)]@L);wv=np.median(np.concatenate([a[:,:,:3][fabric(a)] for a in arr])@L);gain=float(np.clip(iv/wv,.82,1))
 out,n=finish(idle,1);rel=f'{j}/idle.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(dest);t['idle']='../crew-edge-finish-v1/'+rel;files=[];count=n
 for i,a in enumerate(arr):
  b,n=finish(a,gain);count+=n;rel=f'{j}/walk/{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append('../crew-edge-finish-v1/'+rel)
  if i==0:
   for k,c in enumerate([out,b]):
    im=Image.fromarray(c);sheet.paste(im,(k*368+92,j*220+25),im);draw.text((k*368+5,j*220+5),t['label']+(' idle' if k==0 else ' walk'),fill='white')
 t['files']=files;report[t['label']]={'walkFabricGain':gain,'greenEdgePixels':count,'alphaExact':True,'timingUnchanged':True}
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));(P/'tracks.json').write_text(json.dumps(tracks,indent=2));Q=Path('character/crew-side-gameplay-review-v7');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks));h=re.sub(r'<p>James idles.*?</p>','<p>Green edge spill suppressed on all four pairs. James walking fabric brightness matched toward idle. Alpha, geometry and timing unchanged. Preview only.</p>',h);(Q/'index.html').write_text(h,encoding='utf-8');print(report)
