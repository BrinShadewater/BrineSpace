"""Keep exact raw01 and produce whole-cell own-West diagnostic packing."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'character/marsh-loaded-swim-material-v1/sources'
p=S/'west-loop-01.request.json';r=json.loads(p.read_text())
r.update(generationId='exec-fd5045a0-c705-4d01-83ff-14840725a9b1',originalGeneratedPath='C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-fd5045a0-c705-4d01-83ff-14840725a9b1.png',rawSha256=hashlib.sha256((S/'west-loop-01.raw.png').read_bytes()).hexdigest(),status='whole raw retained; own-West scale/visual/native review pending')
p.write_text(json.dumps(r,indent=2)+'\n')
s=(ROOT/'tools/pack_marsh_loaded_swim_material01.py').read_text().replace('east-loop-01','west-loop-01').replace('idle-east','idle-west')
s=s.replace('right_start=b[0]+round((b[2]-b[0])*.6)','right_start=b[0];left_stop=b[0]+round((b[2]-b[0])*.4)')
s=s.replace('aa[:,right_start:b[2]]','aa[:,right_start:left_stop]')
s=s.replace('offset=(163-b[2],108-int(ys.min()))','offset=(50-b[0],106-int(ys.min()))')
s=s.replace('case-right163 and forward-head top108','case-left50 and forward-head top106')
(ROOT/'tools/pack_marsh_loaded_swim_west01.py').write_text(s)
print('West original retained; one own-neutral scale and own-case-left diagnostic packer prepared.')
