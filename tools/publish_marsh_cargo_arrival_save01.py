"""Publish normal-catalogue before/Continue pairs for the arrival checkpoint gate."""
from pathlib import Path
import json, shutil
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'output/marsh-animation-audit/cargo-arrival-save-01-2026-10-02'
O=ROOT/'character/marsh-cargo-held-material-v1/arrival-save-01-actor-review'
read=lambda p:json.loads(p.read_text())
r=read(A/'report.json')
assert r['failures']==0 and len(r['cases'])==4 and len(r['captures'])==8
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
for name in ['inputs','owner']:assert read(A/f'{name}-before.json')==read(A/f'{name}-after.json')
O.mkdir(exist_ok=True)
board=Image.new('RGB',(2120,520),'#293b40')
for i,c in enumerate(r['captures']):
    source=Image.open(A/c['sourceFile']).convert('RGBA')
    native=Image.open(A/c['file']).convert('RGB')
    x=round(c['canvasPosition'][0]*native.width/1920);y=round(c['canvasPosition'][1]*native.height/1080)
    crop=native.crop((x-100,y-110,x+110,y+30))
    tile=Image.new('RGB',(530,260),'#293b40');d=ImageDraw.Draw(tile)
    tile.paste(source,(20,48),source);tile.paste(crop,(265,55))
    d.text((10,8),c['label']+(' / checkpoint' if i<4 else ' / visible Continue'),fill='white')
    d.text((10,27),'CURRENT normal catalogue; staged artwork not loaded',fill='#b1d5c6')
    board.paste(tile,((i%4)*530,(i//4)*260))
    for key in ['file','sourceFile']:shutil.copy2(A/c[key],O/c[key])
    if i>=4:
        before=Image.open(A/r['captures'][i-4]['sourceFile']).convert('RGBA')
        assert before.tobytes()==source.tobytes()
board.save(O/'before-continue-pairs.png')
v={'checks':r['checks'],'failures':0,'fullCheckpoints':4,'freshVisibleTitleContinues':4,'sourceNativePairs':8,'stableBoundedInputs':len(read(A/'inputs-before.json')),'unchangedOwnerNonLogFiles':len(read(A/'owner-before.json')),'normalCatalogue':True,'stagedArtworkAdmission':False,'fullGoalComplete':False,'scope':r['scope'],'visualReviewed':(O/'visual-assessment.json').exists()}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps(v))
