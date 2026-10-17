from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-low-support-v332';o.mkdir(exist_ok=True)
target=p/'north-unload-low-source-v314/raw.png'
source=r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png'
im=Image.open(source).convert('RGBA');ref=Image.new('RGBA',im.size);ref.paste(im.crop((0,208,256,224)),(0,208));ref.resize((1254,1254),Image.Resampling.NEAREST).save(o/'registered-boot-reference.png')
master=r/'character/branforth-west-direct-v2/master-input.png'
refs=[target,o/'registered-boot-reference.png',master]
(o/'inputs.json').write_text(json.dumps(dict(target=str(target.relative_to(r)),standingSource=str(source.relative_to(r)),standingSha256=hashlib.sha256(source.read_bytes()).hexdigest(),bootReferenceCrop=[0,208,256,224],refs=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in refs],normalChanged=False),indent=2)+'\n')
print('Frozen existing bent pose and exact standing-boot support reference.')
