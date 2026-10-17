"""Consolidate selected staged quarters and derive halves without changing art."""
from pathlib import Path
import copy, hashlib, json, shutil
from PIL import Image, ImageDraw
H = Path(__file__).resolve().parent
R = H.parents[1]
families = ['east-south','south-west','west-north','north-east']
routes = [('east','south','west'),('west','south','east'),('north','east','south'),('south','east','north')]
provenance = {}; counts = 0
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for gear in ['bare','helmet']:
    lookup = {}; base = None
    for family in families:
        folder = R/'character'/('veld-swim-turn-'+family+'-coherent-v1')
        manifest = json.loads((folder/(gear+'-manifest.json')).read_text())
        base = base or copy.deepcopy(manifest)
        for state in manifest['states']:
            lookup[state['id']] = (folder,state)
    output = copy.deepcopy(base); output['name'] = 'Veld coherent ordinary swimming turn matrix '+gear; output['states'] = []
    for key,(folder,state) in lookup.items():
        selected = copy.deepcopy(state); selected['frameFiles'] = []
        records = []
        for i,path in enumerate(state['frameFiles']):
            rel = f'frames/{gear}/{key}/{i:03}.png'; target=H/rel; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(folder/path,target); selected['frameFiles'].append(rel)
            records.append(dict(file=rel,source=str((folder/path).relative_to(R)).replace('\\','/'),sha256=sha(target)))
        output['states'].append(selected); provenance[gear+'/'+key] = dict(kind='unchanged staged quarter',frames=records)
    for a,b,c in routes:
        left_dir,left = lookup[f'swim-turn-{a}-{b}']; right_dir,right = lookup[f'swim-turn-{b}-{c}']
        assert Image.open(left_dir/left['frameFiles'][-1]).tobytes()==Image.open(right_dir/right['frameFiles'][0]).tobytes()
        key=f'swim-turn-{a}-{c}'; state = copy.deepcopy(left); state['id']=key; state['frameFiles']=[]
        for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']:
            state[field]=left[field]+right[field][1:]
        state['frameDurationsMs'][5]+=right['frameDurationsMs'][0]
        assert sum(state['frameDurationsMs'])==1040 and len(state['frameDurationsMs'])==11
        records=[]
        sources=[(left_dir,p) for p in left['frameFiles']]+[(right_dir,p) for p in right['frameFiles'][1:]]
        for i,(folder,path) in enumerate(sources):
            rel=f'frames/{gear}/{key}/{i:03}.png'; target=H/rel; target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(folder/path,target); state['frameFiles'].append(rel)
            records.append(dict(file=rel,source=str((folder/path).relative_to(R)).replace('\\','/'),sha256=sha(target)))
        output['states'].append(state); provenance[gear+'/'+key]=dict(kind='derived two quarters; exact shared middle stored once',route=[a,b,c],middleDurationMs=140,totalMs=1040,frames=records)
    (H/(gear+'-manifest.json')).write_text(json.dumps(output,indent=2)+'\n')
    board=Image.new('RGBA',(11*256,4*280),'#202a30'); draw=ImageDraw.Draw(board)
    for row,state in enumerate(output['states'][8:]):
        draw.text((5,row*280+4),gear+' '+state['id']+' / exact middle master;1040ms',fill='white')
        for i,p in enumerate(state['frameFiles']): board.alpha_composite(Image.open(H/p).convert('RGBA'),(i*256,row*280+24))
    board.save(H/(gear+'-half-contact-v1.png')); counts+=sum(len(s['frameFiles']) for s in output['states'])
(H/'provenance.json').write_text(json.dumps(dict(installed=False,sourceFamilies=families,states=provenance),indent=2)+'\n')
print('24 gear states / '+str(counts)+' frame references; exact derived half joins.')
