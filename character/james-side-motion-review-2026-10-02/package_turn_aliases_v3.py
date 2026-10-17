from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,os,copy
P=Path(__file__).resolve().parent;R=P.parents[1]
audit=json.loads((P/'east-turn-join-review.json').read_bytes());repairs=json.loads((P/'turn-head-v3-package-evidence.json').read_bytes())['records'];bindings={};frozen={}
def pixel_hash(file):return hashlib.sha256(Image.open(file).convert('RGBA').tobytes()).hexdigest()
def freeze(file):frozen[file.relative_to(R).as_posix()]=hashlib.sha256(file.read_bytes()).hexdigest()
for row in repairs:
    original=R/row['source'][6:];candidate=P/row['candidate'];freeze(original);freeze(candidate);h=pixel_hash(original)
    assert h not in bindings;bindings[h]=row
records=[];counts={'bare':0,'helmet':0};outputs={}
for mode in ['bare','helmet']:
    states=[];base=None
    for bank in [r for r in audit['records'] if r['gear']==mode]:
        path=R/bank['manifest'];freeze(path);pack=json.loads(path.read_bytes());state=next(s for s in pack['states'] if s['id']==bank['state']);result=copy.deepcopy(state);new_paths=[]
        base=pack if base is None else base
        for i,rel in enumerate(state['frameFiles']):
            file=R/rel[6:] if rel.startswith('res://') else (path.parent/rel).resolve();freeze(file);h=pixel_hash(file);repair=bindings.get(h) if mode=='bare' else None
            target=P/repair['candidate'] if repair else file
            new_paths.append(os.path.relpath(target,P).replace('\\','/'));counts[mode]+=bool(repair)
            records.append({'gear':mode,'state':state['id'],'index':i,'original':file.relative_to(R).as_posix(),'candidate':new_paths[-1],'repaired':bool(repair),'originalPixelHash':h,'candidatePixelHash':pixel_hash(target),'sharedRepair':None if repair is None else [repair['state'],repair['index']]})
        result['frameFiles']=new_paths
        if 'provenance' not in result:result['provenance']={}
        result['provenance']['headReview']='Staged compact bare head repair only for exact original full RGBA aliases; original turn metadata/clocks and unchanged paired shell. Unselected pending source/native/task joins.'
        states.append(result)
    result=copy.deepcopy(base);result['states']=states;result['name']='James staged East-connected turns v3 '+mode;result['status']='staged_unselected_head_join_review'
    (P/('east-turn-v3-'+mode+'-manifest.json')).write_text(json.dumps(result,indent=2));outputs[mode]=result
assert counts['helmet']==0
assert counts['bare']>=12,counts
for mode in ['bare','helmet']:
    lookup={s['id']:s for s in outputs[mode]['states']}
    for a,b in [('east','north'),('east','south'),('east','west')]:
        one=lookup['carry-turn-'+a+'-'+b];two=lookup['carry-turn-'+b+'-'+a]
        assert len(one['frameFiles'])==len(two['frameFiles'])
        for x,y in zip(one['frameFiles'],reversed(two['frameFiles'])):assert pixel_hash(P/x)==pixel_hash(P/y)
freeze(R/'scripts/grid_canvas.gd');freeze(R/'character/ACTIVE_ASSETS.json')
(P/'east-turn-v3-inputs.json').write_text(json.dumps(frozen,indent=2))
(P/'east-turn-v3-package-evidence.json').write_text(json.dumps({'records':records,'repairedSlots':counts,'slots':len(records),'originalMetadataPreserved':True,'exactPairedReverseAliases':True,'selected':False,'scope':'92 source refs in staged paired six-turn manifests; six unique bare repairs propagated only across exact original full-RGBA equality. Original clocks/geometry and helmet sources retained. No normal loader or actor/task acceptance.'},indent=2))
print(json.dumps({'slots':len(records),'repairedSlots':counts,'uniqueRepairs':len(bindings),'pairedReverseAliases':True,'selected':False}))
