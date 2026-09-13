"""Remove negligible alpha haze and register exact hatch quarter turns."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; PACK=ROOT/'assets/construction-material-v2'
a=np.array(Image.open(PACK/'hatch-overhead-raw.png').convert('RGBA'))
a[a[:,:,3]<16,3]=0
im=Image.fromarray(a); box=im.getchannel('A').getbbox(); im=im.crop(box)
assert im.size==(959,993)
out={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    img=im if turn is None else im.transpose(turn)
    p=PACK/f'hatch-overhead-{facing}.png'; img.save(p)
    out[facing]={'size':img.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'hatch-build.json').write_text(json.dumps({'crop':box,'alpha_threshold':16,'lid_center_source':[627,599],'aperture_radius_source':320,'directions':out},indent=2)+'\n')
print('Hatch alpha haze removed; four directions registered.')
