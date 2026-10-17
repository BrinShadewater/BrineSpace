"""Consolidate exact independently authored action references without repainting."""
from pathlib import Path
import copy,json,hashlib
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=0;inputs=[];hashes={}
for gear in ['bare','helmet']:
    states=[]
    board=Image.new('RGBA',(1536,2240),'#202a30');draw=ImageDraw.Draw(board)
    for di,direction in enumerate(['east','west','north','south']):
        folder=H.parent/f'veld-salvage-pickup-{direction}-coherent-v1'
        p=folder/f'{gear}-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
        fit=json.loads((folder/'fit-checks.json').read_text(encoding='utf-8'))
        native=json.loads((folder/'native-candidate-v1-checks.json').read_text(encoding='utf-8'))
        assert native['failures']==0 and native['engine_errors']==[] and native['real_profile_changed_files']==[];checks+=1
        inputs.append(dict(gear=gear,direction=direction,manifestSha256=sha(p),fitSha256=sha(folder/'fit-checks.json'),nativeSha256=sha(folder/'native-candidate-v1-checks.json')))
        for si,s in enumerate(copy.deepcopy(m['states'])):
            files=[]
            for i,f in enumerate(s['frameFiles']):
                source=folder/f;rel='../'+folder.name+'/'+f;files.append(rel);hashes[rel]=sha(source)
                assert hashes[rel]==fit['frameHashes'][f]==native['frameHashes'][f];checks+=1
                im=Image.open(source).convert('RGBA');board.alpha_composite(im,(i*256,(di*2+si)*280+20));draw.text((i*256+4,(di*2+si)*280+4),s['id']+' '+str(i),fill='white')
            s['frameFiles']=files;states.append(s)
    manifest=dict(name='Veld underwater sample work/pickup '+gear,frameWidth=256,frameHeight=256,pivot=[128,128],standingHeight=148,textureFilter='linear',precomposed=True,status=('installed_locally_pending_full_set_polish' if json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'))['actionOverrides'].get('veld-scientific-samples')=='character/veld-salvage-pickup-family-coherent-v1/bare-manifest.json' else 'staged_pending_controller_turn_world_joins'),states=states)
    (H/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');board.save(H/f'{gear}-family-contact-v1.png')
(H/'family-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=manifest['status'].startswith('installed'),inputs=inputs,frameHashes=hashes,scope='Exact96 action refs bound to reviewed source fits and per-direction native evidence; actual controller/world separate'),indent=2)+'\n',encoding='utf-8')
print(f'{checks} consolidation checks PASS;16 paired action states/96 exact references')
