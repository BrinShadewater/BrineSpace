from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent
im=Image.open(p/'clean-master.png').convert('RGBA')
box=im.getchannel('A').point(lambda a:255 if a>=8 else 0).getbbox()
crop=im.crop(box)
size=(round(crop.width*168/crop.height),168)
out=crop.convert('RGBa').resize(size,Image.Resampling.LANCZOS).convert('RGBA')
out.save(p/'body.png')
bg=Image.new('RGBA',out.size,(100,110,115,255));bg.alpha_composite(out);bg.convert('RGB').save(p/'body-review.png')
(p/'manifest.json').write_text(json.dumps(dict(state='suspended_float',direction='front_elevated',duration_seconds=8,loop=True,method='single generated body with continuous engine mesh rig; not individually painted frames',source_crop=box,export_size=size,master_sha256=hashlib.sha256((p/'clean-master.png').read_bytes()).hexdigest(),export_sha256=hashlib.sha256((p/'body.png').read_bytes()).hexdigest(),integration='isolated native core preview'),indent=2))
print(size)
