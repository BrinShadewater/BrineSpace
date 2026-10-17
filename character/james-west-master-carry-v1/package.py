from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
master=Image.open(p/'master-input.png').convert('RGB');a=np.asarray(master).astype(float)
# Existing direct-West green-key/largest component rule, used solely for the
# static original master comparison and its one standing-derived registration.
green=(a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90)
labels,_=ndimage.label(~green);counts=np.bincount(labels.ravel());counts[0]=0;mask=labels==counts.argmax()
ys,xs=np.where(mask);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
scale=148/(bounds[3]-bounds[1]);offset=(128-round((bounds[0]+bounds[2]-1)*.5*scale),224-round(bounds[3]*scale))
reference=Image.fromarray(np.dstack([np.asarray(master),mask.astype('uint8')*255]))
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.size==master.size and raw.getchannel('A').getextrema()==(0,255)
def register(im):
    out=Image.new('RGBA',(256,256));out.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),offset);return out
new=register(raw);new.save(p/'carry-pose.png');ref=register(reference);ref.save(p/'registered-original-master.png')
idle=Image.open(p/'matte-idle-reference.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
# Load the actual original native idle, rather than round-trip its preview.
m=json.loads((r/'character/crew-runtime-matte-v1/branforth/manifest.json').read_bytes());s=next(s for s in m['states'] if s['id']=='idle-west');idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(r/'character/crew-runtime-matte-v1/branforth'/s['frameFiles'][0]).convert('RGBA'),(128-round(m['pivot'][0]),224-round(m['pivot'][1])))
turn=Image.open(r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png').convert('RGBA')
cargo=Image.open(r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png').convert('RGBA')
rows=[('original detailed West master',ref),('selected matte West idle',idle),('current turn West endpoint',turn),('current cargo West endpoint',cargo),('new master-based carry',new)]
board=Image.new('RGB',(1600,640),'#303b40');draw=ImageDraw.Draw(board)
for j,(label,im) in enumerate(rows):
    draw.text((j*320+4,8),label,fill='white');board.paste(im,(j*320+32,24),im)
    crop=im.crop((96,56,176,136)).resize((320,320),Image.Resampling.NEAREST);board.paste(crop,(j*320,290),crop)
board.save(p/'master-comparison.png')
native=Image.new('RGB',(1000,250),'#303b40')
for j,(_,im) in enumerate(rows):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'station-scale.png')
report={'selected':False,'visualReviewPending':True,'rawSize':list(raw.size),'originalMasterBounds':bounds,'standingDerivedScale':scale,'fixedWholeCanvasOffset':list(offset),'nativeBounds':list(new.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'originalMasterNativeBounds':list(ref.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'rawSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'scope':'One bare master-based carrying pose,not full source family/animation/helmet/native or owner acceptance. One original-standing-derived wholecanvas scale/offset, no generated-pose fit/palette/geometry edits.'}
(p/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
