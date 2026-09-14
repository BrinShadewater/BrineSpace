"""Prepare exact cradle turns with measured alpha-gap evidence."""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; PACK=ROOT/'assets/rooms/construction-drone-bay/material'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-4cbeabbe-88ec-495f-873e-42d80fdd02a7.png')
shutil.copyfile(raw,PACK/'cradle-overhead-raw.png')
a=np.array(Image.open(raw).convert('RGBA'))
assert a[550,390,3]<16 and a[550,950,3]<16
assert a[550,670,3]>=240
a[a[:,:,3]<16,3]=0
im=Image.fromarray(a); box=im.getchannel('A').getbbox(); im=im.crop(box)
outputs={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    img=im if turn is None else im.transpose(turn)
    p=PACK/f'cradle-overhead-{facing}.png'; img.save(p)
    outputs[facing]={'size':img.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'cradle-build.json').write_text(json.dumps({'status':'prepared; integration pending','alpha_crop':box,'gap_probes':[[390,550],[950,550]],'pad_probe':[670,550],'outputs':outputs},indent=2)+'\n')
print(outputs)
