from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'manifest.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());settings=json.loads((HERE/'build-settings.json').read_text());checks=0
for state in pack['states']:
    assert len(state['frameFiles'])==12 and not state['loop'];checks+=1
    assert state['frameDurationsMs']==settings['frameDurationsMs'][state['id']];checks+=1
    assert state['events'][0]['id']==('take-helmet-from-locker' if state['id']=='equip-helmet-east' else 'release-helmet-to-locker');checks+=1
    for rel in state['frameFiles']:
        a=np.asarray(Image.open(HERE/rel).convert('RGBA'))
        assert a.shape==(256,256,4);checks+=1
        assert a[:,:,3].max()>180 and not a[[0,-1],:,3].any() and not a[:,[0,-1],3].any();checks+=1
        assert hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==hashes[rel];checks+=1
rows={s['id']:[Image.open(HERE/f).convert('RGBA').tobytes() for f in s['frameFiles']] for s in pack['states']}
for i in range(12):assert rows['equip-helmet-east'][i]==rows['remove-helmet-east'][11-i];checks+=1
for path,key,index in [(settings['referenceBare'],'equip-helmet-east',0),(settings['referenceEquipped'],'equip-helmet-east',11),(settings['referenceEquipped'],'remove-helmet-east',0),(settings['referenceBare'],'remove-helmet-east',11)]:
    im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(HERE.parent.parent/path).convert('RGBA'),(36,52));assert im.tobytes()==rows[key][index];checks+=1
report={'checks':checks,'failures':0,'sourcePoses':12,'frameReferences':24,'removal':'reverse authored fitting','ownerVisualReview':'pending'}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
