from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
raw=Image.open(p/'raw.png').convert('RGBA');assert raw.width==raw.height
# Whole canvas density conversion only. No figure-bounds fit or per-pose grade.
pose=raw.resize((256,256),Image.Resampling.LANCZOS);pose.save(p/'midpoint.png')
sources=[r/'character/james-south-master-carry-v1/carry-pose.png',p/'midpoint.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
ims=[Image.open(s).convert('RGBA') for s in sources];labels=['South reference','authored45deg candidate','West reference']
def board(name,crops,scale):
    w=crops[0].width*scale;h=crops[0].height*scale
    out=Image.new('RGBA',(w*3,h+26),(48,59,63,255));d=ImageDraw.Draw(out)
    for i,(im,label) in enumerate(zip(crops,labels)):
        out.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+6,7),label,fill='white')
    out.convert('RGB').save(p/name)
board('whole-comparison.png',ims,2)
board('upper-comparison.png',[im.crop((80,64,176,160)) for im in ims],5)
out=Image.new('RGBA',(700,320),(48,59,63,255));d=ImageDraw.Draw(out)
for row,height in enumerate([82,54,27]):
    d.text((5,row*106+7),f'{height}px standing ruler',fill='white')
    for i,im in enumerate(ims):
        size=round(256*height/148);small=im.resize((size,size),Image.Resampling.LANCZOS)
        out.alpha_composite(small,(180+i*160-size//2,row*106+96-round(224*height/148)))
out.convert('RGB').save(p/'station-scale.png')
bounds=[im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for im in ims]
(p/'review.json').write_text(json.dumps({'rawSize':raw.size,'rawSha256':hashlib.sha256((p/'raw.png').read_bytes()).hexdigest(),'sourceCanvas':[256,256],'nativeAlpha128Bounds':bounds,'wholeCanvasScale':256/raw.width,'perPoseFit':False,'visualReviewPending':True,'selected':False,'sourceAcceptance':False,'scope':'One bare authored carrying midpoint; no helmet/motion/native/normal admission.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'rawSize':raw.size,'boundsSouthMidWest':bounds,'wholeCanvasScale':256/raw.width}))
