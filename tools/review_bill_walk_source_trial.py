"""Preserve whole source trials and compare identity/geometry without fitting."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=P/sys.argv[1];slot=int(sys.argv[2]);original=Path(sys.argv[3]);raw=D/f'raw-{slot:03}.png';assert not raw.exists();shutil.copyfile(original,raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if (D/'references.json').exists():refs=json.loads((D/'references.json').read_text(encoding='utf-8'))
else:
 target=P/'raw-024.png';refs=[dict(source=str(target),sourceSha256=sha(target),path=str(target),sha256=sha(target),role='only exact detailed stride24 edit target; head/neck posture repair')]
assert all(sha(Path(r['path']))==r['sha256'] and sha(Path(r['source']))==r['sourceSha256'] for r in refs)
receipt=dict(terminal=True,generationId=original.stem,originalPath=str(original),savedPath=str(raw),rawSha256=sha(raw),promptSha256=sha(D/'prompt.txt'),references=refs,normalAdmission=False)
(D/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
def packed(path):return Image.open(path).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)
before=Image.open(R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png').convert('RGBA');target=packed(refs[0]['path']);new=packed(raw);new.save(D/f'candidate-{slot:03}.png')
def bounds(im):
 y,x=np.where(np.asarray(im)[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
nb,ob,tb=bounds(new),bounds(before),bounds(target);a=np.asarray(new)[:,:,3]>127;b=np.asarray(before)[:,:,3]>127
report=dict(status='pending_visual_review',slot=slot,candidateBounds=nb,selectedBounds=ob,targetBounds=tb,boundsDelta=[x-y for x,y in zip(nb,ob)],selectedHeightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]),selectedSoleDelta=nb[3]-ob[3],targetHeightDelta=(nb[3]-nb[1])-(tb[3]-tb[1]),silhouetteIoU=float(np.count_nonzero(a&b)/np.count_nonzero(a|b)),normalAdmission=False,nativeTested=False,scope='Whole256canvas uniform packing, no per-part fitting/scaling/head splice/recolor or normal source edits. Single source study, not a full loop.')
board=Image.new('RGB',(1600,700),'#17252d');draw=ImageDraw.Draw(board)
for n,(label,im) in enumerate([('Selected stride'+str(slot),before),('Exact edit target',target),('New whole source',new),('Original master',packed(P/'original-master.png')),('Detailed idle/reach',packed(P/'detailed-donor.png'))]):
 body=im.resize((320,320),Image.Resampling.NEAREST);board.paste(body,(n*320,35),body);draw.text((n*320+10,12),label,fill='white');head=im.crop((100,66,160,126)).resize((240,240),Image.Resampling.NEAREST);board.paste(head,(n*320+40,440),head)
board.save(D/'comparison.png');(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
