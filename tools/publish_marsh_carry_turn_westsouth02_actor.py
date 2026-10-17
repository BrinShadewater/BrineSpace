"""Publish exact actual path-turn captures with scoped native evidence."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';A=ROOT/'output/marsh-animation-audit/carry-turn-west-south-02-2026-10-02';O=B/'west-south-02-actor-review';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
r=json.loads((A/'report.json').read_text());assert r['failures']==0 and r['actorRestores']==5 and len(r['samples'])==140 and r['turnSlots']==list(range(5)) and r['destinationSlots']==list(range(4))
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
stable={}
for name in ['inputs','owner']:
    before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text());stable[name]=len(before)
selected={};cat=ROOT/'character/marsh-v2/catalog.json'
manifests=[resolve(cat,n) for n in json.loads(cat.read_text())['body']]+[ROOT/'character/marsh-west-carry-material-v1/candidate-03/manifest.json',ROOT/'character/marsh-south-carry-material-v1/candidate-01/manifest.json',B/'west-south-02-unselected/manifest.json']
for p in manifests:
    for s in json.loads(p.read_text())['states']:selected[s['id']]=[resolve(p,n) for n in s['frameFiles']]
captures=r['captures'];assert len(captures)==12
assert [c['expectedKey'] for c in captures]==['idle-west','carry-west']+['carry-turn-west-south']*5+['carry-south']*5
assert [c['slot'] for c in captures[2:7]]==list(range(5)) and [c['slot'] for c in captures[7:11]]==list(range(4))
tiles=[];crops=[];sources=[]
for i,c in enumerate(captures):
    source=Image.open(A/c['sourceFile']).convert('RGBA');options=selected[c['expectedKey']] if c['slot']==-1 else [selected[c['expectedKey']][c['slot']]]
    matches=[p for p in options if Image.open(p).convert('RGBA').tobytes()==source.tobytes()];assert matches,(i,'source differs')
    for key in ['file','sourceFile']:shutil.copy2(A/c[key],O/c[key])
    sources.append({'capture':i,'key':c['expectedKey'],'slot':c['slot'],'path':matches[0].relative_to(ROOT).as_posix(),'sha256':sha(matches[0])})
    native=Image.open(A/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080);box=(x-100,y-110,x+110,y+30);assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
    crop=native.crop(box);crop.save(O/f'crop-{i:03}.png');crops.append(crop);tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile);tile.paste(source,(20,48),source);tile.paste(crop,(265,55));d.text((10,8),c['label']+' / slot'+str(c['slot']),fill='white');d.text((10,27),'Exact source / native crop; actual path corner, staged',fill='#b1d5c6');tiles.append(tile)
for group in range(3):
    board=Image.new('RGB',(1060,520),'#293b40')
    for j,tile in enumerate(tiles[group*4:group*4+4]):board.paste(tile,((j%2)*530,(j//2)*260))
    board.save(O/f'paired-{group}.png')
timing=[60,90,100,90,60];turn=crops[2:7];turn[0].save(O/'held-native-turn.apng',save_all=True,append_images=turn[1:],duration=timing,loop=0,disposal=0,blend=0)
decoded=[f.convert('RGB').copy() for f in ImageSequence.Iterator(Image.open(O/'held-native-turn.apng'))];assert len(decoded)==5
for f,t in zip(decoded,turn):assert f.tobytes()==t.tobytes()
assessment=O/'visual-assessment.json';visual=json.loads(assessment.read_text()).get('allTwelvePairsInspected',False) if assessment.exists() else False
evidence={'normalAdmission':False,'fullGoalComplete':False,'checks':r['checks'],'failures':0,'engineErrors':0,'exitCode':0,'captures':12,'exactSources':12,'controlledSamples':140,'actorPlayerRestores':5,'allFiveTurnPhases':True,'allFourDestinationPhases':True,'exactDestinationFrame0Return':True,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'sourceParity':sources,'visualReviewed':visual,'scope':r['scope'],'heldApng':'Five exact cropped held captures at60/90/100/90/60ms;not realtime continuous film/contact.','retainedFailure':'None in this independent West native interval;East fixture explicit bool retained.'}
(O/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({k:evidence[k] for k in ['checks','captures','exactSources','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles','normalAdmission']}))
