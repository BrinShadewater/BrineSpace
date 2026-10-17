from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,sys
p=Path(__file__).resolve().parent;r=p.parents[1];phase=sys.argv[1];name='contact-'+phase;repair=name+'-feet';inputs=json.loads((p/(repair+'-inputs.json')).read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
raw=Image.open(p/(repair+'-raw.png')).convert('RGBA');assert raw.width==raw.height;native=raw.resize((80,80),Image.Resampling.LANCZOS);native.save(p/(repair+'-native-crop.png'))
base=Image.open(p/(name+'.png')).convert('RGBA');out=base.copy();rect=inputs['admissionRegion'];out.paste(native.crop((0,21,80,48)),(88,197));out.save(p/(repair+'.png'))
a=base.copy();b=out.copy()
for im in [a,b]:im.paste((0,0,0,0),rect)
assert a.tobytes()==b.tobytes()
board=Image.new('RGBA',(1024,580),(48,59,63,255));d=ImageDraw.Draw(board)
for i,im in enumerate([base,out]):
    board.alpha_composite(im,(i*256,28));d.text((i*256+5,7),'before repair' if not i else repair,fill='white')
    board.alpha_composite(im.crop((88,176,168,256)).resize((320,320),Image.Resampling.NEAREST),(i*320,255))
    for j,h in enumerate([82,54,27]):
        sz=round(256*h/148);x=[700,830,960][j];board.alpha_composite(im.resize((sz,sz),Image.Resampling.LANCZOS),(round(x-128*h/148),round(195+i*205-224*h/148)))
board.convert('RGB').save(p/(repair+'-comparison.png'))
(p/(repair+'-review.json')).write_text(json.dumps({'outsideExact':True,'protectedOutsidePixels':63376,'boundsAlpha128':out.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox(),'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'rawSha256':hashlib.sha256((p/(repair+'-raw.png')).read_bytes()).hexdigest(),'scope':'Local generated boot/ankle baseline repair; not complete gait/cadence/native acceptance.'},indent=2)+'\n',encoding='utf-8')
print(repair+':63376outside pixels exact; bounds '+str(out.getchannel('A').point(lambda x:255 if x>=128 else 0).getbbox()))
