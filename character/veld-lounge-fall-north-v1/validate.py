from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;bindings={}
def check(ok,msg):
 global checks
 checks+=1
 assert ok,msg
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text());s=m['states'][0]
 check(m.get('loungeFallDeathMode')=='seated-north-v1','Explicit lounge mortality opt-in')
 check(m['pivot']==[128,224] and m['standingHeight']==148,'Master ruler/pivot')
 check(s['id']=='death-lounge-seated-north' and len(s['frameFiles'])==6,'Seated finite family')
 check(s['frameDurationsMs']==[180,180,180,180,220,500] and not s['loop'] and s['terminalFrame']==5,'Finite authored timing')
 check(s['furnitureFrames']==['']*6 and s['depthOffsets']==[0]*6,'No unsupported fixed furniture layering')
 for f in s['frameFiles']:
  path=R/f.removeprefix('res://');im=Image.open(path);a=np.array(im);box=im.getbbox()
  check(im.mode=='RGBA' and im.size==(256,272),'Complete RGBA canvas')
  check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'No cropped anatomy')
  check(np.all(a[0,:,3]==0) and np.all(a[-1,:,3]==0),'Transparent edges')
  bindings[f.removeprefix('res://')]=hashlib.sha256(path.read_bytes()).hexdigest()
 first=Image.open(P/f'frames/{gear}/death-lounge-seated-north/000.png').convert('RGBA')
 source=Image.open(R/f'character/veld-seated-north-coherent-v1/frames/{gear}/sit-down-north/005.png').convert('RGBA')
 check(first.crop((0,0,256,256)).tobytes()==source.tobytes(),'Exact staged master-aligned seated entrance')
 for index,old in [(3,3),(4,4),(5,5)]:
  actual=Image.open(P/f'frames/{gear}/death-lounge-seated-north/{index:03}.png').convert('RGBA')
  previous=Image.open(R/f'character/veld-death-ground-north-coherent-v1/frames/{gear}/death-ground-north/{old:03}.png').convert('RGBA')
  check(actual.crop((0,0,256,256)).tobytes()==previous.tobytes(),'Exact established floor brace/roll/terminal')
for i,pose in [(1,2),(2,3)]:
 bare=np.array(Image.open(P/f'frames/bare/death-lounge-seated-north/{i:03}.png'))
 helmet=np.array(Image.open(P/f'frames/helmet/death-lounge-seated-north/{i:03}.png'))
 region=np.load(P/f'helmet-protected-pose-{pose}.npy')
 check(np.array_equal(bare[~region],helmet[~region]),'Body unchanged outside canonical head insert')
reg=json.loads((P/'registration.json').read_text());check(reg['fixedRuler']==148/693,'One anatomical ruler for both new interiors')
component=R/reg['helmetComponent']
check(Image.open(component).size==(32,29),'Existing rear depth-pitch component at native scale')
check(hashlib.sha256(component.read_bytes()).hexdigest()==reg['helmetComponentSha256'],'Canonical rear helmet component binding')
for r in reg['records']:
 if r['gear']=='helmet':check(r['helmetNativeScale']==1 and r['helmetPitchDegrees']==40,'Rear helmet pitches in depth rather than changing design')
grade=json.loads((P/'material-grade.json').read_text());check(set(grade)=={'skin','hair','science','neutral'},'Shared semantic master material grade')
normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text() for gear in ['bare','helmet'])
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'builderChecks':reg['checks'],'exports':12,'newInteriorPosesPerGear':2,'normalSelection':normal_selection,'scope':'North source artwork/package checks; combined normal-loader mortality/Continue evidence in ../veld-north-chair-falls-selected-v1','bindings':bindings},indent=2)+'\n',encoding='utf-8')
print(f'{checks} source/endpoint/helmet/alpha checks,0failures;12exports')
