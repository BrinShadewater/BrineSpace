"""Validate source provenance, lossless packing and unchanged staged inputs."""
from pathlib import Path
import ast,json,hashlib,subprocess
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-reach-adjacent-motion-v2';OLD=R/'character/bill-east-reach-adjacent-motion-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
family=json.loads((P/'family-review.json').read_text(encoding='utf-8'))
assert all(sha(Path(p))==h for p,h in family['inputs'].items())
timeline=json.loads((P/'timeline.json').read_text(encoding='utf-8'));assert all(sha(R/p)==h for p,h in timeline['inputs'].items())
for folder in ['extension-003-v2','extension-register-003-v3','recovery-direct-004-v3']:
 D=OLD/folder;receipt=json.loads((D/'provenance.json').read_text(encoding='utf-8'))
 assert sha(Path(receipt['savedPath']))==receipt['rawSha256'] and sha(D/'prompt.txt')==receipt['promptSha256']
 assert all(sha(Path(ref['path']))==ref['sha256'] for ref in receipt['references'])
new=np.asarray(Image.open(OLD/'extension-register-003-v3/raw-003.png').convert('RGBA').resize((352,352),Image.Resampling.LANCZOS).crop((68,52,252,236)))
packed=np.asarray(Image.open(P/'frames/interact-east/003.png').convert('RGBA'));assert np.array_equal(packed[:-6],new[6:]) and not new[:6,:,3].any();assert np.count_nonzero(packed[:,:,3])==np.count_nonzero(new[:,:,3])
for slot in [0,1,2,5]:assert sha(P/f'frames/interact-east/{slot:03}.png')==sha(OLD/f'frames/interact-east/{slot:03}.png')
prior=np.asarray(Image.open(OLD/'frames/interact-east/003.png').convert('RGBA'));a=packed[88:,:,3]>127;b=prior[88:,:,3]>127
aligned_iou=float(np.count_nonzero(a&b)/np.count_nonzero(a|b))
for tool in ['build_bill_east_reach_adjacent_motion_v4.py','review_bill_extension_003_v2.py','review_bill_extension_register_v3.py','verify_bill_reach_stature_v2.py']:ast.parse((R/'tools'/tool).read_text(encoding='utf-8'))
pngs=list(P.rglob('*.png'))+list((OLD/'extension-003-v2').glob('*.png'))+list((OLD/'extension-register-003-v3').glob('*.png'))
result=subprocess.run(['git','check-attr','filter','--']+[p.relative_to(R).as_posix() for p in pngs],cwd=R,capture_output=True,text=True,check=True)
assert len(result.stdout.splitlines())==len(pngs) and all(x.endswith(': filter: lfs') for x in result.stdout.splitlines())
validation=dict(passed=True,sourceInputCount=len(family['inputs']),timelineSourceCount=len(timeline['inputs']),sourceChanges=[],losslessWholeShift=True,alignedExtensionLowerBodyIoU=aligned_iou,pythonSyntaxFiles=4,pngLfsCount=len(pngs),normalAdmission=False,nativeTested=False)
(P/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8');print(json.dumps(validation))
