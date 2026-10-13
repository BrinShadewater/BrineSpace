from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'character/marsh-cargo-held-material-v1/sources'
r=json.loads((S/'east-unload-01.request.json').read_text())
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-6127a987-1f8c-45b1-a92e-9e7aca541beb.png')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(S/'east-unload-01.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
raw=S/'east-unload-01.raw.png'
if raw.exists():assert sha(raw)==sha(original)
else:shutil.copy2(original,raw)
r.update(generationId='exec-6127a987-1f8c-45b1-a92e-9e7aca541beb',originalGeneratedPath=str(original),rawSha256=sha(raw),status='generated; original retained; packing and visual assessment pending',limits='All four exact reference versions viewed before generation. No normal admission, pickup/unload playback or full-set acceptance.')
(S/'east-unload-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'generationId':r['generationId'],'originalRetained':original.exists(),'sha256':r['rawSha256']}))
