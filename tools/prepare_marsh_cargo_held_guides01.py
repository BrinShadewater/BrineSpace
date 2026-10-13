"""Audit selected unload and derived pickup against own staged cargo endpoints."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';S.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(p,n):return (ROOT/n.removeprefix('res://') if n.startswith('res://') else p.parent/n).resolve()
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]={'state':state,'manifest':p,'frames':[resolve(p,n) for n in state['frameFiles']]}
records={}
g=json.loads((ROOT/'character/marsh-carry-turn-material-v1/sources/guide-provenance.json').read_text())
for facing in ['south','north','east','west']:
    data=selected['unload-'+facing];old=data['frames'];idle=ROOT/g['primaryIdles'][facing]['path'];cargo=ROOT/g['stagedEndpoints'][facing]['path']
    paths=[cargo,*old,idle];board=Image.new('RGB',(1472,415*((len(paths)+3)//4)),'#293b40');d=ImageDraw.Draw(board)
    for i,p in enumerate(paths):
        f=Image.open(p).convert('RGBA');assert f.size==(184,184);f=f.resize((368,368),Image.Resampling.NEAREST);x=(i%4)*368;y=(i//4)*415;board.paste(f,(x,y+35),f);d.text((x+4,y+5),'Staged carry endpoint' if i==0 else 'Selected idle PRIMARY' if i==len(paths)-1 else f'Old selected unload{i-1} / motion only',fill='white')
    q=S/f'{facing}-held-motion-review.png'
    if q.exists():assert Image.open(q).convert('RGB').tobytes()==board.tobytes(),'existing guide differs'
    else:board.save(q)
    body=S/f'{facing}-body-primary.png';Image.open(idle).convert('RGBA').resize((736,736),Image.Resampling.NEAREST).save(body)
    endpoint=S/f'{facing}-cargo-endpoint.png';Image.open(cargo).convert('RGBA').resize((736,736),Image.Resampling.NEAREST).save(endpoint)
    pickup=selected['pickup-'+facing];assert len(pickup['frames'])==len(old)==4
    assert all(Image.open(a).convert('RGBA').tobytes()==Image.open(b).convert('RGBA').tobytes() for a,b in zip(pickup['frames'],reversed(old)))
    records[facing]={'selectedUnloadManifest':data['manifest'].relative_to(ROOT).as_posix(),'manifestSha256':sha(data['manifest']),'timing':{k:v for k,v in data['state'].items() if k not in ['id','frameFiles']},'selectedUnloadFrames':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in old],'selectedPickupFrames':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in pickup['frames']],'selectedPickupTiming':{k:v for k,v in pickup['state'].items() if k not in ['id','frameFiles']},'pickupReverseWholePixelsExact':True,'primaryIdle':g['primaryIdles'][facing],'stagedCargoEndpoint':g['stagedEndpoints'][facing],'guides':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [q,body,endpoint]]}
(S/'guide-provenance.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'catalogSha256':sha(cat),'facings':records,'pickupRuntime':'Current orderedcatalog selects FOUR pickup andunload frames at130ms each=520;pickup wholepixels reverse unload exactly for all4facings. crew_life.gd legacy load_into defines a sixduration reverse helper,not evidence of selected Marsh runtime contract. Grid replacementloader reads orderedcatalog. Preserve selected4frame timing unless motion authoring deliberately revises it;verify actual runtime before adoption.','runtimeDependencies':[{'path':n,'sha256':sha(ROOT/n)} for n in ['scripts/crew_life.gd','scripts/bill_npc.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd']],'scope':'Whole old-unload motion boards+own stagedcargo/primarybody guides only;not authored replacement or pickup/unload/native acceptance.'},indent=2)+'\n')
print(json.dumps({'selectedUnloadFrames':{f:len(r['selectedUnloadFrames']) for f,r in records.items()},'guides':12,'normalAdmission':False}))
