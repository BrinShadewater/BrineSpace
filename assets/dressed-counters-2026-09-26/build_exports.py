from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil
ROOT=Path(__file__).resolve().parent
jobs=json.loads((ROOT/'production.json').read_text())['jobs']
sources={r['id']:r['path'] for r in json.loads((ROOT/'sources.json').read_text())}
for folder in ['masters','game-size']: (ROOT/folder).mkdir(exist_ok=True)
rows=[]
for j in jobs:
 p=ROOT/'masters'/(j['id']+'.png')
 if not p.exists(): shutil.copy2(sources[j['id']],p)
 im=Image.open(p).convert('RGBA'); box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox()
 box=(max(0,box[0]-4),max(0,box[1]-4),min(im.width,box[2]+4),min(im.height,box[3]+4))
 crop=im.crop(box); scale=min(j['size'][0]/crop.width,j['size'][1]/crop.height)
 size=tuple(max(1,round(v*scale)) for v in crop.size)
 small=crop.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
 out=Image.new('RGBA',(size[0]+8,size[1]+8));out.paste(small,(4,4))
 dest=ROOT/'game-size'/(j['id']+'.png');out.save(dest)
 rows.append(dict(id=j['id'],master_size=im.size,crop=box,visible_size=size,canvas=out.size,alpha=out.getchannel('A').getextrema(),suggested_display_width=round(out.width*.34,2),runtime_verified=False,master_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2))
for tone,bg in [('light',(205,207,200)),('dark',(35,41,44))]:
 out=Image.new('RGB',(720,300),bg);d=ImageDraw.Draw(out)
 for i,r in enumerate(rows):
  im=Image.open(ROOT/'game-size'/(r['id']+'.png'));x=i%2*360;y=i//2*220
  out.paste(im,(x+(360-im.width)//2,y+250-im.height),im)
  d.text((x+15,y+267),r['id'].removeprefix('counter-dressed-'),fill='white' if tone=='dark' else 'black')
 out.save(ROOT/f'review-{tone}.png')
assert len(rows)==2 and all(r['alpha']==(0,255) for r in rows)
print('2 masters preserved; 2 calibrated RGBA exports; light/dark review sheets written.')


