"""Prepare exact facing variants from the corrected overhead console study."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/command-owner-v2'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-652cd378-5779-49a2-a307-97306d88a6b4.png')
shutil.copyfile(raw,PACK/'equipment-v3.png')
im=Image.open(raw).convert('RGBA');pixels=im.load()
for y in range(im.height):
    for x in range(im.width):
        r,g,b,a=pixels[x,y]
        if min(r,b)-g>25 and r>g*1.3 and b>g*1.3:pixels[x,y]=(0,0,0,0)
record={'status':'prepared-not-selected','source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'processing':'magenta key including cable gaps; independent alpha crop; exact quarter turns','props':{}}
for name,region in [('table',(0,0,im.width//2,im.height)),('comms',(im.width//2,0,im.width,im.height))]:
    part=im.crop(region);box=part.getchannel('A').getbbox();part=part.crop(box)
    outputs={}
    for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
        out=part if turn is None else part.transpose(turn);p=PACK/f'{name}-{facing}.png';out.save(p)
        outputs[facing]={'size':out.size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    record['props'][name]={'region':region,'crop':box,'outputs':outputs}
(PACK/'equipment-build.json').write_text(json.dumps(record,indent=2)+'\n')
print({name:entry['outputs']['down']['size'] for name,entry in record['props'].items()})
