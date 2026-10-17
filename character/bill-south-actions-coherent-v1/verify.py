"""Validate staged south source registration, profile, endpoints and joins."""
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent


def main():
    manifest=json.loads((HERE/'manifest.json').read_text())
    hashes=json.loads((HERE/'frame-hashes.json').read_text())
    settings=json.loads((HERE/'build-settings.json').read_text())
    registration=json.loads((HERE/'source-registration.json').read_text())
    checks=0;frames={}
    assert manifest['pivot']==[128,224] and manifest['standingHeight']==148
    checks+=1
    for state in manifest['states']:
        assert len(state['frameFiles'])==len(state['frameDurationsMs'])==6
        assert state['frameDurationsMs']==settings['frameDurationsMs'][state['id']]
        checks+=2;frames[state['id']]=[]
        for rel in state['frameFiles']:
            im=Image.open(HERE/rel).convert('RGBA');a=np.asarray(im)
            assert im.size==(256,256)
            assert np.any(a[:,:,3]>180)
            assert not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3])
            assert hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==hashes[rel]
            checks+=4;frames[state['id']].append(im)
    idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(HERE.parent/'bill-shared-helmet-runtime-v2/frames/idle-south/000.png').convert('RGBA'),(36,52))
    for key,index in [('interact-south',0),('interact-south',5),('kneel-south',0),('stand-south',5)]:
        assert frames[key][index].tobytes()==idle.tobytes();checks+=1
    for a,b in [('kneel-south','repair-south'),('repair-south','stand-south')]:
        assert frames[a][5].tobytes()==frames[b][0].tobytes();checks+=1
    assert len(registration['frames'])==18;checks+=1
    assert registration['sourceSha256']==hashlib.sha256((HERE/'sources/actions.png').read_bytes()).hexdigest();checks+=1
    report={'checks':checks,'failures':0,'exportedFrames':24,'sourcePoses':18,'ownerAcceptance':'pending','runtimeInstalled':False}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
