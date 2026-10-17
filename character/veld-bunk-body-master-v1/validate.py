"""Manifest/reference integrity and master entry/canvas calibration admission."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
bare=json.loads((P/'bare-manifest.json').read_text());helmet=json.loads((P/'helmet-manifest.json').read_text());original=json.loads((R/'character/dr-veld-v2/supplemental/bunk-east/bare/manifest.json').read_text())
for m in [bare,helmet]:
    assert m['pivot']==[128,224] and m['standingHeight']==148 and m['canvas']==[256,272] and m['precomposed'];checks+=1
    settle=next(s for s in m['states'] if s['id']=='death-bunk-settle-east')
    assert m['supportedBunkDeathMode']=='settle-v1' and not settle['loop'];checks+=1
    assert settle['frameFiles']==m['states'][0]['frameFiles'][2:]+m['states'][3]['frameFiles'][1:];checks+=1
    assert settle['frameDurationsMs']==[300,300,300,300,280,280,420] and settle['depthOffsets']==[96,96,100,100,100,100,100] and settle['furnitureFrames']==['','','bunk','bunk','bunk','bunk','bunk'];checks+=1
    for i,s in enumerate(m['states'][:3]):
        assert {k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in original['states'][i].items() if k!='frameFiles'};checks+=1
    for s in m['states']:
        assert len(s['frameFiles'])==len(s['frameDurationsMs']) and all(d>0 for d in s['frameDurationsMs']);checks+=1
        for f in s['frameFiles']:
            assert f.startswith('res://character/veld-bunk-body-master-v1/');p=R/f.removeprefix('res://');im=Image.open(p);assert im.mode=='RGBA' and im.size==(256,272);checks+=1
            a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>0);checks+=1
for g,source in [('bare','character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'),('helmet','character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png')]:
    out=Image.open(P/f'frames/{g}/bunk-enter-east/000.png').convert('RGBA');ref=Image.open(R/source).convert('RGBA');assert out.crop((36,52,220,236)).tobytes()==ref.tobytes();checks+=1
    assert Image.open(P/f'frames/{g}/bunk-enter-east/006.png').tobytes()==Image.open(P/f'frames/{g}/death-bunk-east/000.png').tobytes();checks+=1
    assert Image.open(P/f'frames/{g}/death-bunk-east/001.png').tobytes()==Image.open(P/f'frames/{g}/death-bunk-east/002.png').tobytes();checks+=1
files=[p for p in (P/'frames').rglob('*.png')]
normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text(encoding='utf-8') for gear in ['bare','helmet'])
result={'checks':checks,'failures':0,'exports':len(files),'referencedFrames':sum(len(s['frameFiles']) for m in [bare,helmet] for s in m['states']),'normalSelection':normal_selection,'sourceChecks':json.loads((P/'bare-registration.json').read_text())['checks'],'helmetChecks':json.loads((P/'helmet-registration.json').read_text())['checks'],'bindings':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'source/package integrity and exact master entry calibration; native/world/lifecycle/visual acceptance separate'}
(P/'package-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(f'{checks}manifest/path/pivot/timing/master-entry checks,0failures;{len(files)}RGBA exports')
