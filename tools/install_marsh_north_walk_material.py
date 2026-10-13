"""Admit only reviewed six-pose North gait; keep the new start staged."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-walk-material-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    baseline=json.loads((BASE/'baseline.json').read_text())['states']
    recipe=json.loads((BASE/'candidate-01/recipe.json').read_text())
    files=[]
    for slot,record in enumerate(recipe['frames']):
        path=BASE/f'candidate-01/{slot:03d}.png'
        assert sha(path)==record['candidateSha256']
        assert np.array_equal(np.array(Image.open(path))[:,:,3],np.array(Image.open(ROOT/record['source']))[:,:,3])
        files.append(path.relative_to(ROOT).as_posix())
    catpath=ROOT/'character/marsh-v2/catalog.json';catalog=json.loads(catpath.read_text())
    relative='../marsh-north-walk-material-v1/candidate-01/manifest.json'
    if relative not in catalog['body']:catalog['body'].append(relative)
    catpath.write_text(json.dumps(catalog,indent=2)+'\n')
    selected={'changedStates':['walk-north'],'states':{'walk-north':files},'scope':'Installed North gait material/detail; all original motion/timing/alpha retained; North start unselected','sourceRecipeSha256':sha(BASE/'candidate-01/recipe.json')}
    (BASE/'selection.json').write_text(json.dumps(selected,indent=2)+'\n')
    # Resolve every current state independently; don't rewrite dated closeout snapshots.
    current={}
    for path in catalog['body']:
        manifest=ROOT/'character/marsh-v2'/path;data=json.loads(manifest.read_text())
        for s in data['states']:
            paths=[(manifest.parent/f).resolve().relative_to(ROOT).as_posix() for f in s['frameFiles']]
            current[s['id']]={'files':paths,'hashes':[sha(ROOT/f) for f in paths],'durations':s['frameDurationsMs'],'loop':s['loop'],'pivot':data['pivot'],'standingHeight':data.get('standingHeight',148)}
    current={k:v for k,v in current.items() if not k.startswith(('equip-helmet-','remove-helmet-'))}
    assert set(current)==set(baseline)
    for key,old in baseline.items():
        if key=='walk-north':assert {k:v for k,v in current[key].items() if k not in ('files','hashes')}=={k:v for k,v in old.items() if k not in ('files','hashes')}
        else:assert current[key]==old,(key,'unrelated selection changed')
    (ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').write_text(json.dumps({'states':current},indent=2)+'\n')
    print('Installed walk-north6poses;203 unrelated states/1052 slots unchanged;start stays staged')
if __name__=='__main__':main()
