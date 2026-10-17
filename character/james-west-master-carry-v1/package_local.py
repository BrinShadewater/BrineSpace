from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'local-inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
raw=Image.open(p/'local-raw.png').convert('RGBA');assert raw.width==raw.height and raw.getchannel('A').getextrema()==(0,255)
crop=raw.resize((80,80),Image.Resampling.LANCZOS);base=Image.open(p/'local-original.png').convert('RGBA');new=base.copy()
x0,y0,x1,y1=inputs['admissionRegion'];cx,cy=inputs['crop'][:2];new.paste(crop.crop((x0-cx,y0-cy,x1-cx,y1-cy)),(x0,y0))
outside=np.ones((256,256),bool);outside[y0:y1,x0:x1]=False
assert np.array_equal(np.asarray(base)[outside],np.asarray(new)[outside]);new.save(p/'local-carry-pose.png')
rows=[('selected matte idle',base),('current turn endpoint',Image.open(r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png').convert('RGBA')),('current cargo endpoint',Image.open(r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png').convert('RGBA')),('new local carry',new)]
board=Image.new('RGB',(1280,640),'#303b40');draw=ImageDraw.Draw(board)
for j,(label,im) in enumerate(rows):
    draw.text((j*320+4,8),label,fill='white');board.paste(im,(j*320+32,24),im)
    upper=im.crop((86,80,166,160)).resize((320,320),Image.Resampling.NEAREST);board.paste(upper,(j*320,290),upper)
board.save(p/'local-master-comparison.png')
native=Image.new('RGB',(800,250),'#303b40')
for j,(_,im) in enumerate(rows):
    for h,y in [(82,25),(54,125),(27,195)]:
        small=im.resize((round(256*h/148),)*2,Image.Resampling.LANCZOS);native.paste(small,(j*200+80-small.width//2,y),small)
native.save(p/'local-station-scale.png')
detail=Image.new('RGB',(1280,670),'#303b40');draw=ImageDraw.Draw(detail)
for j,(label,im) in enumerate([('original crop',Image.open(p/'local-target.png').convert('RGBA')),('generated crop',raw)]):
    draw.text((j*640+4,8),label,fill='white');shown=im.resize((640,640),Image.Resampling.LANCZOS);detail.paste(shown,(j*640,30),shown)
detail.save(p/'local-crop-comparison.png')
report={'selected':False,'visualReviewPending':True,'rawSize':list(raw.size),'protectedOriginalPixels':int(outside.sum()),'admissionRegion':inputs['admissionRegion'],'nativeBounds':list(new.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'originalNativeBounds':list(base.getchannel('A').point(lambda x:255 if x>=180 else 0).getbbox()),'rawSha256':hashlib.sha256((p/'local-raw.png').read_bytes()).hexdigest(),'registration':'Whole generated square->80,original crop86/96; no pose fit/grade','scope':'One bare local source pose; exact selected idle outside admitted torso/arm/hip region. Head/lower legs/boots unchanged. Not full motion/equipment/native/owner acceptance; crop includes upper knee/hip pixels, not an arm-only pixel invariant.'}
(p/'local-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
