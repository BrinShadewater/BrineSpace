"""Retry demonstrated phase4 failure with equally scaled whole support references."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=P/'sequence-individual-004-v2';D.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=P/'sequence-individual-004-v1/edit-target.png';shutil.copyfile(src,D/'edit-target.png')
walk=P/'stride-000-v1/raw-000.png';Image.open(walk).convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS).save(D/'preferred-walk-reference.png');shutil.copyfile(P/'original-master.png',D/'original-master.png')
refs=[]
for source,name,role in [(src,'edit-target.png','Only exact original phase4 edit target'),(walk,'preferred-walk-reference.png','Preferred whole gait rendering, uniformly normalized1254to1024 at matched physical profile, not a replacement pose'),(P/'original-master.png','original-master.png','Original master material/identity authority, matched physical profile')]:
 refs.append(dict(source=str(source),sourceSha256=sha(source),path=str(D/name),sha256=sha(D/name),role=role,canvas=list(Image.open(D/name).size)))
assert all(r['canvas']==[1024,1024] for r in refs)
prompt=(P/'sequence-individual-004-v1/prompt.txt').read_text(encoding='utf-8')+' All three supplied references now use the same1024-square canvas and physical figure scale. Match image1 crown y320 and sole y892 on that1024canvas (31.25% and87.109375% down). Preserve original occupied height572px and width400px; those coordinates refer to the supplied target, not a requested output resolution. Do not let the supporting figure dictate a new size, placement, stance or limb length. Image1 is geometric authority.'
(D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
print('Prepared phase4 v2: all three refs1024square, whole uniform support normalization only; earlier receipts retained.')
