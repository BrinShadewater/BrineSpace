"""Retain whole generated source and pack all figures with one neutral ruler."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-loaded-swim-material-v1/sources'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-c659329f-8f4c-4e57-881a-e600dbca1c20.png')
raw=S/'north-loop-03.raw.png'
if not raw.exists():shutil.copy2(original,raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(raw)==sha(original)
p=S/'north-loop-03.request.json';r=json.loads(p.read_text());r.update(generationId=original.stem,originalGeneratedPath=original.as_posix(),rawSha256=sha(raw),status='whole source retained; scale/camera review pending; unselected')
p.write_text(json.dumps(r,indent=2)+'\n')
s=(ROOT/'tools/pack_marsh_loaded_swim_west01.py').read_text().replace('west-loop-01','north-loop-03').replace('idle-west','idle-north').replace('147/','146/').replace('neutral147','neutral146').replace("'neutralTargetHeight':147","'neutralTargetHeight':146")
start=s.index('        aa=np.array(dense)');end=s.index("    f=Image.new",start)
s=s[:start]+'''        offset=(round(112-(b[0]+b[2]-1)/2),105-b[1]);method='whole swim midpoint112 / top105; diagnostic only'
'''+s[end:]
p=ROOT/'tools/pack_marsh_loaded_swim_north03.py';p.write_text(s)
exec(compile(s,str(p),'exec'))
