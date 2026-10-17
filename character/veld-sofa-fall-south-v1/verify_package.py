"""Source contract checks, independent endpoints and reproducible packaging."""
from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(value,message):
    global checks
    checks+=1
    assert value,message
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reg=json.loads((P/'registration.json').read_text())
for path,digest in reg['bindings'].items():check(sha(R/path)==digest,'Frozen source/master/component binding '+path)
paths=[P/f'{g}-manifest.json' for g in ['bare','helmet']]+list((P/'frames').rglob('*.png'))+[P/'material-grade.json',P/'registration.json',P/'paired-source-review.png']
before={str(p):sha(p) for p in paths}
result=subprocess.run([sys.executable,str(P/'build.py')],capture_output=True,text=True)
check(result.returncode==0,'Deterministic build')
check(all(sha(Path(p))==digest for p,digest in before.items()),'Byte-identical local packaging')
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
    check([m['frameWidth'],m['frameHeight'],m['standingHeight'],m['pivot']]==[256,272,148,[128,224]],'Shared profile')
    check(m['status']=='staged_candidate' and m['sofaFallDeathMode']=='reader-south-v1','Staged opt-in source')
    check(s['frameDurationsMs']==[180,180,200,220,240,500] and not s['loop'] and s['terminalFrame']==5,'Finite death clock')
    check(sum(s['frameDurationsMs'])==1520,'1.52 second terminal')
    for path in s['frameFiles']:
        check(path.startswith('res://character/veld-sofa-fall-south-v1/frames/'),'Whole source path')
        im=Image.open(R/path.removeprefix('res://')).convert('RGBA')
        check(im.size==(256,272),'Shared canvas')
        box=im.getbbox();check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'No clipped silhouette')
    first=Image.open(R/s['frameFiles'][0].removeprefix('res://')).convert('RGBA')
    entry=Image.open(R/f'character/veld-read-seated-south-coherent-v1/frames/{gear}/read-seated-south/003.png').convert('RGBA')
    check(first.crop((0,0,256,256)).tobytes()==entry.tobytes(),'Exact selected reader entrance')
    for slot in [4,5]:
        frame=Image.open(R/s['frameFiles'][slot].removeprefix('res://')).convert('RGBA')
        source=Image.open(R/f'character/veld-death-ground-south-coherent-v1/frames/{gear}/death-ground-south/{slot:03}.png').convert('RGBA')
        check(frame.crop((0,0,256,256)).tobytes()==source.tobytes(),'Retained same-ruler floor endpoint')
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'normalSelection':False,'scope':'source/manifests, paired exact endpoints, raw/master/component bindings, no clipping and deterministic packaging; visual/world acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'normalSelection':False}))
