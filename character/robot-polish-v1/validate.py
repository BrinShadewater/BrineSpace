from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
report={}
for who,expected in [('josh',76),('river',68)]:
    pack=json.loads((ROOT/who/'manifest.json').read_text());old=json.loads((ROOT/who/'baseline.json').read_text())
    states={s['id']:s for s in pack['states']};assert len(states)==expected
    assert set(states)=={s['id'] for s in old['states']}
    assert pack['standingHeight']==148 and pack['strideDistanceCells']['walk']==.1
    colors=set();count=0
    for key,s in states.items():
        assert len(s['frameFiles'])==len(s['frameDurationsMs']) and all(t>0 for t in s['frameDurationsMs'])
        for f in s['frameFiles']:
            im=Image.open(ROOT/f).convert('RGBA');assert im.size==(184,184)
            b=im.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<184 and b[3]<184,(key,b)
            a=np.array(im);assert set(np.unique(a[:,:,3]))<={0,255};colors.update(map(tuple,a[a[:,:,3]>0,:3]));count+=1
    def pixels(key,i):return Image.open(ROOT/states[key]['frameFiles'][i]).tobytes()
    for d in ['south','west','north','east']:
        assert len({pixels('walk-'+d,i) for i in range(4)})==4
        assert all(Image.open(ROOT/f).getbbox()[3]==172 for f in states['walk-'+d]['frameFiles'])
        for action in (['watch','turn','torch','powerdown'] if who=='josh' else ['scan','inspect']):
            assert pixels(action+'-enter-'+d,0)==pixels('idle-'+d,0)
            assert pixels(action+'-exit-'+d,-1)==pixels('idle-'+d,0)
        for to in ['south','west','north','east']:
            if to!=d:
                assert pixels('turn-'+d+'-'+to,0)==pixels('idle-'+d,0)
                assert pixels('turn-'+d+'-'+to,-1)==pixels('idle-'+to,0)
        if who=='josh':assert len(states['powerdown-'+d]['frameFiles'])==1
    groupkeys=[]
    for path in (ROOT/who/'packs').glob('*/manifest.json'):
        part=json.loads(path.read_text());assert part['standingHeight']==148
        for s in part['states']:
            groupkeys.append(s['id'])
            for f in s['frameFiles']:assert (path.parent/f).is_file(),f
    assert set(groupkeys)==set(states) and len(groupkeys)==len(states)
    for s in old['states']:
        root=REPO/'character'/('companion-water-v1/river' if s['id'].startswith('float-') else 'animation-expansion-v5/'+(who if s['id'] in [r['id'] for r in json.loads((ROOT/who/'packs/locomotion/manifest.json').read_text())['states']] else who+'-actions'))
        original=json.loads((root/'manifest.json').read_text());orig=next(v for v in original['states'] if v['id']==s['id'])
        for a,b in zip(s['frameFiles'],orig['frameFiles']):assert (ROOT/a).read_bytes()==(root/b).read_bytes()
    assert len(colors)>64
    report[who]=dict(states=expected,frameReferences=count,opaqueColors=len(colors),coverage='complete',baselineUnchanged=True)
sources=json.loads((ROOT/'review/build-report.json').read_text())['sources']
for name,digest in sources.items():assert hashlib.sha256((ROOT/'sources'/name).read_bytes()).hexdigest()==digest
(ROOT/'review/validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
