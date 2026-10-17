from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];donor=r/'character/crew-runtime-matte-v1/branforth/frames/walk-west-tone-lock-v1'
board=Image.new('RGBA',(1024,564),(48,59,63,255));d=ImageDraw.Draw(board);ims=[];files=[]
for i,index in enumerate((0,48)):
    file=donor/f'{index:03}.png';files.append(file);im=Image.open(file).convert('RGBA');assert im.size==(184,184)
    base=Image.new('RGBA',(256,256));base.paste(im,(36,52));ims.append(base)
    board.alpha_composite(base.resize((512,512),Image.Resampling.NEAREST),(i*512,52));d.text((i*512+8,10),f'actual walk{index}: translation only, fixed148ruler',fill='white')
board.convert('RGB').save(p/'donor-endpoint-comparison.png')
diff=np.any(np.array(ims[0])!=np.array(ims[1]),axis=2)
report={'sourceSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'differentPixels':int(diff.sum()),'headAbove104Different':int(diff[:104].sum()),'legsBelow169Different':int(diff[169:].sum()),'rgbaEqual':not bool(diff.any()),'visualReviewPending':True,'scope':'Two actual selected donor sources, no duplicate-endpoint assumption or carrying-loop acceptance.'}
(p/'donor-endpoint-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='sourceSha256'}))
