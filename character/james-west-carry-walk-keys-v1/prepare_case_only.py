from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];source=r/'character/james-carry-headcaps-v1/frames/004.png';Image.open(source).convert('RGBA').crop((96,132,120,150)).resize((192,144),Image.Resampling.LANCZOS).save(p/'case-only-reference.png')
(p/'case-only-reference.json').write_text(json.dumps({'source':source.relative_to(r).as_posix(),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'crop':[96,132,120,150],'scale':8,'role':'Partial case panel/latches/material only, not full object dimensions. Deliberately excludes screen fragment, torso seam and near full glove; target owns all belt-tool positions, hands and body.'},indent=2)+'\n',encoding='utf-8')
print('Future case-panel reference cropped to exclude belt-screen fragment; no artwork painted.')
