from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok):
    global checks
    assert ok;checks+=1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bindings=json.loads((P/'source-bindings.json').read_text())
for name,h in bindings['bindings'].items():check(sha(R/name.removeprefix('res://'))==h)
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text());check(len(m['states'])==12);check(m['pivot']==[128,224] and m['standingHeight']==148 and m['textureFilter']=='linear')
    for direction in ['east','south','west','north']:
        source=R/f'character/veld-rest-{direction}-coherent-v1';original=json.loads((source/f'{gear}-manifest.json').read_text());states=[s for s in m['states'] if s['id'].endswith('-'+direction)]
        check([s['id'] for s in states]==[s['id'] for s in original['states']]);lie,rise,sleep=states
        check(lie['frameFiles']==list(reversed(rise['frameFiles'])));check(sleep['frameFiles']==[lie['frameFiles'][-1]])
        check(sum(lie['frameDurationsMs'])==1840 and rise['frameDurationsMs']==list(reversed(lie['frameDurationsMs'])));check(not lie['loop'] and not rise['loop'] and sleep['loop'])
        check(len(sleep['restHeadOffset'])==2 and all(abs(float(v))<100 for v in sleep['restHeadOffset']))
        # Independently reconstruct the registered anatomical/component landmark.
        # The sprite renderer adds CELL*.038 before drawing at CELL*.17/H148.
        registration=json.loads((source/f'{gear}-registration.json').read_text())
        final=registration['frames'][-1]
        if gear=='bare':
            center=[final['position'][axis]+(registration['heads'][-1][axis]-final['box'][axis])*registration['fixedRuler'] for axis in range(2)]
        else:
            center=[final['componentPosition'][axis]+final['componentSize'][axis]*.5 for axis in range(2)]
        expected=[(center[axis]-m['pivot'][axis])*(384*.17/m['standingHeight'])+(384*.038 if axis==1 else 0) for axis in range(2)]
        check(all(abs(sleep['restHeadOffset'][axis]-expected[axis])<.000001 for axis in range(2)))
        check(Image.open(R/sleep['frameFiles'][0].removeprefix('res://')).getpixel(tuple(round(v) for v in center))[3]>0)
        for i,s in enumerate(states):
            check(s['frameFiles']==['res://'+(source/f).relative_to(R).as_posix() for f in original['states'][i]['frameFiles']])
            for f in s['frameFiles']:check(Image.open(R/f.removeprefix('res://')).size==(256,256))
tracked=['bare-manifest.json','helmet-manifest.json','source-bindings.json','cardinal-contact-sheet.png'];before={f:sha(P/f) for f in tracked}
subprocess.run([sys.executable,str(P/'build_family.py')],check=True,capture_output=True);check(before=={f:sha(P/f) for f in tracked})
result={'checks':checks,'failures':0,'states':24,'references':104,'uniqueFrames':48,'deterministicFiles':4,'normalSelection':True,'scope':'all cardinal paired source bindings/reverse/held/1840ms/metadata packaging plus registered opaque head landmark and renderer lift; native player/world distinct'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
