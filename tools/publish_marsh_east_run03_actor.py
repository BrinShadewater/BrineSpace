"""Publish exact staged run captures; keep held review separate from admission."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageSequence
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1';AUDIT=ROOT/'output/marsh-animation-audit/east-run-actor-03-2026-10-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=json.loads((AUDIT/'report.json').read_text());assert report['failures']==0 and report['actorRestores']==6 and report['wraps']>=2
    assert (AUDIT/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (AUDIT/'native.log').read_text()
    stable={}
    for name in ['inputs','owner']:
        before=json.loads((AUDIT/f'{name}-before.json').read_text());after=json.loads((AUDIT/f'{name}-after.json').read_text());assert before==after;stable[name]=len(before)
    captures=report['captures'];assert [c['slot'] for c in captures]==[-1,0,1,2,3,4,5,-2]
    catalog=ROOT/'character/marsh-v2/catalog.json';selected={}
    for name in json.loads(catalog.read_text())['body']:
        p=ROOT/name.removeprefix('res://') if name.startswith('res://') else (catalog.parent/name).resolve()
        for state in json.loads(p.read_text())['states']:selected[state['id']]=[(ROOT/f.removeprefix('res://') if f.startswith('res://') else (p.parent/f).resolve()) for f in state['frameFiles']]
    review=BASE/'actor-review-v3';review.mkdir(exist_ok=True);tiles=[];crops=[];source_paths=[]
    for i,c in enumerate(captures):
        source_path=AUDIT/c['sourceFile'];source=Image.open(source_path).convert('RGBA');slot=c['slot']
        options=[ROOT/'character/marsh-v2/frames/bare/idle-east/000.png'] if slot==-1 else selected['walk-east'] if slot==-2 else [BASE/f'candidate-03/{slot:03d}.png']
        match=[p for p in options if np.array_equal(np.array(source),np.array(Image.open(p).convert('RGBA')))];assert len(match)>=1,(i,'submitted source differs');source_paths.append({'capture':i,'path':match[0].relative_to(ROOT).as_posix(),'sha256':sha(match[0])})
        for key in ['file','sourceFile']:shutil.copy2(AUDIT/c[key],review/c[key])
        native=Image.open(AUDIT/c['file']).convert('RGB');x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080);box=(x-100,y-110,x+110,y+30);assert 0<=box[0]<box[2]<=native.width and 0<=box[1]<box[3]<=native.height
        crop=native.crop(box);crop.save(review/f'crop-{i:03d}.png');crops.append(crop)
        tile=Image.new('RGB',(530,260),'#293b40');draw=ImageDraw.Draw(tile);tile.paste(source,(20,48),source);tile.paste(crop,(265,55));draw.text((10,8),c['label']+' / slot'+str(slot),fill='white');draw.text((10,27),'Exact source / native framebuffer crop; staged unselected',fill='#b1d5c6');tiles.append(tile)
    for group in range(2):
        board=Image.new('RGB',(1060,520),'#293b40')
        for i,tile in enumerate(tiles[group*4:group*4+4]):board.paste(tile,((i%2)*530,(i//2)*260))
        board.save(review/f'paired-{group}.png')
    crops[1].save(review/'native-poses.apng',save_all=True,append_images=crops[2:7],duration=[100]*6,loop=0,disposal=1,blend=0)
    for i,f in enumerate(ImageSequence.Iterator(Image.open(review/'native-poses.apng'))):assert np.array_equal(np.array(f.convert('RGB')),np.array(crops[i+1]))
    evidence={'normalAdmission':False,'fullGoalComplete':False,'checks':report['checks'],'failures':0,'engineErrors':0,'exitCode':0,'captures':8,'exactSources':8,'actorPlayerRestores':6,'controlledSamples':len(report['samples']),'wraps':report['wraps'],'strideDistanceCells':report['strideDistanceCells'],'stableBoundedInputs':stable['inputs'],'unchangedOwnerNonLogFiles':stable['owner'],'sourceParity':source_paths,'scope':report['scope'],'visualReviewed':False,'fixturePrecision':'Existing0.001world-unit movement tolerance, no failed East native interval.','nativeApng':'Six exact captured crops,100ms illustrative holds; no realtime moving/contact acceptance.'}
    assessment=review/'visual-assessment.json'
    if assessment.exists():evidence['visualReviewed']=json.loads(assessment.read_text())['allEightViewsInspected']
    (review/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n')
    (review/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Marsh East run staged actor review</title><style>body{background:#182b30;color:#dae8e2;font:16px system-ui;max-width:1300px;margin:25px auto}img{max-width:100%;image-rendering:pixelated}</style><h1>East run: complete alternating stride study</h1><p>Unselected complete authored poses at neutral147occupied calibration, runtime H148. Existing distance cadence and six100ms timing retained. Normal Marsh controller/main/grid/player in a clear furnished room; six actor/player restores and pause holds, two cycle wraps, normal walk slowing.</p><p>Exact held source/native crops below. Side-to-side compression, head/torso/material joins and moving contact remain provisional. No full RunSave/TitleContinue, realtime motion or full family acceptance.</p><p><a href="verification.json">Scoped evidence and retained failed fixture</a> Ã‚Â· <a href="native-poses.apng">Native captured-pose illustration</a></p><img src="paired-0.png"><img src="paired-1.png">''',encoding='utf-8')
    print(json.dumps({k:evidence[k] for k in ['checks','failures','captures','exactSources','actorPlayerRestores','wraps','stableBoundedInputs','unchangedOwnerNonLogFiles','normalAdmission']}))
if __name__=='__main__':main()
