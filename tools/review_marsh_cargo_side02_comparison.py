"""Whole original/redraw comparison and private family metadata, no raster repair."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';O=B/'side02-cross-review';O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[];rows=[];neutral_rows=[]
for f in ['east','west']:
    old=B/f'{f}-unload-01-unselected';new=B/f'{f}-unload-02-unselected';r=json.loads((B/'sources'/f'{f}-unload-02.request.json').read_text())
    paths=[old/'intermediate-1.png',new/'intermediate-1.png',old/'intermediate-2.png',new/'intermediate-2.png',ROOT/r['sourceFrames'][1]['path'],ROOT/r['sourceFrames'][0]['path']]
    labels=['01 half lowering','02 whole redraw half','01 floor lowering','02 whole redraw floor','exact staged carry endpoint','selected idle PRIMARY']
    row=Image.new('RGB',(2208,430),'#293b40');d=ImageDraw.Draw(row)
    for i,(p,label) in enumerate(zip(paths,labels)):
        im=Image.open(p).convert('RGBA');large=im.resize((368,368),Image.Resampling.NEAREST);row.paste(large,(i*368,45),large);d.text((i*368+4,6),f+' / '+label,fill='white');records.append({'facing':f,'label':label,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    rows.append(row)
    row=Image.new('RGB',(1104,430),'#293b40');d=ImageDraw.Draw(row)
    for i,(p,label) in enumerate(zip([ROOT/r['sourceFrames'][0]['path'],old/'ruler.png',new/'ruler.png'],['selected PRIMARY','01 neutral','02 neutral'])):
        im=Image.open(p).convert('RGBA');large=im.resize((368,368),Image.Resampling.NEAREST);row.paste(large,(i*368,45),large);d.text((i*368+4,6),f+' / '+label,fill='white');records.append({'facing':f,'label':label,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
    neutral_rows.append(row)
for name,width,stack in [('whole-pose-comparison.png',2208,rows),('neutral-comparison.png',1104,neutral_rows)]:
    board=Image.new('RGB',(width,860),'#293b40');board.paste(stack[0],(0,0));board.paste(stack[1],(0,430));board.save(O/name)
states=[]
for f,revision in [('south','01'),('north','01'),('east','02'),('west','02')]:
    m=json.loads((B/f'{f}-unload-{revision}-unselected/manifest.json').read_text())
    for s in m['states']:
        assert len(s['frameFiles'])==4 and s['frameDurationsMs']==[130]*4 and not s['loop'] and all(p.startswith('res://') for p in s['frameFiles'])
        states.append(s)
assert len(states)==8
(O/'family-manifest.json').write_text(json.dumps({'revision':'marsh-cargo-held-family02-unselected','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
(O/'verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeFigures':18,'states':8,'slots':32,'sourceParity':records,'scope':'Whole01/02 complete-figure comparisons and private SouthNorth01/EastWest02 family metadata only. No normal catalog selection or full family acceptance.'},indent=2)+'\n');print('18whole comparison figures,private8state32slot family02; originals preserved')
