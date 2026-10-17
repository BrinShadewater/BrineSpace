from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'lower-inputs.json').read_bytes());assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
base=Image.open(p/'midpoint.png').convert('RGBA');raw=Image.open(p/'lower-raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((80,80),Image.Resampling.LANCZOS);crop.save(p/'lower-native.png')
rect=tuple(inputs['admissionRegion']);out=base.copy();out.paste(crop.crop((rect[0]-88,rect[1]-152,rect[2]-88,rect[3]-152)),rect[:2]);out.save(p/'midpoint-lower-v2.png')
originalOutside=base.copy();newOutside=out.copy()
for im in [originalOutside,newOutside]:im.paste((0,0,0,0),rect)
assert originalOutside.tobytes()==newOutside.tobytes()
ims=[Image.open(r/'character/james-south-master-carry-v1/carry-pose.png').convert('RGBA'),base,out,Image.open(r/'character/james-west-master-carry-v1/local-v3-carry-pose.png').convert('RGBA')]
labels=['South reference','midpoint v1 short','lower repair v2','West reference']
def board(name,crops,scale):
    w=crops[0].width*scale;h=crops[0].height*scale;im=Image.new('RGBA',(4*w,h+26),(48,59,63,255));d=ImageDraw.Draw(im)
    for i,(item,label) in enumerate(zip(crops,labels)):
        im.alpha_composite(item.resize((w,h),Image.Resampling.NEAREST),(i*w,26));d.text((i*w+5,7),label,fill='white')
    im.convert('RGB').save(p/name)
board('lower-whole-comparison.png',ims,2)
board('lower-detail-comparison.png',[im.crop((88,160,168,232)) for im in ims],5)
im=Image.new('RGBA',(860,320),(48,59,63,255));d=ImageDraw.Draw(im)
for row,height in enumerate([82,54,27]):
    d.text((5,row*106+7),f'{height}px standing ruler',fill='white')
    for i,item in enumerate(ims):
        sz=round(256*height/148);im.alpha_composite(item.resize((sz,sz),Image.Resampling.LANCZOS),(180+i*160-sz//2,row*106+96-round(224*height/148)))
im.convert('RGB').save(p/'lower-station-scale.png')
bounds=[im.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox() for im in ims]
report={'rawSize':raw.size,'rawSha256':hashlib.sha256((p/'lower-raw.png').read_bytes()).hexdigest(),'admissionRegion':rect,'protectedOriginalPixels':256*256-(rect[2]-rect[0])*(rect[3]-rect[1]),'protectedOutsideExact':True,'nativeAlpha128BoundsSouthV1V2West':bounds,'wholeCanvasScale':80/raw.width,'perPoseFit':False,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Localized generated lower-shin length source repair, all upper pose and knee pixels outside region exact; not paired animation/native acceptance.'}
(p/'lower-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'bounds':bounds,'protected':report['protectedOriginalPixels']}))
