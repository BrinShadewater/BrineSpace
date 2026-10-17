from pathlib import Path
import json,re,numpy as np
from PIL import Image,ImageDraw
S=Path('character/crew-video-idles-v1');P=Path('character/crew-video-idles-v2');P.mkdir(exist_ok=True);Y=np.indices((184,184))[0];L=np.array([.2126,.7152,.0722]);report={};sheet=Image.new('RGB',(552,440),'#303b40');draw=ImageDraw.Draw(sheet)
def sel(a):
 r=a[:,:,:3].astype(float);v=r.mean(2);return(a[:,:,3]>240)&(Y>60)&(Y<153)&(np.ptp(r,axis=2)<30)&(v>25)&(v<100)
for row,(d,folder) in enumerate([('east','branforth-idle-led-east-neutral-v3'),('west','branforth-idle-led-west-timing-v1')]):
 a=np.array(Image.open(S/('branforth-'+d+'.png')).convert('RGBA'));R=Path('character')/folder;m=json.loads((R/'manifest.json').read_text());walk=[np.array(Image.open(R/f).convert('RGBA')) for f in m['states'][0]['frameFiles']];base=np.median(a[:,:,:3][sel(a)],axis=0);target=np.median(np.concatenate([b[:,:,:3][sel(b)] for b in walk]),axis=0);delta=(target-target@L)-(base-base@L);r=a[:,:,:3].astype(float);w=np.clip((35-np.ptp(r,axis=2))/12,0,1)*(a[:,:,3]>0);b=a.copy();b[:,:,:3]=np.clip(np.rint(r+w[:,:,None]*delta),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[w==0],b[w==0]);Image.fromarray(b).save(P/('branforth-'+d+'.png'));report[d]={'sourceMedian':base.tolist(),'walkMedian':target.tolist(),'chromaOffset':delta.tolist(),'alphaExact':True,'outsideMaskExact':True}
 for col,(c,label) in enumerate([(a,'Before'),(b,'Corrected idle'),(walk[0],'Walk reference')]):
  im=Image.fromarray(c);sheet.paste(im,(col*184,row*220+25),im);draw.text((col*184+5,row*220+5),d+' '+label,fill='white')
sheet.save(P/'comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));Q=Path('character/crew-side-gameplay-review-v4');Q.mkdir(exist_ok=True);h=Path('character/crew-side-gameplay-review-v3/index.html').read_text(encoding='utf-8').replace('../crew-video-idles-v1/branforth-','../crew-video-idles-v2/branforth-').replace('Standing frames from the same video sources, with matching material treatment.','James idle green cast corrected toward walk chroma; brightness and geometry retained.');(Q/'index.html').write_text(h,encoding='utf-8');print(report)
