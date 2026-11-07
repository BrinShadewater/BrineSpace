"""Prepare overhead shelf art and architecture while retaining raw provenance."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/observation-room/pack'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-4e175a79-022c-4bbc-90d5-3f53cdba2c27.png')
shutil.copyfile(raw,PACK/'shelves-raw.png')
im=Image.open(raw).convert('RGBA');assert im.getpixel((0,0))[3]==0
im.putalpha(im.getchannel('A').point(lambda a:0 if a<16 else a))
box=im.getchannel('A').getbbox();im=im.crop(box)
outputs={}
for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
    out=im if turn is None else im.transpose(turn);p=PACK/f'shelves-{facing}.png';out.save(p)
    outputs[facing]={'size':out.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(PACK/'shelves-build.json').write_text(json.dumps({'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'crop':box,'processing':'native alpha, haze below16 removed, exact turns','outputs':outputs},indent=2)+'\n')
p=ROOT/'assets/room-risers-v2/registrations.json';d=json.loads(p.read_text());entry=d['observation_room']
backup=PACK/'riser-original-registration.json'
if not backup.exists():backup.write_text(json.dumps(entry,indent=2)+'\n')
assert list(Image.open(PACK/'riser.png').size)==entry['native_size']
entry.update(source='res://assets/rooms/observation-room/pack/riser.png',sha256=hashlib.sha256((PACK/'riser.png').read_bytes()).hexdigest(),stage='Architecture separation integrated; native review pending')
entry.pop('card',None);entry.pop('card_sha256',None)
p.write_text(json.dumps(d,indent=2)+'\n')
print(im.size)
