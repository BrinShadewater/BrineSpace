"""Key the overhead study and prepare exact directional turns; no runtime selection."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'assets/tidal-owner-v2'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-3ea5cfb6-f70d-4a5a-94a1-cfdd85b6e2bf.png')
shutil.copyfile(raw,PACK/'equipment-source-v2.png')
im=Image.open(raw).convert('RGBA')
pixels=im.load()
for y in range(im.height):
    for x in range(im.width):
        r,g,b,a=pixels[x,y]
        if min(r,b)-g>25 and r>g*1.3 and b>g*1.3:
            pixels[x,y]=(0,0,0,0)
record={'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'status':'prepared-not-selected','processing':'magenta key including pull-tab apertures; separate alpha crop; exact turns','props':{}}
for name,region in [('pump',(0,0,im.width//2,im.height)),('monitor',(im.width//2,0,im.width,im.height))]:
    part=im.crop(region)
    box=part.getchannel('A').getbbox()
    part=part.crop(box)
    outputs={}
    for facing,turn in [('down',None),('right',Image.Transpose.ROTATE_90),('up',Image.Transpose.ROTATE_180),('left',Image.Transpose.ROTATE_270)]:
        out=part if turn is None else part.transpose(turn)
        path=PACK/f'{name}-{facing}.png'
        out.save(path)
        outputs[facing]={'size':out.size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    record['props'][name]={'source_region':region,'alpha_crop':box,'outputs':outputs}
(PACK/'equipment-build.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v['outputs']['down']['size'] for k,v in record['props'].items()}))
