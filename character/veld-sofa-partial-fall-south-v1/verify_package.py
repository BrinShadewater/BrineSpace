from pathlib import Path
import json,hashlib,subprocess,sys
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check(ok,message):
    global checks
    checks+=1;assert ok,message
reg=json.loads((P/'source-registration.json').read_text())
for name,digest in reg['bindings'].items():check(sha(R/name)==digest,'Exact retained source binding '+name)
paths=list((P/'frames').rglob('*.png'))+[P/f'{g}-manifest.json' for g in ['bare','helmet']]+[P/'source-registration.json',P/'bare-source-review.png',P/'helmet-source-review.png'];before={str(p):sha(p) for p in paths}
run=subprocess.run([sys.executable,str(P/'build.py')],capture_output=True,text=True);check(run.returncode==0,'Local alias/padding rebuild');check(all(sha(Path(p))==h for p,h in before.items()),'Byte-identical packaging')
for gear in ['bare','helmet']:
    manifest=json.loads((P/f'{gear}-manifest.json').read_text());sit=json.loads((R/f'character/veld-seated-south-selected-v1/{gear}-manifest.json').read_text());down=next(s for s in sit['states'] if s['id']=='sit-down-south');rise=next(s for s in sit['states'] if s['id']=='sit-rise-south')
    check([manifest['frameWidth'],manifest['frameHeight'],manifest['standingHeight'],manifest['pivot']]==[256,272,148,[128,224]],'Reviewed fixed profile')
    check(manifest['status']=='staged_candidate' and manifest['sofaPartialFallDeathMode']=='partial-south-v1','Unselected opt-in partial states')
    check(len(manifest['states'])==6,'All6partial entrances')
    for pose,state in enumerate(manifest['states']):
        check(state['id']==f'death-sofa-pose{pose}-south','Exact named partial state')
        check(state['frameDurationsMs']==([180,160,180,180,220,500] if pose<2 else [180,180,200,220,240,500]) and not state['loop'] and state['terminalFrame']==5,'Finite authored clock')
        first=Image.open(R/state['frameFiles'][0].removeprefix('res://')).convert('RGBA').crop((0,0,256,256))
        for path in [down['frameFiles'][pose],rise['frameFiles'][5-pose]]:check(first.tobytes()==Image.open(R/path.removeprefix('res://')).convert('RGBA').tobytes(),'Exact selected down/reverse-rise entrance')
        for path in state['frameFiles']:
            check(path.startswith('res://character/'),'Whole source path');image=Image.open(R/path.removeprefix('res://')).convert('RGBA');box=image.getbbox();check(image.size==(256,272) and box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'Unclipped shared canvas')
        for index in [4,5]:
            body=Image.open(R/state['frameFiles'][index].removeprefix('res://')).convert('RGBA').crop((0,0,256,256))
            terminal=Image.open(R/f'character/veld-death-ground-south-coherent-v1/frames/{gear}/death-ground-south/{index:03}.png').convert('RGBA')
            check(body.tobytes()==terminal.tobytes(),'Exact canonical floor endpoints')
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'normalSelection':False,'scope':'fixed canvas/ruler, all6exact down/rise sources, finite clocks, retained floor endpoints/source bindings and byte-identical packaging; native joins separate'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0}))
