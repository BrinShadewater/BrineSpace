from pathlib import Path
from PIL import Image,ImageDraw
import sys,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];name=sys.argv[1];assert name in ['early','late']
info=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in info['preCallSha256'].items())
base=Image.open(r/info['base']).convert('RGBA');raw=Image.open(p/(name+'-raw.png')).convert('RGBA');assert raw.width==raw.height
crop=raw.resize((64,64),Image.Resampling.LANCZOS);crop.save(p/(name+'-native.png'))
rect=tuple(info['admissionRegion']);out=base.copy();out.paste(crop.crop((rect[0]-96,rect[1]-64,rect[2]-96,rect[3]-64)),rect[:2]);out.save(p/(name+'-pose.png'))
masked=[base.copy(),out.copy()]
for im in masked:im.paste((0,0,0,0),rect)
assert masked[0].tobytes()==masked[1].tobytes()
ims=[base,out];labels=['original roof','generated roof repair']
for suffix,items,scale in [('whole',ims,2),('head',[im.crop((96,64,160,128)) for im in ims],6)]:
    w=items[0].width*scale;h=items[0].height*scale;board=Image.new('RGBA',(2*w,h+26),(48,59,63,255));d=ImageDraw.Draw(board)
    for i,(im,label) in enumerate(zip(items,labels)):board.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+5,7),label,fill='white')
    board.convert('RGB').save(p/(name+'-'+suffix+'-comparison.png'))
bounds=[im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for im in ims]
report={'rawSha256':hashlib.sha256((p/(name+'-raw.png')).read_bytes()).hexdigest(),'rawSize':raw.size,'crop':info['crop'],'admissionRegion':rect,'protectedOutsidePixels':65288,'protectedOutsideExact':True,'nativeAlpha128BoundsBeforeAfter':bounds,'perPoseFit':False,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Generated hair-roof band only; face/ears/collar/body/case/feet outside region exact, full master proportion/motion unproved.'}
(p/(name+'-review.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'name':name,'boundsBeforeAfter':bounds,'protected':65288}))
