"""Align support-reference physical density using established whole-canvas packing."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';archive=P/'reference-density-v1';archive.mkdir(exist_ok=False)
for name in ['original-master.png','detailed-donor.png','references.json']:shutil.copyfile(P/name,archive/name)
records=json.loads((P/'references.json').read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for record in records[1:]:
 source=Path(record['source']);common=Image.open(source).convert('RGBA').resize((352,352),Image.Resampling.LANCZOS);whole=common.crop((68,52,252,236));out=Image.new('RGBA',(256,256));out.paste(whole,(36,52));out.resize((1024,1024),Image.Resampling.NEAREST).save(record['path']);record['sha256']=sha(Path(record['path']));record['method']='Established uniform352canvas/crop184 profile; whole translation36,52 to256canvas, nearest4x. Same declared H148/p128224 as walk target; no bounding-box fit.'
(P/'references.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');print('Support references now share actual physicalH148/p128224 at4x; original loose canvas-density preparation archived.')
