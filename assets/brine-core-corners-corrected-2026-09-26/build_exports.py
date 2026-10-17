from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
jobs=json.loads((ROOT/'production.json').read_text())['jobs']
sources={r['id']:r['path'] for r in json.loads((ROOT/'sources.json').read_text())}
for folder in ['masters','game-size']: (ROOT/folder).mkdir(exist_ok=True)
rows=[]
for j in jobs:
 p=ROOT/'masters'/(j['id']+'.png')
 if not p.exists(): shutil.copy2(sources[j['id']],p)
 im=Image.open(p).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();crop=im.crop(box)
 limits=[int(v/.34) for v in j['world_limit']]
 factor=min(limits[0]/crop.width,limits[1]/crop.height)
 size=tuple(int(v*factor) for v in crop.size)
 small=crop.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
 out=Image.new('RGBA',(size[0]+8,size[1]+8));out.paste(small,(4,4));dest=ROOT/'game-size'/(j['id']+'.png');out.save(dest)
 w,h=[v*.34 for v in size];west=j['id'].endswith('nw');x=-188.647323608398 if west else 186.158681926555-w;y=-192
 north_gap=(-36-(x+w)) if west else x-36;side_gap=-36-(y+h)
 a=np.array(im);rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>240)&(rgb.min(2)>140)&((rgb.max(2)-rgb.min(2))<35)
 rows.append(dict(id=j['id'],crop=box,content_size=size,canvas=out.size,world_units_per_pixel=.34,world_size=[w,h],proposed_content_origin=[x,y],texture_padding_pixels=4,north_lane_gap=north_gap,north_gap_after_10_padding=north_gap-10,side_lane_gap=side_gap,side_gap_after_10_padding=side_gap-10,pale_material_median=np.median(rgb[mask],axis=0).tolist(),runtime_verified=False,master_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),export_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
 assert out.getchannel('A').getextrema()==(0,255) and north_gap>=10 and side_gap>=10
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2))
for tone,bg in [('light',(205,207,200)),('dark',(35,41,44))]:
 sheet=Image.new('RGB',(900,440),bg);d=ImageDraw.Draw(sheet)
 for i,r in enumerate(rows):
  im=Image.open(ROOT/'game-size'/(r['id']+'.png'));sheet.paste(im,(i*450+(450-im.width)//2,405-im.height),im)
  d.text((i*450+15,420),r['id'],fill='white' if tone=='dark' else 'black')
 sheet.save(ROOT/f'review-{tone}.png')
print(json.dumps([dict(id=r['id'],world=r['world_size'],north_margin=r['north_gap_after_10_padding'],side_margin=r['side_gap_after_10_padding'],pale_rgb=r['pale_material_median']) for r in rows]))
