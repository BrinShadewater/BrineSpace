from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'donor-bridge-v19'
files=[r/'character/james-carry-headcaps-v1/frames/004.png',out/'start-001.png',out/'start-002.png',p/'master-head-review-v16/bare-000.png']
gearhead=r/'character/james-carry-authored-helmet-v1/frames/004.png';master=Image.open(gearhead).convert('RGBA');groups=[];records=[]
for mode in ('bare','helmet'):
 bank=[]
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGBA')
  if mode=='helmet':im.paste(master.crop((102,62,155,110)),(102,62))
  bank.append(im);records.append({'mode':mode,'slot':i,'alpha128Bounds':im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()})
 groups.append(bank)
for kind,rect,scale in [('whole',(0,0,256,256),1),('body',(80,96,176,240),2)]:
 w=(rect[2]-rect[0])*scale;h=(rect[3]-rect[1])*scale;board=Image.new('RGBA',(4*w,2*(h+26)),(48,59,63,255));d=ImageDraw.Draw(board)
 for y,bank in enumerate(groups):
  for i,im in enumerate(bank):
   board.alpha_composite(im.crop(rect).resize((w,h),Image.Resampling.NEAREST),(i*w,y*(h+26)+26));d.text((i*w+3,y*(h+26)+7),('helmet ' if y else 'bare ')+['standing','pose1','pose2','walk0'][i],fill='white')
 board.convert('RGB').save(out/f'chain-{kind}.png')
report={'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files+[gearhead,Path(__file__)]},'records':records,'visualReviewPending':True,'sourceAcceptance':False,'selected':False,'scope':'Four ordered standalone source poses, paired with same-position standing helmet for comparison. No finite clip/native/runtime acceptance.'}
(out/'chain-review.json').write_text(json.dumps(report,indent=2)+'\n');print('Four-pose whole/body chain review prepared; no runtime adoption.')
