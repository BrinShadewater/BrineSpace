from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-full-set-review-2026-10-02/east-inspect-v23';out.mkdir(exist_ok=True)
inventory=r/'character/james-full-set-review-2026-10-02/source-inventory.json';data=json.loads(inventory.read_bytes());state=data['states']['bare']['inspect-east'];idle=data['states']['bare']['idle-east']
files=[inventory,Path(__file__)];sources=[r/idle['frameFiles'][0]]+[r/x for x in state['frameFiles']];files+=sources
samples=[0,35,60,65,70,75,80,105,140];box=(64,20,128,160);w=192;h=420
for page,indices in enumerate([samples[:5],samples[5:]]):
    board=Image.new('RGBA',(6*w,h+26),(48,59,63,255));draw=ImageDraw.Draw(board)
    for col,(f,label) in enumerate([(sources[0],'selected idle')]+[(sources[i+1],f'inspect {i}') for i in indices]):
        im=Image.open(f).convert('RGBA');assert im.size==(184,184)
        board.alpha_composite(im.crop(box).resize((w,h),Image.Resampling.NEAREST),(col*w,26));draw.text((col*w+3,7),label,fill='white')
    board.convert('RGB').save(out/f'detail-{page}.png')
records=[]
for i,f in enumerate(sources[1:]):
    a=np.array(Image.open(f).convert('RGBA')); head=a[20:60,64:108];body=a[60:110,64:98];record=dict(slot=i,source=f.relative_to(r).as_posix(),headRegionSha256=hashlib.sha256(head.tobytes()).hexdigest())
    for name,region in [('head',head),('body',body)]:
        solid=region[:,:,3]>=128;rgb=region[:,:,:3].astype(float)[solid]
        record[name+'MedianRgb']=np.median(rgb,axis=0).tolist();record[name+'MedianRBMinusG']=float(np.median((rgb[:,0]+rgb[:,2])/2-rgb[:,1]))
    records.append(record)
(out/'review.json').write_text(json.dumps(dict(sourceSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
    sampledIndices=samples,records=records,visualReviewPending=True,sourceAcceptance=False,
    scope='Fixed-region diagnostic only, not semantic face/fabric segmentation or proof of color defect. Enlarged nine source phases against exact same-pivot idle; no edits or fitting.'),indent=2)+'\n')
print(json.dumps(dict(sourceFrames=len(records),distinctHeadRegions=len(set(x['headRegionSha256'] for x in records)),boards=2,normalChanged=False)))
