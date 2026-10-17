from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
from scipy.ndimage import label
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
source=P/'generated-rear-heads.png';raw=Image.open(source).convert('RGBA');a=np.array(raw)
names=['rear-control-north','clean-bare-north-bow25','clean-bare-north-bow45','clean-bare-north-bow65','clean-bare-north-bow90','clean-bare-se-closed'];parts=[]
for i,name in enumerate(names):
 row,col=divmod(i,3);cell=(col*raw.width//3,row*raw.height//2,(col+1)*raw.width//3,(row+1)*raw.height//2);part=raw.crop(cell);arr=np.array(part)
 # Generated alpha contains a faint exterior brown glow. The recorded
 # opacity cutoff removes only that matte fringe, without changing RGB.
 opaque=arr[:,:,3]>240;labs,_=label(opaque,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;opaque=labs==int(sizes.argmax())
 arr[:,:,3]=np.where(opaque,255,0).astype('uint8');part=Image.fromarray(arr);box=part.getbbox();parts.append((name,part.crop(box),cell,box))
scale=28/parts[0][1].height;records=[];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);board=Image.new('RGBA',(900,430),'#252b2e');draw=ImageDraw.Draw(board)
for i,(name,part,cell,box) in enumerate(parts):
 size=tuple(round(v*scale) for v in part.size);head=part.resize(size,Image.Resampling.NEAREST);out=P/'sources'/(name+'-native.png');head.save(out)
 records.append({'name':name,'cell':cell,'alphaBox':box,'alphaMatteCutoff':240,'retainPrimaryConnectedAlphaComponent':True,'sourceSize':part.size,'uniformScale':scale,'nativeSize':size,'output':out.relative_to(P).as_posix(),'outputHash':hashlib.sha256(out.read_bytes()).hexdigest()})
 x=i%3*300+70;y=i//3*215+40;board.alpha_composite(head.resize((head.width*5,head.height*5),Image.Resampling.NEAREST),(x,y));draw.text((i%3*300+10,y-30),name.replace('clean-bare-',''),font=font,fill='white')
board.save(P/'rear-source-review.png');(P/'rear-extraction.json').write_text(json.dumps({'source':'generated-rear-heads.png','sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Four anatomically authored rear pitch variants, upright rear control and closed-eye front quarter; deterministic generated-alpha matte cleanup and one uniform scale established by upright calibration head. No RGB edits, no independent width/height fit.','records':records},indent=2)+'\n')
print(json.dumps({'scale':scale,'sources':{q['name']:q['nativeSize'] for q in records}}))
