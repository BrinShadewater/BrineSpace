"""Publish exact East timed-action source/native evidence, no admission claim."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';A=ROOT/'output/marsh-animation-audit/cargo-side-action-02-2026-10-02';O=B/'side-action-02-actor-review';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
r=read(A/'report.json');assert r['failures']==0 and len(r['captures'])==16 and [(c['facing'],c['action']) for c in r['cases']]==[('east','pickup'),('east','unload'),('west','pickup'),('west','unload')]
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
stable={}
for name in ['inputs','owner']:
    before=read(A/f'{name}-before.json');assert before==read(A/f'{name}-after.json');stable[name]=len(before)
states={s['id']:s for f in ['east','west'] for s in read(B/f'{f}-unload-02-unselected/manifest.json')['states']};parity=[]
for case in r['cases']:
    assert case['slots']==list(range(4)) and case['actorRestores']==case['captureCount']==4
    key=case['action']+'-'+case['facing'];caps=r['captures'][case['captureStart']:case['captureStart']+4];tiles=[];crops=[]
    for j,c in enumerate(caps):
        assert c['expectedKey']==key and c['slot']==j
        p=ROOT/states[key]['frameFiles'][j].removeprefix('res://');source=Image.open(A/c['sourceFile']).convert('RGBA')
        assert source.tobytes()==Image.open(p).convert('RGBA').tobytes()
        for n in ['file','sourceFile']:shutil.copy2(A/c[n],O/c[n])
        native=Image.open(A/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080);box=(x-100,y-110,x+110,y+30)
        assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
        crop=native.crop(box);crops.append(crop);crop.save(O/f'{key}-{j}-crop.png')
        tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile);tile.paste(source,(20,48),source);tile.paste(crop,(265,55));d.text((10,8),key+' / slot'+str(j),fill='white');d.text((10,27),'Exact source / native normal timed action, staged',fill='#b1d5c6');tiles.append(tile)
        parity.append({'key':key,'slot':j,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    board=Image.new('RGB',(2120,260),'#293b40')
    for j,tile in enumerate(tiles):board.paste(tile,(j*530,0))
    board.save(O/f'{key}-pairs.png')
    crops[0].save(O/f'{key}-held.apng',save_all=True,append_images=crops[1:],duration=[130]*4,loop=0,disposal=0,blend=0)
    decoded=[im.convert('RGB').copy() for im in ImageSequence.Iterator(Image.open(O/f'{key}-held.apng'))]
    assert len(decoded)==4 and all(x.tobytes()==y.tobytes() for x,y in zip(decoded,crops))
assessment=O/'visual-assessment.json'
e={'normalAdmission':False,'fullGoalComplete':False,'checks':r['checks'],'failures':0,'captures':16,'exactSources':16,'samples':len(r['samples']),'actorPlayerRestores':16,'decodedHeldFrames':16,'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'cases':r['cases'],'sourceParity':parity,'visualReviewed':read(assessment).get('allSixteenPairsInspected',False) if assessment.exists() else False,'scope':r['scope'],'limits':'East/West unloads seeded valid timed actions, not actual workshop arrival which forces North. No expedition delivery/fullsave/TitleContinue/continuous contact/normal admission/fullset acceptance.'}
(O/'verification.json').write_text(json.dumps(e,indent=2)+'\n');print(json.dumps({k:e[k] for k in ['checks','captures','samples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']}))
