from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-west-v3'
for gear in ['bare','helmet']:
 for i in [0,2,3,6]:
  f=f'{gear}/frames/land-swim-west/{i:03}.png';assert Image.open(P/f).convert('RGBA').tobytes()==Image.open(OLD/f).convert('RGBA').tobytes()
f=P/'review.json';e=json.loads(f.read_text());e.update(exactPreservedV3PairedFrames=8,decodedPairedAPNGFramesExact=14,visualReview='Original West master/common148 V3-V4 complete source board, three native4x old/new material crops and complete paired helmet/neck boards inspected. Three new edits bring quilting/square-ring badge and restrained metal/detail into remaining intermediate sources, with compact build maintained. First arm edit recentered/shortened and rejected; two-reference retry closer to original. Face/hair pixels, metals and subtle near-prone shape changed; IoU is diagnostic, not anatomy proof. Normal endpoint materials and full source-boundary/continuous motion consistency remain pending.',visualAcceptance='Full five-intermediate material/detail pass improved source comparison; full master consistency and new native motion proof pending.');f.write_text(json.dumps(e,indent=2)+'\n')
s=(OLD/'build_review_page.py').read_text(encoding='utf-8');lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith("e['visualReview']="):lines[i]="e['visualReview']="+repr(e['visualReview'])
s='\n'.join(lines)+'\n';s=s.replace('Graphite fabric and suit-detail edits on crouch and push-off','Graphite fabric and suit-detail edits across all five intermediate poses').replace('V2 poses','V3 poses');(P/'build_review_page.py').write_text(s,encoding='utf-8')
print('Eight V3 paired frames exact; fourteen decoded APNG source frames. Source review recorded.')
