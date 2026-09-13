"""Clean and orient the generated flat panel-storage companion."""
import json, shutil, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/construction-material-v2'
RAW=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-858fa118-98e0-425e-9584-ca53609ab2db.png')
shutil.copyfile(RAW,PACK/'panel-pallet-raw.png')
shutil.copyfile(Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-9f337696-ca16-420f-81d6-cc6e83053ed5.png'),PACK/'panel-rack-rejected-elevation.png')
a=np.array(Image.open(RAW).convert('RGBA'))
rgb=a[:,:,:3].astype(float)/255
key=np.minimum(rgb[:,:,0],rgb[:,:,2])-rgb[:,:,1]>.18
a[key,3]=0
im=Image.fromarray(a); im=im.crop(im.getchannel('A').getbbox())
out={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    img=im if turn is None else im.transpose(turn)
    p=PACK/f'panel-pallet-{facing}.png'; img.save(p)
    out[facing]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':img.size}
(PACK/'panel-build.json').write_text(json.dumps({'directions':out,'keyed_pixels':int(key.sum()),'rejected':'First edit retained tall plate faces; use flat storage companion.'},indent=2)+'\n')
print(out)
