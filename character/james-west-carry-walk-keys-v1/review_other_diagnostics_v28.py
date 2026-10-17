from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-full-set-review-2026-10-02/diagnostics-v28';out.mkdir(exist_ok=True)
inventory=r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json';d=json.loads(inventory.read_bytes());files=[inventory,Path(__file__)];records=[]
for direction in ['south','north','west']:
 for mode in ['bare','helmet']:
  state=d['states'][mode]['inspect-'+direction];master=d['states'][mode]['idle-'+direction];n=state['frameCount'];indices=[round(j*(n-1)/8) for j in range(9)]
  sources=[(master,0,'idle master')]+[(state,i,'inspect '+str(i)) for i in indices]
  for kind,box,scale in [('whole',(0,0,256,256),1),('head',(80,60,180,160),2)]:
   w=(box[2]-box[0])*scale;h=(box[3]-box[1])*scale;board=Image.new('RGBA',(4*w,3*(h+24)),(48,59,63,255));draw=ImageDraw.Draw(board)
   for j,(s,i,label) in enumerate(sources):
    f=r/s['frameFiles'][i];files.append(f);im=Image.open(f).convert('RGBA');assert s['standingHeight']==148
    px,py=s['pivot'];assert px==int(px) and py==int(py);tile=Image.new('RGBA',(256,256));tile.paste(im,(128-int(px),224-int(py)))
    at=((j%4)*w,(j//4)*(h+24)+24);board.alpha_composite(tile.crop(box).resize((w,h),Image.Resampling.NEAREST),at);draw.text((at[0]+3,at[1]-19),label,fill='white')
    if kind=='whole':records.append(dict(direction=direction,mode=mode,slot=i,role='master' if j==0 else 'action',source=f.relative_to(r).as_posix(),canvas=list(im.size),pivot=s['pivot'],standingHeight=148))
   board.convert('RGB').save(out/f'{mode}-{direction}-{kind}.png')
(out/'review.json').write_text(json.dumps(dict(records=records,sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
    visualReviewPending=True,sourceAcceptance=False,normalChanged=False,scope='Nine distributed phases per three directions/two gears plus same-direction idle masters.60 prescribed slots; whole and enlarged upper-body boards. Static sample review only, no complete cycles/native/room acceptance.'),indent=2)+'\n')
print('Three directions/two gears prepared:60 source slots in12 fixed-pivot/ruler comparison boards.')
