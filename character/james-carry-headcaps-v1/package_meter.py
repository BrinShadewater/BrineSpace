from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
info=json.loads((p/'meter-inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in info['preCallSha256'].items())
base=Image.open(r/info['base']).convert('RGBA');raw=Image.open(p/'meter-raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((40,40),Image.Resampling.LANCZOS);crop.save(p/'meter-native.png');rect=tuple(info['admissionRegion'])
out=base.copy();out.paste(crop.crop((rect[0]-120,rect[1]-128,rect[2]-120,rect[3]-128)),rect[:2]);out.save(p/'late-meter-pose.png')
masked=[base.copy(),out.copy()]
for im in masked:im.paste((0,0,0,0),rect)
assert masked[0].tobytes()==masked[1].tobytes()
for suffix,items,scale in [('whole',[base,out],2),('detail',[im.crop((120,128,160,168)) for im in [base,out]],8)]:
    w=items[0].width*scale;h=items[0].height*scale;board=Image.new('RGBA',(2*w,h+26),(48,59,63,255));d=ImageDraw.Draw(board)
    for i,im in enumerate(items):board.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+5,7),['before lower duplicate','after lower removal'][i],fill='white')
    board.convert('RGB').save(p/('meter-'+suffix+'-comparison.png'))
report={'rawSha256':hashlib.sha256((p/'meter-raw.png').read_bytes()).hexdigest(),'rawSize':raw.size,'admissionRegion':rect,'protectedOutsidePixels':65440,'protectedOutsideExact':True,'upperRetainedMeterOutsideRegion':True,'perPoseFit':False,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Remove late lower duplicate only; upper meter/face/case/feet and all outside rectangle exact. Hand/body contact in admitted region still visually reviewed.'}
(p/'meter-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('Late duplicate removal packaged;65440outside pixels exact.')
