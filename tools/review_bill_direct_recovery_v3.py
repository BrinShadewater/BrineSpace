"""Preserve and measure a direct whole-pose recovery edit without anatomy fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1]
P=R/'character/bill-east-reach-adjacent-motion-v1'
D=P/'recovery-direct-004-v3'
original=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f/exec-6a2d312f-0298-47dd-b737-de1423a9a7bf.png')
raw=D/'raw-004.png';assert not raw.exists();shutil.copyfile(original,raw)
target=P/'sources/raw-001.png'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=dict(terminal=True,generationId=original.stem,originalPath=str(original),savedPath=str(raw),rawSha256=sha(raw),promptSha256=sha(D/'prompt.txt'),references=[dict(path=str(target),role='exact first reach edit target',sha256=sha(target))],normalAdmission=False)
(D/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
def common(p):return Image.open(p).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
def bounds(im):
    y,x=np.where(np.asarray(im)[:,:,3]>127)
    return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
new=common(raw);donor=common(target);old=common(P/'recovery-004-v2/raw-004.png')
a=np.asarray(new)[:,:,3]>127;b=np.asarray(donor)[:,:,3]>127
outside=a.copy();outside[52:236,68:252]=False
new.crop((68,52,252,236)).save(D/'candidate-004.png')
nb,db=bounds(new),bounds(donor)
report=dict(status='pending_visual_review',candidateBounds=nb,donorBounds=db,previousRecoveryBounds=bounds(old),crownDelta=nb[1]-db[1],soleDelta=nb[3]-db[3],heightDelta=(nb[3]-nb[1])-(db[3]-db[1]),opaqueOverflow=int(outside.sum()),lowerBodyIoU=float(np.count_nonzero(a[140:]&b[140:])/np.count_nonzero(a[140:]|b[140:])),normalAdmission=False,nativeTested=False)
board=Image.new('RGB',(1200,670),'#17252d');draw=ImageDraw.Draw(board)
master=common(R/'character/bill-east-idle-interact-joined-v1/head-consistency-pilot-v3/original-master.png')
for i,(label,im) in enumerate([('First reach donor',donor),('Prior recovery',old),('Direct recovery',new),('Original master',master)]):
    whole=im.crop((112,50,244,238)).resize((264,376),Image.Resampling.NEAREST)
    board.paste(whole,(i*300+15,35),whole)
    head=im.crop((126,67,188,120)).resize((248,212),Image.Resampling.NEAREST)
    board.paste(head,(i*300+15,430),head);draw.text((i*300+15,12),label,fill='white')
board.save(D/'comparison.png')
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
