from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
R=P.parent/'crew-runtime-matte-v1/bill'
m=json.loads((R/'manifest.json').read_text())
west=P.parent/'bill-video-west-v2';ws=json.loads((west/'manifest.json').read_text())['states'][0]
m['states']=[ws if s['id']=='walk-west' else s for s in m['states']]
def hair(a,d):
 rgb=a[:,:,:3].astype(float);yy,xx=np.where(a[:,:,3]>127);top=yy.min()
 y=np.indices(a.shape[:2])[0]
 # Conservative crown region: avoids exposed face, beard, collar and suit.
 depth={'south':7,'east':10,'west':10,'north':15}[d]
 return (a[:,:,3]>127)&(y<top+depth)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.10)&(rgb[:,:,0]<145)
sources={};samples={}
for s in m['states']:
 d=s['id'].split('-')[1];root=west if s['id']=='walk-west' else R
 arr=[np.array(Image.open(root/f).convert('RGBA')) for f in s['frameFiles']];sources[s['id']]=arr
 if s['id'].startswith('walk-'):samples[d]=np.concatenate([a[:,:,:3][hair(a,d)] for a in arr])
target=np.median(samples['east'],axis=0)*.88
gains={d:np.clip(target/np.median(v,axis=0),.72,1.0) for d,v in samples.items()}
checks=[]
for s in m['states']:
 key=s['id'];d=key.split('-')[1];dest=P/'frames'/key;dest.mkdir(parents=True,exist_ok=True)
 for i,a in enumerate(sources[key]):
  mask=hair(a,d);out=a.copy();out[:,:,:3][mask]=np.rint(a[:,:,:3][mask]*gains[d]).astype('uint8')
  assert np.array_equal(out[:,:,3],a[:,:,3]);assert np.array_equal(out[~mask],a[~mask])
  Image.fromarray(out).save(dest/f'{i:03}.png');checks.append(int(mask.sum()))
 s['frameFiles']=[f'frames/{key}/{i:03}.png' for i in range(len(sources[key]))]
m['status']='hair_colour_review_candidate';m['name']='Bill consistent darker brown crown';m['strideDistanceCells']['walk-west']=69/384
(P/'manifest.json').write_text(json.dumps(m,indent=2))
(P/'checks.json').write_text(json.dumps({'targetMedianRGB':target.tolist(),'fixedDirectionGains':{k:v.tolist() for k,v in gains.items()},'frames':len(checks),'changedCrownPixelsRange':[min(checks),max(checks)],'alphaAndOutsideMaskUnchanged':True,'scope':'Conservative crown only; face and beard preserved. Per-direction constant gain shared by idle/walk. No new poses.'},indent=2))
out=[]
for t in range(72):
 bg=Image.new('RGB',(800,480),'#303b40');draw=ImageDraw.Draw(bg)
 for j,d in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']=='walk-'+d);n=int(t/72*len(s['frameFiles'])/s.get('gaitCycles',1));before=Image.fromarray(sources[s['id']][n]);after=Image.open(P/s['frameFiles'][n]).convert('RGBA')
  draw.text((j*200+10,8),d+' / original',fill='white');bg.paste(before,(j*200,25),before)
  draw.text((j*200+10,225),'Matched darker brown',fill='white');bg.paste(after,(j*200,245),after)
 out.append(bg)
out[0].save(P/'comparison.png');out[0].save(P/'comparison.gif',save_all=True,append_images=out[1:],duration=[10*(round((i+1)*150/72)-round(i*150/72)) for i in range(72)],loop=0)
(P/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#172226;color:#dbe4df;font:18px system-ui;max-width:900px;margin:24px auto}img{max-width:100%}</style><h1>Bill · darker brown hair across directions</h1><p>Original above, corrected below. Same motion and suit pixels. Conservative crown correction; face and beard unchanged. Review candidate.</p><img src="comparison.gif">')
print('Built',len(checks),'frames; alpha and all pixels outside hair mask identical.')
