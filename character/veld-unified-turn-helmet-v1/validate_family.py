"""Validate actual candidate contracts, protected pixels and cardinal identity."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from registration import MASTER_GASKET_BOTTOM,CLEAR_BOX
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];checks=0
def check(ok):
    global checks
    assert ok;checks+=1
quarters=json.loads((HERE/'quarter-helmet-manifest.json').read_text());half=json.loads((HERE/'half-helmet-manifest.json').read_text());provenance=json.loads((HERE/'family-provenance.json').read_text())
oldstates={}
for pair in ['north-east','east-south','north-west','south-west']:
    m=json.loads((ROOT/f'character/veld-carry-turn-{pair}-consistent-v1/helmet-manifest.json').read_text())
    check(all(quarters[k]==m[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter']))
    oldstates.update({s['id']:s for s in m['states']})
oldhalf=json.loads((ROOT/'character/veld-carry-half-turns-consistent-v1/helmet-manifest.json').read_text())
check(all(half[k]==oldhalf[k] for k in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','textureFilter']))
for m,old in [(quarters,oldstates),(half,{s['id']:s for s in oldhalf['states']})]:
    for s in m['states']:
        check({k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in old[s['id']].items() if k!='frameFiles'})
        for p in s['frameFiles']:
            a=np.array(Image.open(HERE/p).convert('RGBA'));ref=provenance[p];body=ref.get('body',ref.get('previousHalfBody'));b=np.array(Image.open(ROOT/body).convert('RGBA'));mask=np.ones((256,256),bool);mask[65:109,96:169]=False
            check(np.array_equal(a[mask],b[mask]));check(a.shape==(256,256,4));check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20))
        if len(s['frameFiles'])==12:
            check(Image.open(HERE/s['frameFiles'][5]).tobytes()==Image.open(HERE/s['frameFiles'][6]).tobytes())
masters={'north':Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-north.png').convert('RGBA'),'east':Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55)),'south':Image.open(ROOT/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA'),'west':Image.open(ROOT/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA')}
for pair in ['north-east','east-south','north-west','south-west']:
    for i,d in [(0,pair.split('-')[0]),(5,pair.split('-')[1])]:
        head=masters[d];a=np.array(head);y,x=np.where(a[-5:,:,3]>160);center=(x.min()+x.max())/2;pos=(round(128-center),MASTER_GASKET_BOTTOM[d]-head.height);out=Image.open(HERE/f'frames/helmet/carry-turn-{pair}/{i:03}.png').convert('RGBA');b=np.array(out.crop((pos[0],pos[1],pos[0]+head.width,pos[1]+head.height)))
        original=Image.open(ROOT/f'character/veld-carry-turn-{pair}-consistent-v1/frames/helmet/carry-turn-{pair}/{i:03}.png').convert('RGBA');original.paste((0,0,0,0),CLEAR_BOX);original.alpha_composite(head,pos)
        check(original.tobytes()==out.tobytes());check(np.array_equal(a[a[:,:,3]==255],b[a[:,:,3]==255]))
for s in half['states']:
    with Image.open(HERE/f'helmet-{s["id"].removeprefix("carry-turn-")}-v1.gif') as g:
        total=0
        for i in range(g.n_frames):g.seek(i);total+=g.info['duration']
        check(11<=g.n_frames<=12);check(total==sum(s['frameDurationsMs'])*3)
authority=[ROOT/'character/veld-helmet-east-fit-v3/source.png',ROOT/'character/shared-helmet-standard-v1/james-north-reference.png',ROOT/'character/shared-helmet-standard-v1/veld-south-reference.png',ROOT/'character/shared-helmet-standard-v1/veld-west-reference.png']
(HERE/'family-validation.json').write_text(json.dumps({'checks':checks,'failures':0,'masterSources':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in authority},'bodyOutsideHeadExact':True,'originalStateMetadataExact':True,'exactCardinalVisiblePixels':True,'originalRuntimeCyclesMs':{'quarter':800,'half':680},'visualAcceptance':'not established by tests','installed':quarters['status'].startswith('installed'),'ownerVisualAcceptance':'pending'},indent=2)+'\n')
print(f'{checks} candidate contract/pixel/master/GIF checks, 0 failures')
