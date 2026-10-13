"""Preserve and inspect one master-guided whole stride revision."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';original=Path('C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f/exec-73ef655c-2404-4bca-905d-d17ea95e929f.png');raw=P/'raw-024.png';assert not raw.exists();shutil.copyfile(original,raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();refs=json.loads((P/'references.json').read_text(encoding='utf-8'));assert all(sha(Path(r['source']))==r['sourceSha256'] and sha(Path(r['path']))==r['sha256'] for r in refs)
receipt=dict(terminal=True,generationId=original.stem,originalPath=str(original),savedPath=str(raw),rawSha256=sha(raw),promptSha256=sha(P/'prompt.txt'),references=refs,normalAdmission=False)
(P/'provenance.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
before=Image.open(refs[0]['source']).convert('RGBA');new=Image.open(raw).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);new.save(P/'candidate-024.png')
def bounds(im):
 y,x=np.where(np.asarray(im)[:,:,3]>127);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
a=np.asarray(new)[:,:,3]>127;b=np.asarray(before)[:,:,3]>127;nb,ob=bounds(new),bounds(before)
report=dict(status='pending_visual_review',targetBounds=ob,candidateBounds=nb,boundsDelta=[x-y for x,y in zip(nb,ob)],heightDelta=(nb[3]-nb[1])-(ob[3]-ob[1]),soleDelta=nb[3]-ob[3],silhouetteIoU=float(np.count_nonzero(a&b)/np.count_nonzero(a|b)),normalAdmission=False,nativeTested=False,scope='One full walk pose24 of48, raw whole uniform256resampling only. No anatomy fitting/registration/part splice/recolor. Geometry and material review separate from full sequence acceptance.')
board=Image.new('RGB',(1600,760),'#17252d');draw=ImageDraw.Draw(board)
for i,(label,im) in enumerate([('Selected stride24',before),('Master-guided stride24',new),('Original master reference',Image.open(P/'original-master.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS)),('Detailed idle/reach donor',Image.open(P/'detailed-donor.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS))]):
 view=im.resize((384,384),Image.Resampling.NEAREST);board.paste(view,(i*400+8,36),view);draw.text((i*400+10,12),label,fill='white')
 head=im.crop((100,66,160,126)).resize((240,240),Image.Resampling.NEAREST);board.paste(head,(i*400+70,490),head)
board.save(P/'comparison.png');(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
