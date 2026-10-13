"""Retain and whole-pack own South; resolve actual selected idle master."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-loaded-swim-material-v1/sources'
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-e7ba9892-3229-457b-bca0-39b2768fbe1b.png');raw=S/'south-loop-01.raw.png'
if not raw.exists():shutil.copy2(original,raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(raw)==sha(original)
p=S/'south-loop-01.request.json';r=json.loads(p.read_text());r.update(generationId=original.stem,originalGeneratedPath=original.as_posix(),rawSha256=sha(raw),status='whole South source retained; review pending; unselected');p.write_text(json.dumps(r,indent=2)+'\n')
s=(ROOT/'tools/pack_marsh_loaded_swim_west01.py').read_text().replace('west-loop-01','south-loop-01').replace('character/marsh-v2/frames/bare/idle-west/000.png',r['selectedIdleMaster']['path'])
start=s.index('        aa=np.array(dense)');end=s.index('    f=Image.new',start)
s=s[:start]+'''        offset=(round(112-(b[0]+b[2]-1)/2),178-b[3]);method='whole swim midpoint112 / leading case-bottom178; diagnostic only'
'''+s[end:]
p=ROOT/'tools/pack_marsh_loaded_swim_south01.py';p.write_text(s);exec(compile(s,str(p),'exec'))
