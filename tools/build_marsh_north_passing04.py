"""Retain passing04 provenance and reuse the complete two-cell packager."""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-north-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
gid='exec-93a3e4e6-3c34-4012-99e9-2877ff98db8d'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96')/(gid+'.png')
raw=S/'passing-04.raw.png';shutil.copy2(original,raw)
p=S/'passing-04.request.json';r=json.loads(p.read_text())
assert sha(S/'passing-04.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+[r['poseSourceFrame']]:assert sha(ROOT/q['path'])==q['sha256']
r.update(generationId=gid,originalGeneratedPath=str(original),rawSha256=sha(raw),status='Retained unselected: correct right support and both passing elbows at waist; sole clearance still stronger than requested')
p.write_text(json.dumps(r,indent=2)+'\n')
source=(ROOT/'tools/build_marsh_north_passing03.py').read_text().replace('passing-03','passing-04').replace('Arms remain asymmetrical like contact reference, left knee/sole lift stronger than requested.','Both elbows now bent at waist for passing. Left sole lift remains stronger than requested; compare full cycle.')
exec(compile(source,str(ROOT/'tools/build_marsh_north_passing04.py'),'exec'),{'__file__':str(ROOT/'tools/build_marsh_north_passing04.py'),'__name__':'__main__'})
