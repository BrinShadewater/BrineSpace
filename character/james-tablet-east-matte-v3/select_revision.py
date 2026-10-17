from pathlib import Path
import json, hashlib, os, uuid
P=Path(__file__).resolve().parent; R=P.parents[1]
old='james-tablet-east-belt-fixed-source-v2'; new=P.name
def atomic(path,data):
    before=path.read_bytes(); tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    tmp.write_bytes(data)
    assert path.read_bytes()==before, str(path)+' changed concurrently'
    os.replace(tmp,path)
archive=P/'before-selection'; archive.mkdir(exist_ok=True)
changes=[]
for rel in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json']:
    path=R/rel; data=path.read_bytes(); revised=data
    for mode in ['bare','helmet']:
        a=(old+'/'+mode+'-manifest.json').encode(); b=(new+'/'+mode+'-manifest.json').encode()
        assert data.count(a)==1,(rel,mode)
        revised=revised.replace(a,b)
    saved=archive/path.name
    assert not saved.exists(), 'Already selected; inspect state before retry'
    saved.write_bytes(data); atomic(path,revised)
    changes.append({'path':rel,'before':hashlib.sha256(data).hexdigest(),'after':hashlib.sha256(revised).hexdigest()})
for stem in ['validate','native-arrival-continue']:
    text=(R/'character'/old/(stem+'.gd')).read_text().replace(old,new)
    (P/(stem+'.gd')).write_text(text)
for mode in ['bare','helmet']:
    path=P/(mode+'-manifest.json'); pack=json.loads(path.read_bytes())
    pack['status']='selected_source_reviewed_native_validation_pending'
    atomic(path,(json.dumps(pack,indent=2)+'\n').encode())
(P/'selection-evidence.json').write_text(json.dumps({'changes':changes,'visualReview':'All282 final source frames in10boards and both master/current/candidate comparison boards inspected. Tablet matte grey; geometry preserved. Native validation pending.'},indent=2))
print('Selected paired East tablet revision; two exact loader/registry paths changed in each file.')
