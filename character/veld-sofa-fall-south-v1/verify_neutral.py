"""Independent exact protected-body checks and reproducible neutral packaging."""
from pathlib import Path
import json,hashlib,subprocess,sys
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v,m):
    global checks
    checks+=1;assert v,m
reg=json.loads((P/'neutral-registration.json').read_text())
for path,digest in reg['bindings'].items():check(sha(R/path)==digest,'Frozen patch/source binding '+path)
paths=[P/f'{g}-neutral-manifest.json' for g in ['bare','helmet']]+list((P/'frames').rglob('*.png'))+[P/'neutral-registration.json',P/'neutral-source-review.png']
before={str(p):sha(p) for p in paths}
run=subprocess.run([sys.executable,str(P/'build_neutral.py')],capture_output=True,text=True)
check(run.returncode==0,'Local neutral build')
check(all(sha(Path(p))==h for p,h in before.items()),'All original and neutral frames byte-identical rebuild')
for gear in ['bare','helmet']:
    m=json.loads((P/f'{gear}-neutral-manifest.json').read_text());s=m['states'][0]
    check([m['frameWidth'],m['frameHeight'],m['standingHeight'],m['pivot']]==[256,272,148,[128,224]],'Reviewed body ruler')
    check(s['id']=='death-sofa-neutral-south' and m['status']=='staged_candidate','Unselected neutral branch')
    check(s['frameDurationsMs']==[180,180,200,220,240,500] and not s['loop'],'Same finite supported fall clock')
    entry=Image.open(R/f'character/veld-read-seated-south-coherent-v1/frames/{gear}/read-seated-south/000.png').convert('RGBA')
    first=Image.open(R/s['frameFiles'][0].removeprefix('res://')).convert('RGBA')
    check(first.crop((0,0,256,256)).tobytes()==entry.tobytes(),'Exact current neutral entrance')
    common=json.loads((P/f'{gear}-manifest.json').read_text())['states'][0]
    for slot in [3,4,5]:check(s['frameFiles'][slot]==common['frameFiles'][slot],'Exact whole-source alias, brace/floor')
    for slot,pose in [(1,2),(2,3)]:
        record=next(r for r in reg['patches'] if r['gear']==gear and r['sourcePose']==pose)
        x0,y0,x1,y1=record['nativeWindow'];mask=np.ones((272,256),bool);mask[y0:y1,x0:x1]=False
        original=np.array(Image.open(R/common['frameFiles'][slot].removeprefix('res://')).convert('RGBA'))
        changed=np.array(Image.open(R/s['frameFiles'][slot].removeprefix('res://')).convert('RGBA'))
        check(np.array_equal(original[mask],changed[mask]),'Unchanged whole head/helmet/remaining body outside explicit window')
        check(not np.array_equal(original,changed),'Authored patch actually differs')
    for path in s['frameFiles']:
        check(path.startswith('res://character/'),'Whole source path')
        im=Image.open(R/path.removeprefix('res://')).convert('RGBA');box=im.getbbox()
        check(im.size==(256,272) and box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'Shared canvas, unclipped body')
(P/'neutral-package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'normalSelection':False,'visualScope':'source inspection separate; no world/save acceptance'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0}))
