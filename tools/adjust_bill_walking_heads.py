from pathlib import Path
import json,hashlib,re
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
P=Path('character/bill-walk-head-v1');P.mkdir(exist_ok=True);R=Path('character/crew-runtime-matte-v1/bill');m=json.loads((R/'manifest.json').read_text());report={};sheet=Image.new('RGB',(736,440),'#303b40');draw=ImageDraw.Draw(sheet)
for col,d in enumerate(['east','west']):
 s=next(s for s in m['states'] if s['id']=='walk-'+d);files=[];hashes={}
 for i,f in enumerate(s['frameFiles']):
  a=np.array(Image.open(R/f).convert('RGBA'));yy,xx=np.indices(a.shape[:2],dtype=float);top=int(np.where(a[:,:,3]>127)[0].min());head=(a[:,:,3]>127)&(yy<top+10);cx=float(np.median(xx[head]));anchor=top+25;weight=np.clip((anchor-yy)/4,0,1);scale=1-.03*weight;sx=cx+(xx-cx)/scale;sy=anchor+(yy-anchor)/scale
  # Premultiplied sampling avoids dark halos at transparent hair edges.
  v=a.astype(float)/255;v[:,:,:3]*=v[:,:,3:4];b=np.stack([map_coordinates(v[:,:,k],[sy,sx],order=1,mode='constant',cval=0) for k in range(4)],axis=2);alpha=b[:,:,3:4];b[:,:,:3]=np.divide(b[:,:,:3],alpha,out=np.zeros_like(b[:,:,:3]),where=alpha>0);out=np.clip(np.rint(b*255),0,255).astype('uint8');out[yy>=anchor]=a[yy>=anchor];assert np.array_equal(out[yy>=anchor],a[yy>=anchor]);rel=f'frames/walk-{d}/{i:03}.png';dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(dest);files.append(rel);hashes[rel]=hashlib.sha256(dest.read_bytes()).hexdigest()
  if i==0:
   for row,im in enumerate([Image.fromarray(a),Image.fromarray(out)]):sheet.paste(im,(col*368+92,row*215+20),im);draw.text((col*368+8,row*215+3),d+(' installed' if row==0 else ' head -3%'),fill='white')
 s['frameFiles']=files;s['provenance']['headAdjustment']='3% head scale about neck anchor at crown+25px, four-pixel transition into unchanged body; premultiplied bilinear sampling';report[d]=dict(frames=len(files),scale=.97,bodyPixelsExact=True,timingUnchanged=True);(P/f'{d}-hashes.json').write_text(json.dumps(hashes,indent=2))
for s in m['states']:
 if s['id'] not in ['walk-east','walk-west']:s['frameFiles']=['../crew-runtime-matte-v1/bill/'+f for f in s['frameFiles']]
(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps(report,indent=2));sheet.save(P/'comparison.png')
html=Path('character/crew-idle-match-v1/index.html').read_text();raw=re.search(r'const tracks=(.*?);let ready=',html).group(1);tracks=json.loads(raw)
for t in tracks:
 who,d=t['label'].lower().split();t['idleFiles']=['../crew-idle-match-v1/'+f for f in t['idleFiles']];t['idle']='../crew-idle-match-v1/'+t['idle']
 if who=='bill' and d in ['east','west']:
  s=next(s for s in m['states'] if s['id']=='walk-'+d);t['files']=s['frameFiles']
html=html.replace(raw,json.dumps(tracks)).replace('Matched idle preview','Bill walking head adjustment').replace('Candidate only; no runtime changes.','Bill east/west walking heads reduced 3%; all other poses unchanged. Candidate only; no runtime changes.').replace('src="contact.png"','src="comparison.png"');(P/'index.html').write_text(html);print(report)
