from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
import numpy as np,json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];(H/'sources').mkdir(exist_ok=True)
im=Image.open(H/'generated-standing-style-v1.png').convert('RGBA');names=['south','east','north','west'];parts=[];records=[]
limits={'south':(180,85,365,283,245,220,329),'east':(190,85,375,277,242,226,349),'north':(195,80,355,264,239,225,331),'west':(200,80,388,274,243,225,369)}
for i,d in enumerate(names):
 cell=im.crop((i*im.width//4,0,(i+1)*im.width//4,im.height));a=np.array(cell);yy,xx=np.indices(a.shape[:2]);x0,y0,x1,y1,band,nx0,nx1=limits[d];r,g,b=[a[:,:,k].astype(float) for k in range(3)]
 warm=(r>g*1.055)&(r>b*1.09);allowed=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)&((yy<band)|(warm&(xx>=nx0)&(xx<nx1)))
 mask=allowed&(a[:,:,3]>8);lab,_=ndimage.label(mask,np.ones((3,3)));counts=np.bincount(lab.ravel());counts[0]=0;mask=lab==counts.argmax();a[~mask]=0;part=Image.fromarray(a);box=part.getbbox();part=part.crop(box);parts.append((d,part,box))
scale=29/parts[0][1].height
board=Image.new('RGBA',(1200,360),'#252d31');draw=ImageDraw.Draw(board);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
for i,(d,part,box) in enumerate(parts):
 size=tuple(round(n*scale) for n in part.size);native=part.resize(size,Image.Resampling.LANCZOS);p=H/'sources'/('style-'+d+'-native.png');native.save(p)
 # Native, 4x and 7x views all come from the same exported pixels.
 board.alpha_composite(native,(i*300+10,42));board.alpha_composite(native.resize((native.width*7,native.height*7),Image.Resampling.NEAREST),(i*300+70,65));draw.text((i*300+10,10),d+' / native + 7x',font=font,fill='white')
 records.append({'direction':d,'cell':i,'sourceBox':box,'sourceSize':part.size,'uniformScale':scale,'nativeSize':native.size,'resample':'Lanczos, preserving authored alpha; no per-axis fit','sourceHash':hashlib.sha256((H/'generated-standing-style-v1.png').read_bytes()).hexdigest(),'output':p.relative_to(H).as_posix()})
board.save(H/'extracted-heads-review.png');(H/'standing-extraction.json').write_text(json.dumps({'source':'generated-standing-style-v1.png','records':records},indent=2)+'\n');print(json.dumps({'uniformScale':scale,'sizes':[q['nativeSize'] for q in records]}))
