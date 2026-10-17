from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes());review=json.loads((p/'review.json').read_bytes())
for inventory in [inputs['preCallSha256'],review['currentLoaderReadSha256']]:assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inventory.items())
review.update(visualReviewPending=False,selected=False,sourceAcceptance=False,representativePoseDisposition='Provisionally viable bare South holding pose,not admitted animation bank',finding='Generated torso crop/all original-crop/full/master/current-carry/West/82/54/27boards inspected. Two-hand front case grip readable; belt wrench remains viewer-left and meter viewer-right, partly occluded by foreground arms/case.59802outside pixels exact: original selected head/lower body/boots,crown76/sole224 retained. No duplicate held tools observed. Detail/torso seams/tool occlusion need paired full-family/motion review; single static source not helmet/native/owner acceptance.')
(p/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print('South source review closed; frozen source/actual loader hashes stable; representative bare pose retained provisionally.')
