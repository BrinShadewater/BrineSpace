"""Exact-source paired boards for one normal-controller water journey."""
from pathlib import Path
import hashlib,json,math,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';A=ROOT/'output/marsh-animation-audit/loaded-swim-northfamily-world-01-2026-10-03';O=B/'northfamily-world-01-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
r=read(A/'report.json');assert r['failures']==0 and len(r['phases'])==12
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text() and 'WARNING:' not in (A/'native.log').read_text()
stable={}
for kind in ['inputs','owner']:
    before=read(A/f'{kind}-before.json');assert before==read(A/f'{kind}-after.json');stable[kind]=len(before)
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
manifests=[resolve(cat,n) for n in read(cat)['body']]+[B/'opposite-ew-01-unselected/family-manifest.json']
for p in manifests:
    for state in read(p)['states']:selected[state['id']]=[resolve(p,n) for n in state['frameFiles']]
tiles=[];parity=[]
for i,c in enumerate(r['captures']):
    p=selected[c['expectedKey']][c['slot']];source=Image.open(A/c['sourceFile']).convert('RGBA')
    assert source.tobytes()==Image.open(p).convert('RGBA').tobytes()
    native=Image.open(A/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080)
    box=(x-105,y-115,x+115,y+40);assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
    crop=native.crop(box);tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile)
    tile.paste(source,(10,44),source);tile.paste(crop,(265,52));d.text((8,6),c['phase']+' / '+c['expectedKey']+' / '+str(c['slot']),fill='white')
    d.text((8,25),'Exact source / q0 journey / private North-turn family',fill='#b1d5c6');tiles.append(tile)
    for key in ['file','sourceFile']:shutil.copy2(A/c[key],O/c[key])
    parity.append({'key':c['expectedKey'],'slot':c['slot'],'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
boards=[]
for page in range(math.ceil(len(tiles)/8)):
    batch=tiles[page*8:page*8+8];board=Image.new('RGB',(2120,260*math.ceil(len(batch)/4)),'#293b40')
    for j,t in enumerate(batch):board.paste(t,((j%4)*530,(j//4)*260))
    name=f'route-{page:02}-pairs.png';board.save(O/name);boards.append({'file':name,'pairs':len(batch)})
endpoint_checks=[];new=selected['swim-carry-west'][0]
for key,slot in [('swim-pickup-west',-1),('swim-carry-turn-east-west',-1),('swim-carry-turn-west-south',0),('cargo-drain-west',0)]:
    old=selected[key][slot];endpoint_checks.append({'key':key,'slot':slot,'sameAsNewWestLoop0':Image.open(old).convert('RGBA').tobytes()==Image.open(new).convert('RGBA').tobytes(),'oldPath':old.relative_to(ROOT).as_posix(),'oldSha256':sha(old),'newPath':new.relative_to(ROOT).as_posix(),'newSha256':sha(new)})
v={'checks':r['checks'],'failures':0,'actualCompletedExpeditions':1,'phases':r['phases'],'sourceNativePairs':len(parity),'samples':len(r['samples']),'actorPlayerRestores':r['actorPlayerRestores'],'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'boards':boards,'sourceParity':parity,'endpointChecks':endpoint_checks,'scope':r['scope'],'normalAdmission':False,'fullGoalComplete':False,'visualReviewed':(O/'visual-assessment.json').exists()}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({k:v[k] for k in ['checks','sourceNativePairs','samples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']}));print(json.dumps(boards));print(json.dumps(endpoint_checks))
