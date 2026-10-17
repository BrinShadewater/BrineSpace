from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,msg):
 global checks
 checks+=1
 assert ok,msg
b=json.loads((P/'source-bindings.json').read_text())
for path,digest in b['bindings'].items():check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'Original source binding')
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text())
 check(m.get('loungeFallDeathMode')=='late-north-v1','Explicit late floor opt-in')
 check(m['pivot']==[128,224] and m['standingHeight']==148,'Master ruler/pivot')
 check(len(m['states'])==2,'Both late entrance sources')
 for s,pose in zip(m['states'],[3,4]):
  check(s['id']==f'death-lounge-late{pose}-north','Exact pose-specific selector')
  check(s['frameDurationsMs']==[180,180,180,180,220,500] and not s['loop'] and s['terminalFrame']==5,'Finite authored source clock')
  for i,f in enumerate(s['frameFiles']):
   im=Image.open(R/f.removeprefix('res://'));a=np.array(im);box=im.getbbox()
   check(im.mode=='RGBA' and im.size==(256,272),'Registered complete source canvas')
   check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'Complete uncropped anatomy')
   check(np.all(a[0,:,3]==0) and np.all(a[-1,:,3]==0),'Transparent boundary')
   if i==0:
    old=Image.open(R/f'character/veld-seated-north-coherent-v1/frames/{gear}/sit-down-north/{pose:03}.png').convert('RGBA')
    check(im.crop((0,0,256,256)).tobytes()==old.tobytes(),'Exact live partial seat entrance pixels')
   else:check(f==f'res://character/veld-lounge-fall-north-v1/frames/{gear}/death-lounge-seated-north/{i:03}.png','Exact original authored slump/landing, no grading or resampling')
normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text() for gear in ['bare','helmet'])
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'builderChecks':b['checks'],'newPaddedFrames':4,'references':24,'normalSelection':normal_selection,'scope':'Exact late3/late4 joins and original authored source binding; native review separate'},indent=2)+'\n')
print(f'{checks} package/source/alpha checks,0failures;24references/4newpadded entrances')
