"""Join whole quarter sequences at exact shared cardinal endpoints;no new pixels."""
from pathlib import Path
import copy,hashlib,json,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';O=B/'opposite-01-unselected';assert not O.exists();O.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else p.parent/n
quarters={};quarter_states=[];inputs=[]
for stem in ['east-south-01','west-south-02','east-north-02','west-north-01']:
    p=B/f'{stem}-unselected/manifest.json';m=json.loads(p.read_text());inputs.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    for state in m['states']:
        paths=[resolve(p,n) for n in state['frameFiles']];assert len(paths)==5
        quarters[state['id']]=paths;s=copy.deepcopy(state);s['frameFiles']=['res://'+q.relative_to(ROOT).as_posix() for q in paths];quarter_states.append(s)
        inputs.extend({'path':q.relative_to(ROOT).as_posix(),'sha256':sha(q)} for q in paths)
routes=[('east-west','east-north','north-west','north'),('north-south','north-east','east-south','east')]
chains={};joins=[]
for pair,a,b,via in routes:
    first=quarters['carry-turn-'+a];second=quarters['carry-turn-'+b];assert sha(first[-1])==sha(second[0]),'shared cardinal PNG differs'
    paths=first+second[1:];assert len(paths)==9;chains[pair]=paths;origin,dest=pair.split('-');chains[dest+'-'+origin]=list(reversed(paths))
    joins.append({'pair':pair,'via':via,'sharedEndpoint':first[-1].relative_to(ROOT).as_posix(),'sha256':sha(first[-1]),'secondSharedEndpoint':second[0].relative_to(ROOT).as_posix()})
g=json.loads((B/'sources/guide-provenance.json').read_text());states=[];records=[]
for pair,paths in chains.items():
    folder=O/('carry-turn-'+pair);folder.mkdir();files=[];frames=[]
    for i,q in enumerate(paths):
        p=folder/f'{i:03}.png';shutil.copy2(q,p);assert sha(p)==sha(q);files.append(p.relative_to(O).as_posix());frames.append(Image.open(p).convert('RGBA'));records.append({'state':'carry-turn-'+pair,'slot':i,'path':q.relative_to(ROOT).as_posix(),'sourceSha256':sha(q),'copy':p.relative_to(ROOT).as_posix()})
    old=next(t['timing'] for t in g['selectedTurns'] if t['key']=='carry-turn-'+pair);timing=old['frameDurationsMs'];assert timing==[60,90,100,90,120,90,100,90,60] and sum(timing)==800
    states.append({'id':'carry-turn-'+pair,'frameFiles':files,**old})
    frames[0].save(O/f'{pair}.apng',save_all=True,append_images=frames[1:],duration=timing,loop=0,disposal=0,blend=0)
    decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(O/f'{pair}.apng'))];assert len(decoded)==9 and all(a.tobytes()==b.tobytes() for a,b in zip(decoded,frames))
    board=Image.new('RGB',(1840,830),'#293b40');d=ImageDraw.Draw(board)
    for i,f in enumerate(frames):
        x=(i%5)*368;y=(i//5)*415;large=f.resize((368,368),Image.Resampling.NEAREST);board.paste(large,(x,y+35),large);d.text((x+4,y+5),f'{pair} whole slot{i} / {timing[i]}ms / staged',fill='white')
    board.save(O/f'{pair}-comparison.png')
for pair,paths in chains.items():
    a,b=pair.split('-');assert [sha(q) for q in paths]==list(reversed([sha(q) for q in chains[b+'-'+a]]))
m={'revision':'marsh-carry-opposite-01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states};(O/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
family_states=quarter_states
for state in states:
    s=copy.deepcopy(state);s['frameFiles']=['res://'+(O/n).relative_to(ROOT).as_posix() for n in s['frameFiles']];family_states.append(s)
assert len(family_states)==12 and len({s['id'] for s in family_states})==12 and sum(len(s['frameFiles']) for s in family_states)==76
family={**m,'revision':'marsh-carry-turn-family-01-unselected','states':family_states};(O/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeSourceCopies':36,'exactDecodedApngFrames':36,'reverseWholeOrderExact':True,'sharedEndpointJoins':joins,'quarterInputs':inputs,'sourceParity':records,'familyStates':12,'familySlots':76,'operations':'Copy exact whole PNG quarter frames;join once at common cardinal endpoint,reverse whole order only,no raster edits or mirroring. Existing selected opposite timing/facing/water/depth metadata retained.','limits':'Source packaging only;four quarter forward paths reviewed separately. Opposite/reverse actual paths and normalfullsave/visibleContinue untested;all known quarter angle/head/body/material/case/foot joins remain provisional.'},indent=2)+'\n')
print('Four staged opposite800ms states/36byte-exact PNGs/36decodedAPNGframes;12state76slot private family manifest;no raster edits.')
