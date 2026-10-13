"""Exact-source complete-route boards; captures are samples, not contact film."""
from pathlib import Path
import hashlib,json,shutil,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';A=ROOT/'output/marsh-animation-audit/cargo-delivery-01-2026-10-02';O=B/'delivery-01-actor-review';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
r=read(A/'report.json');assert r['failures']==0 and [c['origin'] for c in r['cases']]==['east','west','south','north']
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
stable={}
for n in ['inputs','owner']:
    before=read(A/f'{n}-before.json');assert before==read(A/f'{n}-after.json');stable[n]=len(before)
catalog=ROOT/'character/marsh-v2/catalog.json';manifests=[resolve(catalog,n) for n in read(catalog)['body']]
for f,rev in [('east','03'),('west','03'),('south','01'),('north','01')]:manifests.append(ROOT/f'character/marsh-{f}-carry-material-v1/candidate-{rev}/manifest.json')
manifests += [ROOT/'character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json',B/'side02-cross-review/family-manifest.json']
selected={}
for p in manifests:
    for s in read(p)['states']:selected[s['id']]=[resolve(p,n) for n in s['frameFiles']]
parity=[];boards=[];restores=0
for case in r['cases']:
    assert case['completed'] and case['stages']==['workshop_pickup','workshop_carry','workshop_unload'] and case['pickupSlots']==case['unloadSlots']==list(range(4))
    assert case['actorRestores']==case['captureCount']
    restores+=case['actorRestores'];start=case['captureStart'];caps=r['captures'][start:start+case['captureCount']];tiles=[]
    assert all(c['case']==case['origin'] for c in caps)
    for j,c in enumerate(caps):
        p=selected[c['expectedKey']][c['slot']];source=Image.open(A/c['sourceFile']).convert('RGBA');assert source.tobytes()==Image.open(p).convert('RGBA').tobytes(),(case['origin'],c['expectedKey'],c['slot'])
        for n in ['file','sourceFile']:shutil.copy2(A/c[n],O/c[n])
        native=Image.open(A/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080);box=(x-100,y-110,x+110,y+30)
        assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
        crop=native.crop(box);crop.save(O/f'crop-{start+j:03}.png')
        tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile);tile.paste(source,(20,48),source);tile.paste(crop,(265,55));d.text((10,8),case['origin']+' / '+c['expectedKey']+' / '+str(c['slot']),fill='white');d.text((10,27),'Exact source / native complete normal delivery, staged',fill='#b1d5c6');tiles.append(tile)
        parity.append({'case':case['origin'],'key':c['expectedKey'],'slot':c['slot'],'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    for page in range(math.ceil(len(tiles)/8)):
        batch=tiles[page*8:page*8+8];board=Image.new('RGB',(2120,260*math.ceil(len(batch)/4)),'#293b40')
        for j,tile in enumerate(batch):board.paste(tile,((j%4)*530,(j//4)*260))
        name=f'{case["origin"]}-{page:02}-pairs.png';board.save(O/name);boards.append({'case':case['origin'],'file':name,'pairs':len(batch)})
assert restores==len(parity)==len(r['captures'])
assessment=O/'visual-assessment.json'
v={'normalAdmission':False,'fullGoalComplete':False,'checks':r['checks'],'failures':0,'completeNormalDeliveries':4,'captures':len(parity),'exactSources':len(parity),'controlledSamples':len(r['samples']),'actorPlayerRestores':restores,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'cases':r['cases'],'boards':boards,'sourceParity':parity,'visualReviewed':read(assessment).get('allPairsInspected',False) if assessment.exists() else False,'scope':r['scope'],'limits':'Complete normal furnished-fixture delivery routes with staged sources. Not paid building/expedition/fullRunSave/actualvisibleTitleContinue/continuouscontact/normaladmission/fullsetacceptance.'}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['checks','completeNormalDeliveries','captures','controlledSamples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']}))
print(json.dumps(boards))
