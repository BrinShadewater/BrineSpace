"""Retain original reference density while matching the target physical profile."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';archive=P/'reference-density-v2';archive.mkdir(exist_ok=False)
for name in ['original-master.png','detailed-donor.png','references.json']:shutil.copyfile(P/name,archive/name)
records=json.loads((P/'references.json').read_text(encoding='utf-8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for record in records[1:]:
 common=Image.open(record['source']).convert('RGBA').resize((1408,1408),Image.Resampling.LANCZOS);whole=common.crop((272,208,1008,944));out=Image.new('RGBA',(1024,1024));out.paste(whole,(144,208));out.save(record['path']);record['sha256']=sha(Path(record['path']));record['method']='Whole high-density1408canvas (fourfold352profile), crop736 (fourfold184), translation144,208 to1024. PhysicalH148/p128224 at4x; no low-res intermediate or bounding-box fit.'
(P/'references.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8');print('Corrected support references retain high source density and matching physical profile; both preparation histories archived.')
