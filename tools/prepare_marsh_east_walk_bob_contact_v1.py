"""Register revised phase1 without painting, then prepare the proven native fixture."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/marsh-east-walk-bob-polish-v1'
OUT=ROOT/'character/marsh-east-walk-bob-contact-v1';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((SOURCE/'review.json').read_text());records=[]
for slot in range(6):
    source=SOURCE/f'{slot:03}.png';assert sha(source)==review['records'][slot]['frameSha256']
    dest=OUT/f'{slot:03}.png';arr=np.asarray(Image.open(source).convert('RGBA'))
    if slot==1:
        assert np.all(arr[-1,:,3]==0)
        translated=np.zeros_like(arr);translated[1:]=arr[:-1]
        assert np.array_equal(translated[1:],arr[:-1])
        assert np.count_nonzero(translated[:,:,3])==np.count_nonzero(arr[:,:,3])
        Image.fromarray(translated).save(dest)
    else:shutil.copyfile(source,dest)
    records.append({'slot':slot,'beforePath':source.relative_to(ROOT).as_posix(),'beforeSha256':sha(source),'path':dest.relative_to(ROOT).as_posix(),'sha256':sha(dest),'translation':[0,1] if slot==1 else [0,0],'method':'Entire RGBA Y+1, outgoing row alpha0, surviving rows equal, visible alpha count identical.' if slot==1 else 'Exact byte copy.'})
manifest=json.loads((SOURCE/'manifest.json').read_text())
manifest['states'][0]['frameFiles']=['res://'+(OUT/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'registration.json').write_text(json.dumps({'records':records,'normalAdmission':False,'sourceReviewSha256':sha(SOURCE/'review.json'),'reason':'Phase1 whole-canvas edit preserved crown but sole one native pixel above original; bound geometry only, actual normal-actor contact verification follows.'},indent=2)+'\n')
s=(ROOT/'tools/review_marsh_east_walk_world_v1.gd').read_text()
s=s.replace('east-walk-world-v3-2026-10-03','east-walk-bob-world-v1-2026-10-03').replace('marsh-east-walk-family-contact-v1/manifest.json','marsh-east-walk-bob-contact-v1/manifest.json')
(ROOT/'tools/review_marsh_east_walk_bob_world_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_east_walk_bob_world_v1.gd.uid').write_text('uid://dmeastbobworld1\n')
f=(ROOT/'tools/fingerprint_marsh_east_walk_world_v1.py').read_text()
f=f.replace('records={p.relative_to(ROOT)',"paths.update(p for folder in ['character/marsh-east-walk-bob-polish-v1','character/marsh-east-walk-bob-contact-v1'] for p in (ROOT/folder).glob('*') if p.is_file())\npaths.update(ROOT/'tools'/n for n in ['prepare_marsh_east_walk_bob_polish_v1.py','review_marsh_east_walk_bob_polish_v1.py','prepare_marsh_east_walk_bob_contact_v1.py','review_marsh_east_walk_bob_world_v1.gd','review_marsh_east_walk_bob_world_v1.gd.uid','fingerprint_marsh_east_walk_bob_world_v1.py'])\nrecords={p.relative_to(ROOT)")
(ROOT/'tools/fingerprint_marsh_east_walk_bob_world_v1.py').write_text(f)
print('Phase1 full RGBA registration proved; five exact copies; native fixture derived from tested1653-check actual actor/main/grid probe.')
