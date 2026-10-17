from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
p=Path(__file__).resolve().parent;r=p.parents[1];name=sys.argv[1]
inputs=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
raw=Image.open(p/(name+'-raw.png')).convert('RGBA');assert raw.width==raw.height
crop=inputs['crop'];rect=inputs['admissionRegion'];native=raw.resize((crop[2]-crop[0],crop[3]-crop[1]),Image.Resampling.LANCZOS);native.save(p/(name+'-native-crop.png'))
base=Image.open(p/'base.png').convert('RGBA');out=base.copy();out.paste(native.crop((rect[0]-crop[0],rect[1]-crop[1],rect[2]-crop[0],rect[3]-crop[1])),rect[:2]);out.save(p/(name+'.png'))
a=base.copy();b=out.copy()
for im in [a,b]:im.paste((0,0,0,0),rect)
assert a.tobytes()==b.tobytes()
full=Image.new('RGBA',(512,282),(48,59,63,255));d=ImageDraw.Draw(full)
for i,im in enumerate([base,out]):full.alpha_composite(im,(i*256,26));d.text((i*256+5,7),'original base' if not i else name,fill='white')
full.convert('RGB').save(p/(name+'-full-comparison.png'))
detail=Image.new('RGBA',(768,410),(48,59,63,255));d=ImageDraw.Draw(detail)
for i,im in enumerate([base,out]):detail.alpha_composite(im.crop(crop).resize((384,384),Image.Resampling.NEAREST),(i*384,26));d.text((i*384+5,7),'original base' if not i else name,fill='white')
detail.convert('RGB').save(p/(name+'-detail-comparison.png'))
station=Image.new('RGBA',(900,420),(48,59,63,255));d=ImageDraw.Draw(station)
for row,im in enumerate([base,out]):
    for j,h in enumerate([148,82,54,27]):
        sz=round(256*h/148);x=[140,410,620,790][j];station.alpha_composite(im.resize((sz,sz),Image.Resampling.LANCZOS),(round(x-128*h/148),round(195+row*205-224*h/148)));d.text((x-60,row*205+8),('base ' if row==0 else name+' ')+str(h),fill='white')
station.convert('RGB').save(p/(name+'-station-comparison.png'))
(p/(name+'-review.json')).write_text(json.dumps({'protectedOutsideExact':True,'protectedOutsidePixels':65536-(rect[2]-rect[0])*(rect[3]-rect[1]),'boundsAlpha128':out.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'rawSha256':hashlib.sha256((p/(name+'-raw.png')).read_bytes()).hexdigest(),'scope':'One generated contact pose, source review only; no native/full gait/cadence/context acceptance.'},indent=2)+'\n',encoding='utf-8')
print(name+': outside pixels exact; fixed source-canvas density, no fit/grade.')
