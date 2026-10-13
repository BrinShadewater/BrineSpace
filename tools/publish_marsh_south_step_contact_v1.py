"""Freeze actual normal-source route evidence and retained failed contact study."""
from pathlib import Path
import json,hashlib,shutil,math
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-v2/supplemental/south-step-contact-v1'
OUT=BASE/'world-review';OUT.mkdir(exist_ok=True)
OLD=ROOT/'output/marsh-animation-audit/south-step-normal-world-v1-2026-10-03'
NEW=ROOT/'output/marsh-animation-audit/south-step-normal-world-v2-2026-10-03'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
failed=read(OLD/'report.json');r=read(NEW/'report.json')
assert (failed['checks'],failed['failures'])==(874,24)
assert (r['checks'],r['failures'],len(r['captures']),len(r['samples']),r['normalActorRestores'])==(874,0,44,176,6)
assert (NEW/'native-exit.txt').read_text().strip()=='0' and (OLD/'native-exit.txt').read_text().strip()=='1'
for audit in [OLD,NEW]:
    for kind in ['owner','inputs']:assert read(audit/f'{kind}-before.json')==read(audit/f'{kind}-after.json')
assert not any(m in (NEW/'native.log').read_text() for m in ['ERROR:', 'WARNING:', 'SCRIPT ERROR'])
errors=[line for line in (OLD/'native.log').read_text().splitlines() if line.startswith('ERROR:')]
assert len(errors)==24 and all(line=='ERROR: right supporting depth planted before transfer' for line in errors)
before=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json')['states']
after=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json')['states']
assert set(before)==set(after) and [k for k in before if before[k]!=after[k]]==['walk-step-south']
a,b=before['walk-step-south'],after['walk-step-south'];sa=dict(a['state']);sb=dict(b['state']);sa.pop('frameFiles');sb.pop('frameFiles')
assert sa==sb and a['pivot']==b['pivot'] and a['standingHeight']==b['standingHeight']
assert [i for i,(f,g) in enumerate(zip(a['frames'],b['frames'])) if f!=g]==[3]
tiles=[];parity=[]
# Observed in complete1600x900 native capture; all prescribed starts identical.
box=(400,190,550,340)
for c in r['captures']:
    source=Image.open(NEW/c['sourceFile']).convert('RGBA')
    selected=ROOT/after[c['key']]['frames'][c['slot']]['path']
    assert source.size==(184,184) and source.tobytes()==Image.open(selected).convert('RGBA').tobytes()
    assert c['foot'][0]==8176 and 7712<=c['foot'][1]<=7719
    native=Image.open(NEW/c['file']).convert('RGB');assert native.size==(1600,900)
    tile=Image.new('RGB',(360,224),'#293b40');draw=ImageDraw.Draw(tile)
    draw.text((3,4),c['label']+' / '+str(c['slot']),fill='white')
    tile.paste(source,(0,30),source);tile.paste(native.crop(box),(202,46))
    tiles.append(tile)
    for key in ['file','sourceFile']:shutil.copy2(NEW/c[key],OUT/c[key])
    parity.append({'key':c['key'],'slot':c['slot'],'source':selected.relative_to(ROOT).as_posix(),'sourceSha256':sha(selected),'nativeFile':c['file'],'nativeSha256':sha(NEW/c['file'])})
boards=[]
for page in range(math.ceil(len(tiles)/8)):
    batch=tiles[8*page:8*page+8];board=Image.new('RGB',(1440,224*math.ceil(len(batch)/4)),'#293b40')
    for i,t in enumerate(batch):board.paste(t,((i%4)*360,(i//4)*224))
    p=OUT/f'route-{page:02}-pairs.png';board.save(p);boards.append({'file':p.name,'sha256':sha(p),'pairs':len(batch),'actuallyInspected':False})
first=next(c for c in failed['captures'] if c['key']=='walk-step-south' and c['slot']==3)
corrected=next(c for c in r['captures'] if c['key']=='walk-step-south' and c['slot']==3)
comparison=Image.new('RGB',(720,224),'#293b40');draw=ImageDraw.Draw(comparison)
for i,(audit,c,label) in enumerate([(OLD,first,'Before: supporting sole1sourcepixel up'),(NEW,corrected,'After: whole drawingY+1')]):
    source=Image.open(audit/c['sourceFile']).convert('RGBA');native=Image.open(audit/c['file']).convert('RGB')
    comparison.paste(source,(360*i,30),source);comparison.paste(native.crop(box),(360*i+202,46));draw.text((360*i+3,4),label,fill='white')
comparison.save(OUT/'contact-before-after.png')
shutil.copy2(OLD/'report.json',OUT/'failed-v1-report.json')
v={'checks':874,'failures':0,'samples':176,'captures':44,'normalActorRestores':6,'stableInputs':len(read(NEW/'inputs-before.json')),'unchangedOwnerFiles':len(read(NEW/'owner-before.json')),'failedV1':{'checks':874,'failures':24,'stableInputs':len(read(OLD/'inputs-before.json')),'unchangedOwnerFiles':len(read(OLD/'owner-before.json')),'soleDepthErrorWorld':65.28/148},'nativeCrop':box,'cropScope':'Fixed whole neighborhood observed from first complete native capture; full native originals retained. No crop/scale of artwork.','sourceParity':parity,'boards':boards,'comparison':{'file':'contact-before-after.png','sha256':sha(OUT/'contact-before-after.png'),'actuallyInspected':False},'scope':r['scope'],'normalAdmission':True,'fullGoalComplete':False,'continuousCadenceReviewed':False}
(OUT/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
print('874checks/0failures,176samples/44exact native-source pairs/6actor restores;5319inputs/2931owner stable;6route boards+before-after prepared')
