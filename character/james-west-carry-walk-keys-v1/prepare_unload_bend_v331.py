from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-bend-anchor-v331';o.mkdir(exist_ok=True)
source=r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png';master=r/'character/branforth-west-direct-v2/master-input.png'
Image.open(source).convert('RGBA').resize((1254,1254),Image.Resampling.NEAREST).save(o/'edit-target.png')
refs=[o/'edit-target.png',master]
(o/'inputs.json').write_text(json.dumps(dict(referenceSource=str(source.relative_to(r)),referenceSourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),refs=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in refs],normalChanged=False),indent=2)+'\n')
print('Frozen whole-source rear-view bend anchor inputs.')
