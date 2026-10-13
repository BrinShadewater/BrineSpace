"""Publish96 exact source/native pairs with seven actual route scopes."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1';A=ROOT/'output/marsh-animation-audit/carry-remaining-paths-01-2026-10-02';O=B/'remaining-paths-01-actor-review';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else p.parent/n
r=json.loads((A/'report.json').read_text());keys=['carry-turn-'+p for p in ['south-east','south-west','north-east','north-west','west-east','north-south','south-north']]
assert r['failures']==0 and [c['key'] for c in r['cases']]==keys and len(r['captures'])==96 and len(r['samples'])==1040
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
stable={}
for name in ['inputs','owner']:
    before=json.loads((A/f'{name}-before.json').read_text());assert before==json.loads((A/f'{name}-after.json').read_text());stable[name]=len(before)
cat=ROOT/'character/marsh-v2/catalog.json';manifests=[resolve(cat,n) for n in json.loads(cat.read_text())['body']]
manifests += [ROOT/'character/marsh-east-carry-material-v1/candidate-03/manifest.json',ROOT/'character/marsh-west-carry-material-v1/candidate-03/manifest.json',ROOT/'character/marsh-south-carry-material-v1/candidate-01/manifest.json',ROOT/'character/marsh-north-carry-material-v1/candidate-01/manifest.json',B/'opposite-01-unselected/family-manifest.json']
selected={};timings={}
for p in manifests:
    for s in json.loads(p.read_text())['states']:selected[s['id']]=[resolve(p,n) for n in s['frameFiles']];timings[s['id']]=s.get('frameDurationsMs',[])
sources=[];case_evidence=[];restores=0;decoded_count=0
for case in r['cases']:
    key=case['key'];phases=case['phaseCount'];count=phases+7;assert case['captureCount']==count and case['samples']==(140 if phases==5 else 160) and case['actorRestores']==phases and case['turnSlots']==list(range(phases)) and case['destinationSlots']==list(range(4))
    start=case['captureStart'];caps=r['captures'][start:start+count];assert [c['expectedKey'] for c in caps]==['idle-'+case['origin'],'carry-'+case['origin']]+[key]*phases+['carry-'+case['destination']]*5
    assert [c['slot'] for c in caps[2:2+phases]]==list(range(phases)) and [c['slot'] for c in caps[2+phases:6+phases]]==list(range(4))
    tiles=[];crops=[]
    for j,c in enumerate(caps):
        source=Image.open(A/c['sourceFile']).convert('RGBA');options=selected[c['expectedKey']] if c['slot']==-1 else [selected[c['expectedKey']][c['slot']]]
        matches=[p for p in options if Image.open(p).convert('RGBA').tobytes()==source.tobytes()];assert matches,(start+j,'wrong exactsource')
        for n in ['file','sourceFile']:shutil.copy2(A/c[n],O/c[n])
        sources.append({'capture':start+j,'case':key,'key':c['expectedKey'],'slot':c['slot'],'path':matches[0].relative_to(ROOT).as_posix(),'sha256':sha(matches[0])})
        native=Image.open(A/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080);box=(x-100,y-110,x+110,y+30);assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
        crop=native.crop(box);crop.save(O/f'crop-{start+j:03}.png');crops.append(crop)
        tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile);tile.paste(source,(20,48),source);tile.paste(crop,(265,55));d.text((10,8),c['label']+' / slot'+str(c['slot']),fill='white');d.text((10,27),'Exact source / native crop; actual normal route, staged',fill='#b1d5c6');tiles.append(tile)
    board=Image.new('RGB',(2120,260*(count//4)),'#293b40')
    for j,tile in enumerate(tiles):board.paste(tile,((j%4)*530,(j//4)*260))
    name=key.removeprefix('carry-turn-');board.save(O/f'{name}-pairs.png')
    turn=crops[2:2+phases];timing=timings[key];assert len(timing)==phases and sum(timing)==(400 if phases==5 else 800)
    turn[0].save(O/f'{name}-held.apng',save_all=True,append_images=turn[1:],duration=timing,loop=0,disposal=0,blend=0)
    decoded=[f.convert('RGB').copy() for f in ImageSequence.Iterator(Image.open(O/f'{name}-held.apng'))];assert len(decoded)==phases and all(a.tobytes()==b.tobytes() for a,b in zip(decoded,turn))
    decoded_count+=phases;restores+=phases;case_evidence.append({'key':key,'phases':phases,'captures':count,'samples':case['samples'],'actorPlayerRestores':phases,'exactDestination0Return':True,'allDestinationPhases':True,'board':f'{name}-pairs.png'})
assert restores==decoded_count==47
assessment=O/'visual-assessment.json';visual=json.loads(assessment.read_text()).get('all96PairsInspected',False) if assessment.exists() else False
evidence={'normalAdmission':False,'fullGoalComplete':False,'checks':r['checks'],'failures':0,'engineErrors':0,'exitCode':0,'actualPaths':7,'captures':96,'exactSources':96,'controlledSamples':1040,'actorPlayerRestores':47,'decodedHeldApngFrames':47,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'sourceParity':sources,'cases':case_evidence,'visualReviewed':visual,'scope':r['scope'],'limits':'Seven actual staged paths only;held crops/APNG not realtime film/contact,notfullRunSave/visibleTitleContinue/complete delivery orfullsetacceptance.'}
(O/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n');print(json.dumps({k:evidence[k] for k in ['checks','actualPaths','captures','exactSources','controlledSamples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']}))
