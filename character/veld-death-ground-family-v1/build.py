"""Resolve all four staged dry-collapse sources without changing selection."""
from pathlib import Path
import json,copy,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
DIRS=['east','west','north','south'];bound={};reports={};checks=0;manifests={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok):
    global checks
    assert ok;checks+=1
for gear in ['bare','helmet']:
    states=[];header=None
    for direction in DIRS:
        folder=R/f'character/veld-death-ground-{direction}-coherent-v1'
        m=json.loads((folder/f'{gear}-manifest.json').read_text());s=copy.deepcopy(m['states'][0])
        if header is None:header=copy.deepcopy(m)
        require(all(m.get(k)==header.get(k) for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter']))
        require(s['id']=='death-ground-'+direction and len(s['frameFiles'])==6 and not s['loop'] and s['terminalFrame']==5)
        require(s['frameDurationsMs']==[180,160,180,180,220,500] and s['waterPoses']==[False]*6 and s['facings']==[direction]*6)
        hashes=json.loads((folder/('frame-hashes.json' if direction=='east' else f'{gear}-frame-hashes.json')).read_text());files=[]
        for i,name in enumerate(s['frameFiles']):
            f=folder/name;im=Image.open(f)
            require(im.mode=='RGBA' and im.size==(256,256));require(sha(f)==hashes[name])
            files.append('res://'+f.relative_to(R).as_posix());bound[f.relative_to(R).as_posix()]=sha(f)
        if direction=='east':
            master=R/('character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png' if gear=='bare' else 'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png')
        else:
            reg=json.loads((folder/f'{gear}-registration.json').read_text())
            master=R/reg['idle' if gear=='bare' else 'helmetIdle']
        entry=Image.new('RGBA',(256,256));entry.alpha_composite(Image.open(master).convert('RGBA'),(36,52))
        require(entry.tobytes()==Image.open(folder/s['frameFiles'][0]).tobytes())
        bound[master.relative_to(R).as_posix()]=sha(master)
        packpath=folder/('verification.json' if direction=='east' else 'paired-verification.json')
        pack=json.loads(packpath.read_text())
        native_path=R/f'output/veld-death-ground-{direction}-candidate-v1/validation.json'
        native=json.loads(native_path.read_text());evidence_name='paired-candidate-evidence.json' if direction=='west' else 'candidate-evidence.json'
        evidence=json.loads((folder/evidence_name).read_text());stored=evidence.get('files',evidence.get('sha256',{}))
        require((pack['passed'] if direction=='east' else pack['failures']==0) and native['returnCode']==0)
        for f in [R/f'output/veld-death-ground-{direction}-candidate-v1/native.log',R/f'tests/test_veld_death_ground_{direction}_candidate.gd']:
            require(stored[f.relative_to(R).as_posix()]==sha(f));bound[f.relative_to(R).as_posix()]=sha(f)
        reports[direction]={'packagingChecks':pack['checks'],'playerChecks':70,'runnerPassed':native['passed'],'realProfileChanges':native['realProfileChanges'],'scope':'per-direction source/player proof; actual death/Continue/world joins unproven'}
        for f in [folder/f'{gear}-manifest.json',packpath,native_path]:bound[f.relative_to(R).as_posix()]=sha(f)
        s['frameFiles']=files;states.append(s)
    header.update(name='Veld staged cardinal dry-collapse '+gear,status='staged_family_actual_entry_continue_world_pending',deathEntryMode='lowered-start-v1',states=states)
    manifests[gear]=header;(P/f'{gear}-manifest.json').write_text(json.dumps(header,indent=2)+'\n')
board=Image.new('RGBA',(1536,8*256),'#202a30');draw=ImageDraw.Draw(board)
for gi,gear in enumerate(['bare','helmet']):
    for di,direction in enumerate(DIRS):
        for i,file in enumerate(manifests[gear]['states'][di]['frameFiles']):
            frame=Image.open(R/file.removeprefix('res://')).convert('RGBA');at=(i*256,(gi*4+di)*256)
            board.alpha_composite(frame,at);draw.text((at[0]+5,at[1]+5),f'{direction} / {gear} / {i}',fill='white')
board.save(P/'all-cardinal-poses.png');board.resize((852,1136),Image.Resampling.LANCZOS).save(P/'station-scale-contact.png')
report={'checks':checks,'failures':0,'states':8,'references':48,'normalSelection':False,'sourceReports':reports,'boundFiles':bound,'scope':'combined source paths/exact master entries/current hash-bound per-direction evidence; combined player/world proof separate'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks':checks,'states':8,'references':48,'normalSelection':False}))
