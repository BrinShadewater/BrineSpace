from pathlib import Path
import json,re
import numpy as np
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
src=Path('character/crew-pose-match-v1');out=Path('character/bill-side-head-v3');out.mkdir(exist_ok=True)
m=json.loads((src/'bill/manifest.json').read_text());report={};sheet=Image.new('RGB',(1104,440),'#303b40');draw=ImageDraw.Draw(sheet)
y,x=np.indices((184,184),dtype=float)
for row,d in enumerate(['east','west']):
 s=next(s for s in m['states'] if s['id']=='walk-'+d);files=[]
 for n,f in enumerate(s['frameFiles']):
  a=np.array(Image.open(Path('character/crew-idle-size-match-v1/bill')/f).convert('RGBA'));top=int(np.where(a[:,:,3]>127)[0].min());cx=float(np.median(x[(a[:,:,3]>127)&(y<top+10)]));anchor=top+25;weight=np.clip((anchor-y)/5,0,1);scale=1-.08*weight
  width=.8648 if d=='east' else .8372
  widthScale=1+(width-1)*np.clip((anchor-y)/9,0,1)
  sx=cx+(x-cx)/widthScale;sy=y+(y-top)*(1/.92-1)*weight
  v=a.astype(float)/255;v[:,:,:3]*=v[:,:,3:4];b=np.stack([map_coordinates(v[:,:,k],[sy,sx],order=3,mode='constant') for k in range(4)],axis=2);alpha=b[:,:,3:4];b[:,:,:3]=np.divide(b[:,:,:3],alpha,out=np.zeros_like(b[:,:,:3]),where=alpha>0);b=np.clip(np.rint(b*255),0,255).astype('uint8');b[y>=anchor]=a[y>=anchor];assert np.array_equal(b[y>=anchor],a[y>=anchor])
  rel=f'frames/walk-{d}/{n:03}.png';dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(dest);files.append(rel)
  if n==0:
   idleM=json.loads(Path('character/crew-idle-match-v1/bill/manifest.json').read_text());idle=next(t for t in idleM['states'] if t['id']=='idle-'+d);ii=Image.open(Path('character/crew-idle-match-v1/bill')/idle['frameFiles'][0]).convert('RGBA')
   for col,(im,label) in enumerate([(ii,'Idle'),(Image.open(Path('character/bill-side-head-v2')/f).convert('RGBA'),'Previous'),(Image.fromarray(b),'Crown restored')]):
    sheet.paste(im,(col*368+92,row*220+25),im);draw.text((col*368+65,row*220+3),d+' - '+label,fill='white')
 s['frameFiles']=files;s['provenance']={'source':'character/crew-idle-size-match-v1/bill','headWidthScale':width,'headHeightScale':.92,'crownAnchored':True,'sampling':'single premultiplied cubic pass','bodyPixelsExact':True};report[d]={'frames':len(files),'headWidthScale':width,'crownAnchored':True,'bodyPixelsExact':True,'timingUnchanged':True}
for s in m['states']:
 if s['id'] not in ['walk-east','walk-west']:s['frameFiles']=['../crew-pose-match-v1/bill/'+f for f in s['frameFiles']]
(out/'manifest.json').write_text(json.dumps(m,indent=2));(out/'validation.json').write_text(json.dumps(report,indent=2));sheet.save(out/'comparison.png')
html=(src/'index.html').read_text();raw=re.search(r'const tracks=(.*?);let ready=',html).group(1);tracks=json.loads(raw)
for t in tracks:
 who,d=t['label'].lower().split()
 if who=='bill' and d in ['east','west']:t['files']=next(s for s in m['states'] if s['id']=='walk-'+d)['frameFiles']
 else:t['files']=['../crew-pose-match-v1/'+f for f in t['files']]
html=html.replace(raw,json.dumps(tracks)).replace('Crew pose proportion matching','Bill side head clarity and height').replace('src="contact.png"','src="../crew-pose-match-v1/contact.png"')
html=re.sub(r'<p>.*?</p>','<p>Bill side heads rebuilt from earlier frames with a single cubic sampling pass. Crown height restored; body and timing unchanged. Preview only.</p>',html,count=1)
html=html.replace('<h2>Static contact sheet</h2>','<h2>Bill: idle / previous / crown restored</h2>').replace('src="../crew-pose-match-v1/contact.png"','src="comparison.png"')
html=html.replace('i.onerror=reject;i.src=src','i.onerror=()=>{setTimeout(()=>{i.src=src},500)};i.src=src')
(out/'index.html').write_text(html);print(report)
