"""Preserve native alpha and prepare overhead systems terminal turns."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/command-owner-v2'
raw=PACK/'systems-raw.png';im=Image.open(raw).convert('RGBA')
assert im.getpixel((0,0))[3]==0
im.putalpha(im.getchannel('A').point(lambda a:0 if a<16 else a))
box=im.getchannel('A').getbbox();im=im.crop(box)
outputs={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    out=im if turn is None else im.transpose(turn);p=PACK/f'systems-{facing}.png';out.save(p)
    outputs[facing]={'size':out.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'systems-build.json').write_text(json.dumps({'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'crop':box,'processing':'native alpha retained, haze below16 removed, exact quarter turns','outputs':outputs},indent=2)+'\n')
print(im.size)
