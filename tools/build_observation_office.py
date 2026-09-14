"""Preserve overhead desk/chair alpha and prepare a shared quarter-turn family."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/rooms/observation-room/pack'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-9b403aa5-63f5-4e60-9213-530a263a14d6.png')
shutil.copyfile(raw,PACK/'office-raw.png')
im=Image.open(raw).convert('RGBA');assert im.getpixel((0,0))[3]==0
im.putalpha(im.getchannel('A').point(lambda a:0 if a<16 else a))
split=round(im.width*.70);records={}
for name,region in [('wooden-desk',(0,0,split,im.height)),('chair-rear',(split,0,im.width,im.height))]:
    part=im.crop(region);box=part.getchannel('A').getbbox();part=part.crop(box);outputs={}
    for q,turn in [(0,None),(1,Image.Transpose.ROTATE_270),(2,Image.Transpose.ROTATE_180),(3,Image.Transpose.ROTATE_90)]:
        out=part if turn is None else part.transpose(turn);p=PACK/f'{name}-q{q}.png';out.save(p)
        outputs[q]={'size':out.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    records[name]={'region':region,'crop':box,'outputs':outputs}
(PACK/'office-build.json').write_text(json.dumps({'status':'prepared-not-selected','raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'processing':'native alpha, haze below16 removed, independent crops and exact turns','props':records},indent=2)+'\n')
print({name:entry['outputs'][0]['size'] for name,entry in records.items()})
