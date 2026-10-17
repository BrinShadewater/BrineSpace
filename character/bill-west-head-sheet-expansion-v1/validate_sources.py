from pathlib import Path
import ast,json,hashlib,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
banks=[ROOT/'character/bill-west-head-sheet-trial-v1']+[p.parent for p in OUT.glob('group-*/generation-provenance-v1.json')]
bound={q['key']:q for q in [json.loads(p.read_text()) for p in (ROOT/'character/bill-west-master-head-repair-v1').glob('generation-provenance-*.json')] if q.get('derivedSheetPose')}
cells=0;bindings=0
for bank in banks:
 receipt=bank/'generation-provenance-v1.json';q=json.loads(receipt.read_text())
 assert sha(Path(q['promptFile']))==q['promptSha256']==q['submittedPromptSha256']
 assert sha(Path(q['savedPath']))==q['sha256']==sha(Path(q['originalPath']))
 for ref in q['references']:assert sha(Path(ref['path']))==ref['sha256']
 review=json.loads((bank/'review.json').read_text())
 assert sha(Path(review['masterComparisonPath']))==review['masterComparisonSha256']
 for pose in q['poses']:
  assert sha(Path(pose['sourcePath']))==pose['sourceSha256'];cells+=1;key=f"bare-walk-{pose['frame']:03}"
  j=bound.get(key)
  if j and j['sharedProvenancePath']==str(receipt):
   assert sha(receipt)==j['sharedProvenanceSha256']
   a=Image.open(bank/f"pose-{pose['frame']:03}-candidate.png").convert('RGBA');b=Image.open(ROOT/f'character/bill-west-master-head-repair-v1/{key}-candidate.png').convert('RGBA')
   assert a.tobytes()==b.tobytes();bindings+=1
scripts=[OUT/'build_group_review.py',Path(__file__)]+list((ROOT/'character/bill-west-head-sheet-trial-v1').glob('*.py'))
for p in scripts:ast.parse(p.read_text(encoding='utf-8'))
pngs=[p for bank in banks for p in bank.rglob('*.png')];names=[p.relative_to(ROOT).as_posix() for p in pngs]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],cwd=ROOT,input=('\0'.join(names)+'\0').encode(),capture_output=True,check=True).stdout.decode().split('\0')
assert all(attrs[i+2]=='lfs' for i in range(0,len(attrs)-1,3))
report={'sharedGenerationCalls':len(banks),'explicitSourceCells':cells,'exactBoundCandidatePixels':bindings,'pythonSyntaxChecks':len(scripts),'pngLfsChecks':len(pngs),'normalAdmission':False,'nativeRun':False,'fullVisualAcceptance':False}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
