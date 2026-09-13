"""Preserve generated alpha and prepare inward-facing overhead bench variants."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/construction-material-v2'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-2cd506d7-ee6b-4364-af82-21e5f72b54bf.png')
shutil.copyfile(raw,PACK/'bench-overhead-raw.png')
im=Image.open(raw).convert('RGBA')
assert im.getpixel((0,0))[3]==0
box=im.getchannel('A').getbbox(); im=im.crop(box)
outputs={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    image=im if turn is None else im.transpose(turn)
    p=PACK/f'bench-overhead-{facing}.png'; image.save(p)
    outputs[facing]={'size':image.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'bench-build.json').write_text(json.dumps({'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'alpha_crop':box,'processing':'existing alpha preserved; crop and exact quarter turns','outputs':outputs},indent=2)+'\n')
print(outputs)
