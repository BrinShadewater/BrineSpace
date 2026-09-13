"""Prepare a coherent Tidal overhead inventory through exact turns."""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; PACK=ROOT/'assets/tidal-owner-v2'; REG=ROOT/'rooms/full-wall-v1/registrations'
raw=Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-e0e9783b-045e-4cbc-9853-b431d60dfcb1.png')
shutil.copyfile(raw,PACK/'source-v2.png')
a=np.array(Image.open(raw).convert('RGBA'));rgb=a[:,:,:3].astype(float)/255
a[np.minimum(rgb[:,:,0],rgb[:,:,2])-rgb[:,:,1]>.18,3]=0
im=Image.fromarray(a);im=im.crop(im.getchannel('A').getbbox());out={}
for direction,turn in [('north',None),('east',Image.Transpose.ROTATE_270),('south',Image.Transpose.ROTATE_180),('west',Image.Transpose.ROTATE_90)]:
    img=im if turn is None else im.transpose(turn); p=PACK/f'{direction}-overhead.png';img.save(p)
    name='tidal-condensation-wall.json' if direction=='north' else f'side-tidal-condensation-wall-{direction}.json'
    backup=PACK/(name+'.before')
    if not backup.exists():shutil.copyfile(REG/name,backup)
    w,h=img.size; digest=hashlib.sha256(p.read_bytes()).hexdigest()
    d={'source':'res://'+p.relative_to(ROOT).as_posix(),'sha256':digest,'region':[0,0,w,h],'pieces':[[[0,0],[w,0],[w,h],[0,h]]],'direction':direction,'wall_contact':{'side':direction,'purpose':'Fixed manifold outward; cartridge releases and keypad inward'},'method':'Overhead inventory repair; magenta key; exact turns'}
    (REG/name).write_text(json.dumps(d,indent=2)+'\n');out[direction]={'size':[w,h],'sha256':digest}
(PACK/'build.json').write_text(json.dumps({'status':'integrated candidate pending native review','directions':out,'inventory':'three coil returns, two vessels, three cartridges, one console'},indent=2)+'\n')
print(out)
