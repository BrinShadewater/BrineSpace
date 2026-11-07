"""Select polished North step and refresh only the source contract, not art batches."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def install():
    p=ROOT/'character/marsh-v2/catalog.json';catalog=json.loads(p.read_text())
    relative='../marsh-north-step-v1/sequence-v2/manifest.json'
    if relative not in catalog['body']:catalog['body'].append(relative)
    p.write_text(json.dumps(catalog,indent=2)+'\n')
    states={}
    for relative in catalog['body']:
        manifest=ROOT/'character/marsh-v2'/relative;data=json.loads(manifest.read_text())
        for s in data['states']:
            files=[(manifest.parent/f).resolve().relative_to(ROOT).as_posix() for f in s['frameFiles']]
            states[s['id']]={'files':files,'hashes':[hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files],'durations':s['frameDurationsMs'],'loop':s['loop'],'pivot':data['pivot'],'standingHeight':data.get('standingHeight',148)}
    states={k:v for k,v in states.items() if not k.startswith(('equip-helmet-','remove-helmet-'))}
    p=ROOT/'character/marsh-consistency-review-v1/runtime-contract.json';old=json.loads(p.read_text())['states']
    for key,value in old.items():assert states[key]==value,(key,'unrelated source selection changed')
    assert set(states)-set(old)<= {'walk-step-north'}
    p.write_text(json.dumps({'states':states},indent=2)+'\n')
    (ROOT/'character/marsh-north-step-v1/selection.json').write_text(json.dumps({'changedStates':['walk-step-north'],'states':{'walk-step-north':states['walk-step-north']['files']},'status':'Normal actor/main/catalog/validator selected; native same-scene disk checks recorded; fresh-title Continue pending','sourceRecipeSha256':hashlib.sha256((ROOT/'character/marsh-north-step-v1/sequence-v2/recipe.json').read_bytes()).hexdigest()},indent=2)+'\n')
    print(len(states),'selected states;',sum(len(s['files']) for s in states.values()),'slots; unrelated sources unchanged')
if __name__=='__main__':install()
