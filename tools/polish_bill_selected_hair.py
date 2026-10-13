from pathlib import Path
import json,hashlib,re
import numpy as np
from PIL import Image,ImageDraw
P=Path('character/bill-hair-match-v3');P.mkdir(exist_ok=True)
roots={'south':Path('character/bill-selected-directions-v2/south'),'east':Path('character/bill-east-selected-loop-v1'),'north':Path('character/bill-selected-directions-v2/north'),'west':Path('character/crew-runtime-matte-v1/bill')}
def hair(a,d):
 rgb=a[:,:,:3].astype(float);top=np.where(a[:,:,3]>127)[0].min();y=np.indices(a.shape[:2])[0];depth={'south':7,'east':10,'west':10,'north':18}[d]
 if d=='north':return (a[:,:,3]>16)&(y<top+depth)&(rgb.max(2)<140)&(rgb[:,:,0]>rgb[:,:,1]*1.05)
 return (a[:,:,3]>16)&(y<top+depth)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.10)&(rgb[:,:,0]<140)
target=np.array([47,33,26]);report={};tracks=[];sheet=Image.new('RGB',(800,460),'#303b40');draw=ImageDraw.Draw(sheet)
for j,(d,root) in enumerate(roots.items()):
 m=json.loads((root/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='walk-'+d);arr=[np.array(Image.open(root/f).convert('RGBA')) for f in s['frameFiles']];sample=np.concatenate([a[:,:,:3][hair(a,d)] for a in arr]);median=np.median(sample,axis=0);gain=target/median;after=[];hashes={};counts=[]
 for i,a in enumerate(arr):
  mask=hair(a,d);b=a.copy();corrected=a[:,:,:3][mask]*gain; lum=corrected@np.array([.2126,.7152,.0722]); brown=target/(target@np.array([.2126,.7152,.0722])); corrected=corrected*.55+lum[:,None]*brown*.45; b[:,:,:3][mask]=np.clip(np.rint(corrected),0,255).astype('uint8');assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[~mask],b[~mask]);out=P/d/f'frames/walk-{d}/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out);hashes[f'frames/walk-{d}/{i:03}.png']=hashlib.sha256(out.read_bytes()).hexdigest();after.append(b);counts.append(int(mask.sum()))
 s['frameFiles']=list(hashes);s['provenance']=dict(source=str(root),method='Fixed direction gains plus 45% shared brown hue ramp; extended rear hair mask and translucent edge coverage. No per-frame normalization');m['states']=[s];m['status']='hair_match_candidate';(P/d/'manifest.json').write_text(json.dumps(m,indent=2));(P/d/'frame-hashes.json').write_text(json.dumps(hashes,indent=2));report[d]=dict(frames=len(arr),beforeMedian=median.tolist(),fixedGain=gain.tolist(),afterMedian=np.median(np.concatenate([b[:,:,:3][hair(a,d)] for a,b in zip(arr,after)]),axis=0).tolist(),changedPixelsRange=[min(counts),max(counts)],alphaAndOutsideMaskExact=True)
 tracks.append(dict(label=d.title()+' - dark brown',files=[d+'/'+f for f in s['frameFiles']],durations=s['frameDurationsMs']))
 for row,a in enumerate([arr[0],after[0]]):
  im=Image.fromarray(a);top=np.where(a[:,:,3]>127)[0].min();im=im.crop((60,top,130,top+34)).resize((196,95));sheet.paste(im,(j*200,row*210+30),im);draw.text((j*200+5,row*210+8),d+(' before' if row==0 else ' matched'),fill='white')
sheet.save(P/'hair-comparison.png');(P/'validation.json').write_text(json.dumps(dict(targetMedianRGB=target.tolist(),directions=report,scope='Crown hair only, face/beard/suit and all timing preserved; runtime unchanged'),indent=2));html=Path('character/bill-selected-directions-v2/index.html').read_text();html=re.sub(r'const tracks=.*?;let loaded=',lambda _: 'const tracks='+json.dumps(tracks)+';let loaded=',html);html=html.replace('South: 20% less body chroma, with a gentle 5% reduction on skin and hair. North: 3.5% larger around the fixed foot pivot. East and west unchanged.','Polished dark brown hair: rear hair coverage, translucent edge colours and restrained highlights. Approved suit finish, proportions and motion retained.');html=html.replace('<script>','<h2>Hair before / after</h2><img src="hair-comparison.png" style="max-width:100%"><script>');(P/'index.html').write_text(html);print(json.dumps(report))
