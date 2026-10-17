from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,sys
p=Path(__file__).resolve().parent;r=p.parents[1];name=sys.argv[1]
info=json.loads((p/(name+'-inputs.json')).read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in info['preCallSha256'].items())
bare=Image.open(r/info['bareSource']).convert('RGBA');raw=Image.open(p/(name+'-raw.png')).convert('RGBA');assert raw.width==raw.height
crop=raw.resize((64,64),Image.Resampling.LANCZOS);crop.save(p/(name+'-native.png'));rect=tuple(info['admissionRegion'])
paired=bare.copy();paired.paste(crop.crop((rect[0]-96,rect[1]-56,rect[2]-96,rect[3]-56)),rect[:2]);paired.save(p/(name+'-helmet.png'))
masked=[bare.copy(),paired.copy()]
for im in masked:im.paste((0,0,0,0),rect)
assert masked[0].tobytes()==masked[1].tobytes()
ims=[Image.open(p/'south-standing.png').convert('RGBA'),bare,paired,Image.open(p/'west-standing.png').convert('RGBA')];labels=['South helmet master','paired bare target',name+' generated helmet','West helmet master']
for suffix,items,scale in [('whole',ims,1),('head',[im.crop((96,56,160,120)) for im in ims],5)]:
    w=items[0].width*scale;h=items[0].height*scale;out=Image.new('RGBA',(4*w,h+26),(48,59,63,255));d=ImageDraw.Draw(out)
    for i,(im,label) in enumerate(zip(items,labels)):out.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+5,7),label,fill='white')
    out.convert('RGB').save(p/(name+'-'+suffix+'-comparison.png'))
report={'rawSha256':hashlib.sha256((p/(name+'-raw.png')).read_bytes()).hexdigest(),'rawSize':raw.size,'admissionRegion':rect,'protectedOutsidePixels':62992,'protectedOutsideExact':True,'nativeAlpha128Bounds':paired.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox(),'uniformWholeCropScale':64/raw.width,'perPoseFit':False,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Single helmet projection paired with unchanged carried body outside fixed head/collar region; master helmet contour/face/perspective/material review required.'}
(p/(name+'-review.json')).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'name':name,'bounds':report['nativeAlpha128Bounds'],'protectedOutside':62992}))
