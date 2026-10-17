from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
S=Path('character/bill-hair-match-v4');P=Path('character/bill-material-match-v1');P.mkdir(exist_ok=True)
sources={};medians={}
def fabric(a):
 r=a[:,:,:3].astype(float);y=np.indices(a.shape[:2])[0];v=r.mean(2);return (a[:,:,3]>240)&(y>=60)&(y<153)&(np.ptp(r,axis=2)<18)&(v>25)&(v<90)
for d in ['south','east','north','west']:
 m=json.loads((S/d/'manifest.json').read_text());arr=[np.array(Image.open(S/d/f).convert('RGBA')) for f in m['states'][0]['frameFiles']];sources[d]=(m,arr);medians[d]=np.median(np.concatenate([a[:,:,:3][fabric(a)] for a in arr]),axis=0)
target=np.min(np.array(list(medians.values())),axis=0);report={};sheet=Image.new('RGB',(800,440),'#303b40');draw=ImageDraw.Draw(sheet)
for j,(d,(m,arr)) in enumerate(sources.items()):
 gain=np.minimum(target/medians[d],1);counts=[];hashes={};newSamples=[]
 for i,(a,f) in enumerate(zip(arr,m['states'][0]['frameFiles'])):
  rgb=a[:,:,:3].astype(float);y,x=np.indices(a.shape[:2]);spread=np.ptp(rgb,axis=2);v=rgb.mean(2);weight=np.clip((22-spread)/10,0,1)*np.clip((105-v)/25,0,1)*np.clip((v-18)/12,0,1)*np.clip((y-53)/9,0,1)*(a[:,:,3]>16)
  result=rgb*(1+weight[:,:,None]*(gain-1));h=np.zeros(a.shape[:2],bool)
  if d in ['east','west']:
   top=np.where(a[:,:,3]>127)[0].min();dy=y-top;cx=np.median(x[(a[:,:,3]>127)&(dy<8)]);back=(x<cx+3)&(x>cx-11) if d=='east' else (x>cx-3)&(x<cx+11)
   h=(a[:,:,3]>16)&((dy<10)|((dy<21)&back)|((dy>=19)&(dy<27)))&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]<112)&(rgb[:,:,1]<60)&(v<68)
   l=rgb[h]@np.array([.2126,.7152,.0722]);brown=np.array([43,34,28]);result[h]=l[:,None]*brown/(brown@np.array([.2126,.7152,.0722]))
  b=a.copy();b[:,:,:3]=np.clip(np.rint(result),0,255).astype('uint8');allowed=(weight>0)|h;assert np.array_equal(a[~allowed],b[~allowed]);assert np.array_equal(a[:,:,3],b[:,:,3]);out=P/d/f;out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out);hashes[f]=hashlib.sha256(out.read_bytes()).hexdigest();counts.append(int(h.sum()));newSamples.append(b[:,:,:3][fabric(a)])
  if i==0:
   for row,c in enumerate([a,b]):
    im=Image.fromarray(c);sheet.paste(im,(j*200,row*215+20),im);draw.text((j*200+5,row*215+3),d+(' before' if row==0 else ' matched'),fill='white')
 m['states'][0]['provenance']['materialPass']='Fixed neutral fabric gain shared across clip; red side hair shifted to restrained brown hue with luminance retained.';(P/d/'manifest.json').write_text(json.dumps(m,indent=2));(P/d/'frame-hashes.json').write_text(json.dumps(hashes,indent=2));report[d]=dict(beforeFabric=medians[d].tolist(),target=target.tolist(),gain=gain.tolist(),afterFabric=np.median(np.concatenate(newSamples),axis=0).tolist(),hairPixelsRange=[min(counts),max(counts)],alphaAndOutsideMasksExact=True)
sheet.save(P/'material-comparison.png');(P/'validation.json').write_text(json.dumps(report,indent=2));html=(S/'index.html').read_text().replace('Dark brown crown, sideburns and beard matched across directions. Approved suit, proportions and motion retained.','Graphite suit tones matched across directions; remaining red in side-view hair reduced. Poses and timing unchanged.').replace('hair-comparison.png','material-comparison.png').replace('Hair before / after','Materials before / after');(P/'index.html').write_text(html);print(report)

