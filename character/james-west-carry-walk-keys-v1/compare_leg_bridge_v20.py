from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'leg-bridge-v20'
files=[r/'character/james-carry-headcaps-v1/frames/004.png',out/'candidate.png',p/'master-head-review-v16/bare-000.png']
head=r/'character/james-carry-authored-helmet-v1/frames/004.png';helmet=Image.open(head).convert('RGBA')
groups=[];records=[]
for mode in ('bare','helmet'):
    bank=[]
    for i,f in enumerate(files):
        im=Image.open(f).convert('RGBA')
        if mode=='helmet':im.paste(helmet.crop((102,62,155,110)),(102,62))
        bank.append(im)
        records.append(dict(mode=mode,slot=i,alpha128Bounds=im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()))
    groups.append(bank)
for kind,rect,scale in [('whole',(0,0,256,256),1),('body',(80,96,176,240),2)]:
    w=(rect[2]-rect[0])*scale;h=(rect[3]-rect[1])*scale
    board=Image.new('RGBA',(3*w,2*(h+26)),(48,59,63,255));draw=ImageDraw.Draw(board)
    for row,bank in enumerate(groups):
        for i,im in enumerate(bank):
            board.alpha_composite(im.crop(rect).resize((w,h),Image.Resampling.NEAREST),(i*w,row*(h+26)+26))
            draw.text((i*w+3,row*(h+26)+7),('helmet ' if row else 'bare ')+['standing','leg trial','walk0'][i],fill='white')
    board.convert('RGB').save(out/f'chain-{kind}.png')
report=dict(sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files+[head,Path(__file__)]},
    records=records,visualReviewPending=True,sourceAcceptance=False,selected=False,
    scope='Three-pose source comparison at identical pivot/ruler. No finite timing or runtime adoption. Helmet head copied solely for paired comparison.')
(out/'chain-review.json').write_text(json.dumps(report,indent=2)+'\n')
print('Paired standing/lower-body-trial/walk0 source boards prepared.')
