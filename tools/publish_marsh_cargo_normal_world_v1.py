"""Exact-source paired boards for one normal-controller water journey."""
from pathlib import Path
import hashlib,json,math,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-v2/supplemental/cargo-matched-v1';A=ROOT/'output/marsh-animation-audit/cargo-normal-world-v1-2026-10-03';INTERVAL=ROOT/'output/marsh-animation-audit/cargo-normal-v1-2026-10-03';O=B/'world-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
r=read(A/'report.json');assert r['failures']==0 and len(r['phases'])==12
assert (INTERVAL/'world-exit.txt').read_text().strip()=='0'
log=(INTERVAL/'world.log').read_text()
assert not any(marker in log for marker in ['ERROR:', 'WARNING:', 'SCRIPT ERROR'])
stable={}
for kind in ['inputs','owner']:
    before=read(INTERVAL/f'{kind}-before.json');assert before==read(INTERVAL/f'{kind}-after.json');stable[kind]=len(before)
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
manifests=[resolve(cat,n) for n in read(cat)['body']]
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
    d.text((8,25),'Exact source / q2 normal selected cargo journey',fill='#b1d5c6');tiles.append(tile)
    for key in ['file','sourceFile']:shutil.copy2(A/c[key],O/c[key])
    parity.append({'key':c['expectedKey'],'slot':c['slot'],'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
boards=[]
for page in range(math.ceil(len(tiles)/8)):
    batch=tiles[page*8:page*8+8];board=Image.new('RGB',(2120,260*math.ceil(len(batch)/4)),'#293b40')
    for j,t in enumerate(batch):board.paste(t,((j%4)*530,(j//4)*260))
    name=f'route-{page:02}-pairs.png';board.save(O/name);boards.append({'file':name,'pairs':len(batch)})
endpoint_checks=[]
v={'checks':r['checks'],'failures':0,'actualCompletedExpeditions':1,'phases':r['phases'],'sourceNativePairs':len(parity),'samples':len(r['samples']),'actorPlayerRestores':r['actorPlayerRestores'],'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'boards':boards,'sourceParity':parity,'endpointChecks':endpoint_checks,'scope':r['scope'],'normalAdmission':True,'fullGoalComplete':False,'visualReviewed':(O/'visual-assessment.json').exists()}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({k:v[k] for k in ['checks','sourceNativePairs','samples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']}));print(len(boards),'native route comparison boards prepared')
