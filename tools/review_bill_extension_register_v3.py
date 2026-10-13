"""Inspect whole-pose shoulder relaxation, preserving raw and explicit bounds."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil,sys,numpy as np
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-reach-adjacent-motion-v1';D=P/'extension-register-003-v3'
original=Path(sys.argv[1]);raw=D/'raw-003.png';assert not raw.exists();shutil.copyfile(original,raw)
target=P/'sources/raw-003.png';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
receipt=dict(terminal=True,generationId=original.stem,originalPath=str(original),savedPath=str(raw),rawSha256=sha(raw),promptSha256=sha(D/'prompt.txt'),references=[dict(path=str(target),role='existing complete extension, slight shoulder relaxation only',sha256=sha(target))],normalAdmission=False)
(D/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
def common(p):return Image.open(p).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS)
def bounds(im):
 y,x=np.where(np.asarray(im)[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
new=common(raw);old=common(target);a=np.asarray(new)[:,:,3]>127;b=np.asarray(old)[:,:,3]>127
outside=a.copy();outside[52:236,68:252]=False;nb,ob=bounds(new),bounds(old)
new.crop((68,52,252,236)).save(D/'candidate-003.png')
report=dict(status='pending_visual_review',candidateBounds=nb,targetBounds=ob,opaqueOverflow=int(outside.sum()),heightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]),soleDelta=nb[3]-ob[3],lowerBodyIoU=float(np.count_nonzero(a[140:]&b[140:])/np.count_nonzero(a[140:]|b[140:])),normalAdmission=False,nativeTested=False)
board=Image.new('RGB',(1200,670),'#17252d');draw=ImageDraw.Draw(board)
for i,(label,p) in enumerate([('Idle authority donor',R/'character/bill-east-idle-interact-joined-v1/head-consistency-pilot-v3/idle-edit-target.png'),('Existing extension',target),('Relaxed extension',raw),('Original master',R/'character/bill-east-idle-interact-joined-v1/head-consistency-pilot-v3/original-master.png')]):
 im=common(p);whole=im.crop((112,50,244,238)).resize((264,376),Image.Resampling.NEAREST);board.paste(whole,(i*300+15,35),whole)
 head=im.crop((126,67,188,120)).resize((248,212),Image.Resampling.NEAREST);board.paste(head,(i*300+15,430),head);draw.text((i*300+15,12),label,fill='white')
board.save(D/'comparison.png');(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
