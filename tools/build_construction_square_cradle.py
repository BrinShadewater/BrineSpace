"""Build the broad support deck without replacing the rejected cradle study."""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; PACK=ROOT/'assets/rooms/construction-drone-bay/material'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-21e70154-5073-4bc2-97db-7ebc637bde8b.png')
shutil.copyfile(raw,PACK/'cradle-square-raw.png')
a=np.array(Image.open(raw).convert('RGBA')); a[a[:,:,3]<16,3]=0
im=Image.fromarray(a); box=im.getchannel('A').getbbox(); im=im.crop(box)
out={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    img=im if turn is None else im.transpose(turn)
    p=PACK/f'cradle-square-{facing}.png';img.save(p)
    out[facing]={'size':img.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'cradle-square-build.json').write_text(json.dumps({'crop':box,'directions':out,'status':'candidate'},indent=2)+'\n')
print(out)
