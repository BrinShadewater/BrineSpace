"""Prepare remaining edits with high-density whole refs at one physical profile."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slot in [s for s in range(48) if s not in [0,4,12,24,36]]:
 D=P/f'sequence-individual-{slot:03}-v2';D.mkdir(exist_ok=False)
 original=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png';a=np.asarray(Image.open(original).convert('RGBA'));y,x=np.where(a[:,:,3]>127);crown=int(y.min()*4);sole=int((y.max()+1)*4);width=int((x.max()-x.min()+1)*4)
 target=P/f'sequence-individual-{slot:03}-v1/edit-target.png';walk=P/'sequence-individual-004-v2/preferred-walk-reference.png';master=P/'original-master.png'
 refs=[dict(path=str(p),sha256=sha(p),source=str(original if p==target else p),sourceSha256=sha(original if p==target else p),role=role,canvas=list(Image.open(p).size)) for p,role in [(target,'Only exact original full pose edit target'),(walk,'Preferred walking material/identity, uniformly normalized whole1254to1024, not replacement pose'),(master,'Original master identity/material authority, matched physical reference profile')]]
 assert all(r['canvas']==[1024,1024] for r in refs)
 prompt=(P/f'sequence-individual-{slot:03}-v1/prompt.txt').read_text(encoding='utf-8')+f' All references use the same1024square physical figure profile. Match image1 crown y{crown}, sole y{sole}, occupied height{sole-crown}px and width{width}px on the supplied1024canvas; these describe the target, not a forced output resolution. Preserve image1 precise silhouette, posture, head scale and all limb lengths. Supporting figures must not dictate size, placement or pose. Image1 is geometric authority.'
 (D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
print('Prepared43 matched-profile phase edits; existing phase4v2 retained; no submission or normal-source mutation.')
