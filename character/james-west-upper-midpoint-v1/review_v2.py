from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
d=json.loads((p/'inputs.json').read_bytes());frozen=json.loads((p/'v2-inputs.json').read_bytes())
assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in frozen.items())
body=Image.open(r/d['sources'][1]).convert('RGBA');poses=[Image.open(r/d['sources'][0]).convert('RGBA')]
for name in ['early-v2','midpoint','late-v2']:
    raw=Image.open(p/('raw.png' if name=='midpoint' else name+'-raw.png')).convert('RGBA');assert raw.size==(1254,1254)
    crop=raw.resize((80,80),Image.Resampling.LANCZOS);im=body.copy();im.paste(crop.crop((8,8,66,78)),(104,64))
    assert all(im.getpixel((x,y))==body.getpixel((x,y)) for y in range(256) for x in range(256) if not(104<=x<162 and 64<=y<134))
    im.save(p/(name+'-candidate.png'));poses.append(im)
poses.append(Image.open(r/d['sources'][2]).convert('RGBA'))
board=Image.new('RGB',(1600,640),'#303b40');draw=ImageDraw.Draw(board)
for i,(name,im) in enumerate(zip(['entry','early v2','midpoint','late v2','exit'],poses)):
    draw.text((i*320+8,8),name,fill='white');board.paste(im,(i*320+32,30),im)
    upper=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(i*320,290),upper)
board.save(p/'v2-comparison.png')
native=Image.new('RGB',(1000,250),'#303b40');nd=ImageDraw.Draw(native)
for i,im in enumerate(poses):
    nd.text((i*200+4,4),str(i),fill='white')
    for h,y in [(82,25),(54,125),(27,195)]:
        resized=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(resized,(i*200+80-resized.width//2,y),resized)
native.save(p/'v2-station-scale.png')
report={'selected':False,'visualReviewPending':True,'protectedPixelsEach':61476,'uniformScale':80/1254,'scope':'Three upper comparison poses on a common original middle body; endpoints exact. Not final native bank.','preCallHashesUnchanged':True,'rawHashes':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['early-v2-raw.png','raw.png','late-v2-raw.png']}}
(p/'v2-review.json').write_text(json.dumps(report,indent=2)+'\n');print('Two endpoint-targeted revisions packaged;exact outside pixels and frozen inputs verified.')
