"""Register whole West figures and derive the tested actual-actor contact probe."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/marsh-west-walk-family-detail-v1'
OUT=ROOT/'character/marsh-west-walk-family-contact-v1';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((SOURCE/'review.json').read_text());records=[]
for r in review['records']:
    i=r['slot'];p=SOURCE/f'{i:03}.png';assert sha(p)==r['frameSha256']
    assert .98<=r['heightRatio']<=1.02 and r['opaqueIoU']>.90
    dy=-r['soleDisplacement'];assert abs(dy)<=1
    a=np.asarray(Image.open(p).convert('RGBA'));q=OUT/f'{i:03}.png'
    if dy:
        assert np.all(a[-1,:,3]==0) if dy==1 else np.all(a[0,:,3]==0)
        b=np.zeros_like(a)
        if dy==1:b[1:]=a[:-1];assert np.array_equal(b[1:],a[:-1])
        else:b[:-1]=a[1:];assert np.array_equal(b[:-1],a[1:])
        assert np.count_nonzero(b[:,:,3])==np.count_nonzero(a[:,:,3])
        Image.fromarray(b).save(q)
    else:shutil.copyfile(p,q)
    assert abs(r['crownDisplacement']+dy)<=2
    records.append({'slot':i,'beforePath':p.relative_to(ROOT).as_posix(),'beforeSha256':sha(p),'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q),'translation':[0,dy],'originalBounds':r['originalOpaqueBounds'],'sourceBounds':r['opaqueBounds'],'method':'Lossless whole RGBA registration, outgoing alpha0/surviving rows exact/visible count unchanged.' if dy else 'Exact byte copy.'})
manifest=json.loads((SOURCE/'manifest.json').read_text());manifest['states'][0]['frameFiles']=['res://'+(OUT/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(OUT/'registration.json').write_text(json.dumps({'records':records,'normalAdmission':False,'sourceReviewSha256':sha(SOURCE/'review.json'),'scope':'Whole drawings only, no anatomy fitting/recolour/alpha cleanup; bounds predict contact, actual main/grid proof follows.'},indent=2)+'\n')
s=(ROOT/'tools/review_marsh_east_walk_world_v1.gd').read_text().replace('east','west').replace('East','West').replace('EAST','WEST')
s=s.replace('west-walk-world-v3-2026-10-03','west-walk-world-v1-2026-10-03').replace('Vector2(112,0)','Vector2(-112,0)').replace('start+Vector2(length,0)','start-Vector2(length,0)')
old='actor.foot.x>=previous.x-.001 and actor.foot.x<=start.x+length+.001'
new='actor.foot.x<=previous.x+.001 and actor.foot.x>=start.x-length-.001'
assert old in s;s=s.replace(old,new)
(ROOT/'tools/review_marsh_west_walk_world_v1.gd').write_text(s)
(ROOT/'tools/review_marsh_west_walk_world_v1.gd.uid').write_text('uid://dmwestworldwalk1\n')
f=(ROOT/'tools/fingerprint_marsh_east_walk_selected_v1.py').read_text()
f=f.replace('records={p.relative_to(ROOT)',"paths.update(p for folder in ['character/marsh-west-walk-family-detail-v1','character/marsh-west-walk-family-contact-v1'] for p in (ROOT/folder).glob('*') if p.is_file())\npaths.update(ROOT/'tools'/n for n in ['prepare_marsh_west_walk_family_v1.py','review_marsh_west_walk_family_v1.py','prepare_marsh_west_walk_world_v1.py','review_marsh_west_walk_world_v1.gd','review_marsh_west_walk_world_v1.gd.uid','fingerprint_marsh_west_walk_world_v1.py'])\nrecords={p.relative_to(ROOT)")
(ROOT/'tools/fingerprint_marsh_west_walk_world_v1.py').write_text(f)
p=(ROOT/'tools/publish_marsh_east_walk_world_v1.py').read_text().replace('east-walk-world-v3-2026-10-03','west-walk-world-v1-2026-10-03').replace('marsh-east-walk-family-contact-v1','marsh-west-walk-family-contact-v1').replace('post-south-contact','post-east-walk').replace("key=='walk-east'","key=='walk-west'")
p=p.replace('1653','1561').replace('3,43','3,36').replace("'pairedCaptures':43","'pairedCaptures':36")
p=p.replace("print('43exact same-root source/native pairs;8complete review boards;5377inputs/2931owner stable;normal selection unchanged')","print(f'36exact same-root source/native pairs;6complete review boards;{len(a)}inputs/{len(owner)}owner stable;normal selection unchanged')")
(ROOT/'tools/publish_marsh_west_walk_world_v1.py').write_text(p)
print('Whole-frame West registration and actual normal-actor/main/grid staged probe prepared; catalogue unchanged.')
