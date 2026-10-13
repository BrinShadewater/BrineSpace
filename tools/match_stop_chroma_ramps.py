from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
S=Path('character/crew-side-gameplay-review-v4');P=Path('character/crew-stop-neutral-v1');P.mkdir(exist_ok=True);h=(S/'index.html').read_text(encoding='utf-8');raw=re.search(r'const tracks=(.*?);const c=',h).group(1);tracks=json.loads(raw);L=np.array([.2126,.7152,.0722]);sheet=Image.new('RGB',(1104,880),'#303b40');draw=ImageDraw.Draw(sheet);report={}
for j,t in enumerate(tracks):
 a=np.array(Image.open(S/t['idle']).convert('RGBA'));walk=[np.array(Image.open(S/f).convert('RGBA')) for f in t['files']];samples=[]
 for b in walk:
  rgb=b[:,:,:3].astype(float);spread=np.ptp(rgb,axis=2);sel=(b[:,:,3]>240)&(spread<28);samples.append(rgb[sel])
 pixels=np.concatenate(samples);lum=pixels@L;centers=np.arange(10,251,20);ch=[]
 for center in centers:
  ss=pixels[abs(lum-center)<15];ch.append(np.median(ss-(ss@L)[:,None],axis=0) if len(ss) else np.zeros(3))
 ch=np.array(ch);r=a[:,:,:3].astype(float);v=r@L;chroma=np.stack([np.interp(v,centers,ch[:,k]) for k in range(3)],2);target=v[:,:,None]+chroma
 # Match neutral shadows AND highlights. Warm skin/hair and yellow/red badges stay outside.
 spread=np.ptp(r,axis=2);w=np.clip((35-spread)/12,0,1)*(a[:,:,3]>0);out=r+w[:,:,None]*(target-r);b=a.copy();b[:,:,:3]=np.clip(np.rint(out),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);f=f'idle-{j}.png';Image.fromarray(b).save(P/f);t['idle']='../crew-stop-neutral-v1/'+f;report[t['label']]={'luminanceCenters':centers.tolist(),'walkChromaRamp':ch.tolist(),'alphaExact':True,'outsideMaskExact':True,'luminancePreservedBeforeRounding':True}
 for k,(c,label) in enumerate([(a,'Previous idle'),(b,'Neutral idle'),(walk[0],'Walk reference')]):
  im=Image.fromarray(c);sheet.paste(im,(k*368+92,j*220+25),im);draw.text((k*368+8,j*220+4),t['label']+' '+label,fill='white')
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));Q=Path('character/crew-side-gameplay-review-v5');Q.mkdir(exist_ok=True);h=h.replace(raw,json.dumps(tracks)).replace('James idle green cast corrected toward walk chroma; brightness and geometry retained.','All four idles: neutral shadows, midtones and highlights matched to their walking colour ramps. Brightness and geometry retained.');(Q/'index.html').write_text(h,encoding='utf-8');print('4 idles corrected across luminance ranges; walk assets untouched.')
