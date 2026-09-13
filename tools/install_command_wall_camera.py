"""Clean exterior white and select camera-corrected wall sources at original scale."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
import numpy as np
ROOT=Path(__file__).resolve().parents[1];PACK=ROOT/'assets/command-owner-v2'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-7b530842-9d7b-4afd-beaf-b32626b38b1c.png')
shutil.copyfile(raw,PACK/'wall-north-v2.png')
records={}
for name,file in [('north','wall-north-v2.png'),('sides','wall-sides.png')]:
    im=Image.open(PACK/file).convert('RGBA');a=np.array(im)
    rgb=a[:,:,:3].astype(int)
    mask=Image.fromarray(((rgb.min(2)>=210)&((rgb.max(2)-rgb.min(2))<=25)).astype('uint8'))
    ImageDraw.floodfill(mask,(0,0),2)
    # Source backgrounds can have isolated white pockets behind mounting feet.
    # These command sources have no authored white equipment surfaces.
    exterior=np.array(mask)>0;a[exterior]=0
    target=PACK/f'wall-{name}-clean.png';Image.fromarray(a).save(target)
    old=ROOT/f'assets/command-directional-v1/command-{name}.png'
    assert Image.open(old).size==im.size
    paths=[]
    for p in (ROOT/'rooms/full-wall-v1/registrations').glob('command-wall-*.json'):
        d=json.loads(p.read_text())
        if d.get('source') not in [f'res://assets/command-directional-v1/command-{name}.png',f'res://assets/command-owner-v2/wall-{name}-clean.png']:continue
        backup=PACK/(p.name+'.before')
        if not backup.exists():shutil.copyfile(p,backup)
        d['source']=f'res://assets/command-owner-v2/wall-{name}-clean.png'
        d['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        d['method']='Camera correction with border-connected neutral alpha cleanup; original scale and registration frames preserved'
        p.write_text(json.dumps(d,separators=(',',':'))+'\n');paths.append(p.name)
    records[name]={'size':im.size,'exterior_pixels':int(exterior.sum()),'registrations':paths,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
(PACK/'wall-camera-build.json').write_text(json.dumps(records,indent=2)+'\n')
print({k:len(v['registrations']) for k,v in records.items()})
