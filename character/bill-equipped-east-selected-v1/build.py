"""Freeze accepted equipped east actions plus matching idle/walk shell grade."""
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
IDLE_WALK = ROOT/'bill-shared-helmet-east-matte-v1'
ACTIONS = ROOT/'bill-east-actions-coherent-v5'


def main():
    base = json.loads((IDLE_WALK/'manifest.json').read_text())
    anchors = json.loads((IDLE_WALK/'checks.json').read_text())
    result = {k:v for k,v in base.items() if k != 'states'}
    result.update(name='Bill accepted equipped east revision', status='owner_visual_accepted_2026_09_29',states=[])
    hashes = {}
    for source in [IDLE_WALK,ACTIONS]:
        manifest = json.loads((source/'manifest.json').read_text())
        for state in manifest['states']:
            state = copy.deepcopy(state)
            key = state['id']
            files = []
            for i,rel in enumerate(state['frameFiles']):
                im = Image.open(source/rel).convert('RGBA')
                if source == IDLE_WALK:
                    tx,ty = anchors[key][i]['template']
                    a = np.asarray(im).copy()
                    yy,xx = np.indices((184,184))
                    xx = xx-(tx-75)
                    yy = yy-(ty-25)
                    rgb = a[:,:,:3].astype(float)
                    shell = (yy<51)&(a[:,:,3]>0)&(rgb.mean(2)<85)
                    shell &= ~((xx>=89)&(yy>=30))
                    shell &= ~((xx>=99)&(yy<29))
                    a[shell,:3] = np.clip(rgb[shell]*0.92,0,255).astype('uint8')
                    im = Image.fromarray(a)
                dest = HERE/'frames'/key/f'{i:03d}.png'
                dest.parent.mkdir(parents=True,exist_ok=True)
                im.save(dest)
                relative = dest.relative_to(HERE).as_posix()
                files.append(relative)
                hashes[relative] = hashlib.sha256(dest.read_bytes()).hexdigest()
            state['frameFiles'] = files
            state['provenance'] = 'selected matte east idle/walk plus approved v5 equipped actions; matching 8 percent shell grade'
            result['states'].append(state)
    (HERE/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
    lookup = {s['id']:s for s in result['states']}
    idle = Image.open(HERE/lookup['idle-east']['frameFiles'][0]).tobytes()
    for key,i in [('interact-east',0),('interact-east',5),('kneel-east',0),('stand-east',5)]:
        assert Image.open(HERE/lookup[key]['frameFiles'][i]).tobytes()==idle
    print(f'Selected equipped east: {len(hashes)} frames, six states, exact idle endpoints')


if __name__ == '__main__':
    main()
