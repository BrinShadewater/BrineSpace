from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
checks=0
def check(ok,msg):
 global checks
 checks+=1
 assert ok,msg
bindings={}
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text())
 check(m.get('earlyBunkFloorDeathMode')=='floor-v1','Explicit early floor selector opt-in')
 check(m['canvas']==[256,272] and m['pivot']==[128,224] and m['standingHeight']==148,'Declared original body ruler/pivot')
 for state in m['states']:
  check(not state['loop'] and state['terminalFrame']==len(state['frameFiles'])-1,'Finite terminal')
  check(len(state['frameFiles'])==len(state['frameDurationsMs'])==len(state['depthOffsets'])==len(state['furnitureFrames']),'Complete per-frame metadata')
  check(all(x=='' for x in state['furnitureFrames']) and all(x==0 for x in state['depthOffsets']),'Floor contact family, no false bunk support')
  for f in state['frameFiles']:
   path=R/f.removeprefix('res://');im=Image.open(path)
   check(im.mode=='RGBA' and im.size==(256,272),'Whole RGBA canvas')
   box=im.getbbox();check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272,'No clipped limbs')
   a=np.array(im);check(np.all(a[0,:,3]==0) and np.all(a[-1,:,3]==0),'Transparent perimeter')
   bindings[f.removeprefix('res://')]=hashlib.sha256(path.read_bytes()).hexdigest()
 key='death-bunk-crouch-east'
 first=Image.open(P/f'frames/{gear}/{key}/000.png').convert('RGBA')
 incoming=Image.open(R/f'character/veld-bunk-body-master-v1/frames/{gear}/bunk-enter-east/001.png').convert('RGBA')
 check(first.tobytes()==incoming.tobytes(),'Exact current crouching entrance')
 last=Image.open(P/f'frames/{gear}/{key}/004.png').convert('RGBA')
 terminal=Image.open(R/f'character/veld-death-ground-east-coherent-v1/frames/{gear}/death-ground-east/005.png').convert('RGBA')
 check(last.crop((0,0,256,256)).tobytes()==terminal.tobytes(),'Exact current floor terminal')
 for i in range(6):
  exported=Image.open(P/f'frames/{gear}/death-bunk-standing-east/{i:03}.png').convert('RGBA')
  original=Image.open(R/f'character/veld-death-ground-east-coherent-v1/frames/{gear}/death-ground-east/{i:03}.png').convert('RGBA')
  check(exported.crop((0,0,256,256)).tobytes()==original.tobytes(),'Standing source retained at original pivot')
for i,pose in enumerate([2,3,4],1):
 bare=np.array(Image.open(P/f'frames/bare/death-bunk-crouch-east/{i:03}.png'))
 helmet=np.array(Image.open(P/f'frames/helmet/death-bunk-crouch-east/{i:03}.png'))
 protected=np.load(P/f'helmet-protected-pose-{pose}.npy')
 check(np.array_equal(bare[~protected],helmet[~protected]),'Suit/limbs unchanged outside canonical head insert')
reg=json.loads((P/'registration.json').read_text());check(reg['fixedRuler']==148/495,'One ruler for all generated poses')
grade=json.loads((P/'material-grade.json').read_text());check(set(grade)=={'skin','hair','science','neutral'},'Pooled semantic palette mapping')
for kind in grade:check(grade[kind]['sourcePixels']>30 and grade[kind]['masterPixels']>5,'Nonempty master material authority')
normal_selection=all(f'"res://{P.relative_to(R).as_posix()}/{gear}-manifest.json"' in (R/'scripts/grid_canvas.gd').read_text(encoding='utf-8') for gear in ['bare','helmet'])
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceBuilderChecks':reg['checks'],'exports':22,'generatedInteriorPosesPerGear':3,'normalSelection':normal_selection,'scope':'Source package checks; combined normal-loader contact/mortality/Continue evidence in ../veld-bunk-selected-v1','bindings':bindings},indent=2)+'\n')
print(f'{checks} package/alpha/source/body/endpoint checks,0failures;22 RGBA exports')
