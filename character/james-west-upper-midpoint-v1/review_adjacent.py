from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'inputs.json').read_bytes());a=json.loads((p/'adjacent-inputs.json').read_bytes())
assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in a.items())
source=Image.open(r/d['sources'][1]).convert('RGBA');box=(104,64,162,134)
poses=[Image.open(r/d['sources'][0]).convert('RGBA')]
for name in ['early','midpoint','late']:
    raw=Image.open(p/('raw.png' if name=='midpoint' else name+'-raw.png')).convert('RGBA')
    assert raw.size==(1254,1254)
    crop=raw.resize((80,80),Image.Resampling.LANCZOS)
    im=source.copy();im.paste(crop.crop((8,8,66,78)),(104,64));im.save(p/(name+'-candidate.png'))
    assert all(im.getpixel((x,y))==source.getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
    poses.append(im)
poses.append(Image.open(r/d['sources'][2]).convert('RGBA'))
board=Image.new('RGB',(1600,640),'#303b40');draw=ImageDraw.Draw(board)
for i,(name,im) in enumerate(zip(['entry','early','midpoint','late','exit'],poses)):
    draw.text((i*320+8,8),name,fill='white');board.paste(im,(i*320+32,30),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(i*320,290),upper)
board.save(p/'adjacent-comparison.png')
native=Image.new('RGB',(1000,240),'#303b40');nd=ImageDraw.Draw(native)
for i,im in enumerate(poses):
    nd.text((i*200+4,4),str(i),fill='white')
    for h,y in [(82,25),(54,125),(27,195)]:
        resized=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS)
        native.paste(resized,(i*200+80-resized.width//2,y),resized)
native.save(p/'station-scale.png')
(p/'adjacent-review.json').write_text(json.dumps({'selected':False,'visualReviewPending':True,'newAuthoredUpperPoses':3,'protectedPixelsEach':61476,'scope':'Source comparison on one common original body; not final full-body bank or native playback.','sourceHashes':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['raw.png','early-raw.png','late-raw.png']}},indent=2)+'\n')
print('Three upper poses packaged at original crop origin/common80/1254 scale;61476protected pixels each.')
