from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-west-v2'
unchanged=[]
for gear in ['bare','helmet']:
 for i in [0,1,4,5,6]:
  f=f'{gear}/frames/land-swim-west/{i:03}.png'
  assert Image.open(P/f).convert('RGBA').tobytes()==Image.open(OLD/f).convert('RGBA').tobytes()
  unchanged.append(f)
frozen=json.loads((P.parent/'bill-land-water-material-west-v1/targeted-inputs.json').read_text())
bank={k:v for k,v in frozen.items() if k.startswith('character/bill-land-water-west-v2/')}
assert len(bank)==16
assert all(hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in bank.items())
e=json.loads((P/'review.json').read_text())
e.update(exactUnchangedV2Frames=unchanged,previousNativeV2SourceInputsStable=16,decodedAPNGFramesExactBothGears=14,visualReview='Original master/right West figure, complete V2/V3 common148 comparison, before/after native4x material crops and all fourteen bare/helmet neck crops inspected. New crouch/push have more neutral graphite quilting, worn metal detail and square/ring shoulder badges, with compact two-hand poses retained. Metals are brighter; face/hair pixels regenerated. Other three intermediate poses and walking/equipped endpoint material differences remain; no complete family grade/master identity or continuous motion acceptance.',visualAcceptance='Two source detail/material corrections improved; whole family and new bank native proof pending.')
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n')
s=(OLD/'build_review_page.py').read_text()
review="Full paired source board and fourteen head/collar crops reviewed. New graphite quilting and square/ring badges on crouch/push; canonical helmet remains unchanged. Other poses, brighter metal, head identity, walking endpoint material shift and continuous native motion remain pending. Connected alpha is not anatomy/motion acceptance."
lines=s.splitlines()
for i,line in enumerate(lines):
 if line.startswith("e['visualReview']="):lines[i]="e['visualReview']="+repr(review)
s='\n'.join(lines)+'\n'
s=s.replace('Compact crouch and push-off, paired with Bill’s established West helmet.','Graphite fabric and suit-detail edits on crouch and push-off, paired with Bill’s established West helmet.')
s=s.replace('Compare against the original master and earlier poses','Compare against the original master and V2 poses')
s=s.replace('<img src="master-comparison.png"><img src="paired-helmet-review.png">','<img src="master-comparison.png"><img src="material-detail-comparison.png"><img src="paired-helmet-review.png">')
(P/'build_review_page.py').write_text(s,encoding='utf-8')
print(json.dumps({'unchangedPairedFrames':10,'previousNativeBankInputsStable':16,'decodedPairedAPNGFramesExact':14,'newNativeProof':False}))
