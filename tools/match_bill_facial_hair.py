from pathlib import Path
import json, numpy as np, shutil
from PIL import Image,ImageDraw
P=Path('character/bill-hair-match-v4');P.mkdir(exist_ok=True);S=Path('character/bill-hair-match-v3');report={};sheet=Image.new('RGB',(800,300),'#303b40');draw=ImageDraw.Draw(sheet)
def mask(a,d):
 rgb=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);top=np.where(a[:,:,3]>127)[0].min();crown=(a[:,:,3]>127)&(yy<top+8);cx=np.median(xx[crown]);dy=yy-top
 if d=='north':return np.zeros(a.shape[:2],bool)
 side=(abs(xx-cx)>6) if d=='south' else ((xx<cx+1)&(xx>cx-4) if d=='east' else (xx>cx-1)&(xx<cx+4))
 region=((dy>=18)&(dy<27))|((dy>=8)&(dy<20)&side)
 return region&(a[:,:,3]>127)&(rgb[:,:,0]>rgb[:,:,1]*1.18)&(rgb[:,:,1]>rgb[:,:,2]*1.06)&(rgb[:,:,0]<125)&(rgb.mean(2)<76)
for j,d in enumerate(['south','east','north','west']):
 m=json.loads((S/d/'manifest.json').read_text());s=m['states'][0];arr=[np.array(Image.open(S/d/f).convert('RGBA')) for f in s['frameFiles']];samples=[a[:,:,:3][mask(a,d)] for a in arr];target=np.array([47,33,26]);median=np.median(np.concatenate(samples),axis=0) if d!='north' else target;gain=np.minimum(target/median,1);counts=[]
 for i,(a,f) in enumerate(zip(arr,s['frameFiles'])):
  sel=mask(a,d);b=a.copy();v=a[:,:,:3][sel]*gain;l=v@np.array([.2126,.7152,.0722]);v=.3*v+.7*l[:,None]*(target/(target@np.array([.2126,.7152,.0722])));b[:,:,:3][sel]=np.clip(np.rint(v),0,255).astype('uint8');assert np.array_equal(a[~sel],b[~sel]);assert np.array_equal(a[:,:,3],b[:,:,3]);out=P/d/f;out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out);counts.append(int(sel.sum()))
  if i==0:
   top=np.where(a[:,:,3]>127)[0].min()
   for row,c in enumerate([a,b]):
    im=Image.fromarray(c).crop((60,top,130,top+34)).resize((196,95));sheet.paste(im,(j*200,row*140+22),im);draw.text((j*200+5,row*140+3),d+(' before' if row==0 else ' beard matched'),fill='white')
 s['provenance']['facialHair']='Fixed masked beard/sideburn gain plus shared brown hue. No per-frame normalization.';(P/d/'manifest.json').write_text(json.dumps(m,indent=2));report[d]=dict(frames=len(arr),fixedGain=gain.tolist(),pixelsRange=[min(counts),max(counts)],alphaAndOutsideMaskExact=True)
sheet.save(P/'hair-comparison.png');html=(S/'index.html').read_text().replace('Polished dark brown hair: rear hair coverage, translucent edge colours and restrained highlights. Approved suit finish, proportions and motion retained.','Dark brown crown, sideburns and beard matched across directions. Approved suit, proportions and motion retained.');(P/'index.html').write_text(html);(P/'validation.json').write_text(json.dumps(report,indent=2));print(report)
