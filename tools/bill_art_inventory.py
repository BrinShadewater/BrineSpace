"""Record source provenance for every effective Bill body frame from a runtime dump."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
WATER=ROOT/'character/crew-underwater-v1'
DUMP=ROOT/'output/local-sprite-repair-2026-09-12/runtime-baseline'
TARGET=ROOT/'tools/bill-art-source-contract.json'

def signature(path):
    im=Image.open(path).convert('RGBA'); box=im.getbbox()
    a=np.array(im.crop(box));a[a[:,:,3]==0]=0
    return (a.shape,hashlib.sha256(a.tobytes()).hexdigest()),box

def manifests():
    yield ROOT/'character/major-bill-v2/final/manifest.json'
    yield ROOT/'character/crew-construction-v1/bill/manifest.json'
    for root in ['crew-actions-v1','crew-life-v1']:
        yield from sorted((ROOT/'character'/root/'bill').glob('*/manifest.json'))
    for clip in ['death-ground-east','death-water-east','tread-east','tread-west','tread-north','tread-south','equip-helmet-east','remove-helmet-east']:
        yield WATER/'pilot'/f'bill-{clip}'/'manifest.json'
    for clip in ['swim-east-v2','swim-west-v2','swim-south-v2','swim-north-v2','pickup-helmet-east-v4','deposit-helmet-east-v1']:
        yield WATER/'revisions'/f'bill-{clip}'/'manifest.json'
    for clip in ['equip-helmet-east','remove-helmet-east']:
        yield WATER/'locker'/f'bill-{clip}'/'manifest.json'

def main():
    lookup={}; sources={}; records={}
    for path in manifests():
        data=json.loads(path.read_text())
        sources[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
        for e in data['states']:
            for rel in e['frameFiles']:
                frame=(path.parent/rel).resolve()
                key=frame.relative_to(ROOT).as_posix()
                if key in records: continue
                sig,box=signature(frame)
                records[key]={'manifest':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(frame.read_bytes()).hexdigest(),'bounds':list(box)}
                lookup.setdefault(sig,(key,box))
    inventory=json.loads((DUMP/'inventory.json').read_text())
    unmatched=[]
    for e in inventory['states']:
        for f in e['frames']:
            sig,box=signature(DUMP/f['file'])
            if sig not in lookup:
                unmatched.append(f['file']);continue
            source,sbox=lookup[sig]
            f['sourceFrame']=source
            f['sourceOffset']=[box[0]-sbox[0],box[1]-sbox[1]]
            f.pop('file')
    if unmatched:
        (DUMP/'unmatched.json').write_text(json.dumps(unmatched,indent=2))
        raise RuntimeError(f'{len(unmatched)} effective frames have no source match: {unmatched[:10]}')
    inventory['equipmentStates']=[e['id'] for e in inventory.pop('equipment')]
    inventory.update(sourceFrames=records,sourceManifests=sources,method='Actual runtime frame matching against original source frames; transparent margins may differ at transition endpoints. Offsets are source pixels at the legacy density.')
    TARGET.parent.mkdir(exist_ok=True)
    TARGET.write_text(json.dumps(inventory,indent=2)+'\n')
    print(json.dumps({'states':len(inventory['states']),'frames':sum(len(e['frames']) for e in inventory['states']),'originalFrames':len(records),'manifests':len(sources),'unmatched':len(unmatched)}))

if __name__=='__main__':main()
