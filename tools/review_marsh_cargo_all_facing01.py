"""Cross-reference complete figures and stage eight source states, no admission."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';O=B/'all-facing-01-cross-review';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
states=[];rows=[];records=[]
for f in ['south','north','east','west']:
    S=B/'sources';r=json.loads((S/f'{f}-unload-01.request.json').read_text());P=B/f'{f}-unload-01-unselected';m=json.loads((P/'manifest.json').read_text())
    assert sha(S/f'{f}-unload-01.raw.png')==r['rawSha256'] and sha(Path(r['originalGeneratedPath']))==r['rawSha256']
    for s in m['states']:
        assert len(s['frameFiles'])==4 and s['frameDurationsMs']==[130]*4 and not s['loop']
        assert all(n.startswith('res://') for n in s['frameFiles'])
        states.append(s)
    unload=P/f'unload-{f}';pickup=P/f'pickup-{f}'
    assert sha(unload/'000.png')==r['sourceFrames'][1]['sha256'] and sha(unload/'003.png')==r['sourceFrames'][0]['sha256']
    assert all(sha(pickup/f'{i:03}.png')==sha(unload/f'{3-i:03}.png') for i in range(4))
    images=[ROOT/r['sourceFrames'][0]['path'],ROOT/r['sourceFrames'][1]['path'],P/'intermediate-1.png',P/'intermediate-2.png',P/'ruler.png']
    row=Image.new('RGB',(1840,430),'#293b40');d=ImageDraw.Draw(row)
    for i,(p,label) in enumerate(zip(images,['selected idle PRIMARY','staged carry endpoint','whole half-lowering','whole floor lowering','neutral diagnostic'])):
        im=Image.open(p).convert('RGBA');large=im.resize((368,368),Image.Resampling.NEAREST);row.paste(large,(i*368,45),large);d.text((i*368+5,7),f+' / '+label,fill='white');records.append({'facing':f,'label':label,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    rows.append(row)
for i,pair in enumerate(['south-north','east-west']):
    board=Image.new('RGB',(1840,860),'#293b40');board.paste(rows[i*2],(0,0));board.paste(rows[i*2+1],(0,430));board.save(O/f'{pair}-whole.png')
assert len(states)==8 and sum(len(s['frameFiles']) for s in states)==32
(O/'family-manifest.json').write_text(json.dumps({'revision':'marsh-cargo-held-family01-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'states':8,'frameSlots':32,'wholeFigures':20,'figures':records,'operations':'Whole figures nearest review only; no raster edits. Eight source states referenced with whole literal res paths and original metadata, exact carry/idle endpoints and full pixel-order reversal. Source coverage is not art/runtime/save/Continue acceptance.'},indent=2)+'\n');print('8states/32slots,20whole-figure cross-review,all endpoints and reversals exact')
