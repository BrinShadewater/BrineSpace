from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
bindings=json.loads((P/'source-bindings.json').read_text(encoding='utf-8'))
for filename,digest in bindings['sha256'].items():
 check(hashlib.sha256((ROOT/filename.removeprefix('res://')).read_bytes()).hexdigest()==digest,'source/frame binding '+filename)
registry=json.loads((P.parent/'ACTIVE_ASSETS.json').read_text(encoding='utf-8'))
loader=(ROOT/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 check(m['status']=='installed_runtime_reviewed','installed status')
 check(registry['actionOverrides' if gear=='bare' else 'equipmentOverrides']['bill-dry-recovery-family']==f'character/bill-recover-air-family-v1/{gear}-manifest.json','registry selection')
 check(f'res://character/bill-recover-air-family-v1/{gear}-manifest.json' in loader,'normal loader selection')
 check(m['pivot']==[128,224] and m['standingHeight']==148,'dry plane')
 check({s['id'] for s in m['states']}=={'recover-air-'+d for d in ['east','west','north','south']},'cardinal coverage')
 for s in m['states']:
  check(len(s['frameFiles'])==6 and s['frameDurationsMs']==[500]*6 and not s['loop'],'three-second finite recovery')
  check(s['waterPoses']==[False]*6 and s['waterKinds']==['recover']*6,'dry recovery')
  check(all(f.startswith('res://character/') for f in s['frameFiles']),'whole literal paths')
  images=[Image.open(ROOT/f.removeprefix('res://')).convert('RGBA') for f in s['frameFiles']]
  check(all(im.size==(256,256) for im in images),'frame planes')
  check(images[0].tobytes()==images[-1].tobytes(),'identical idle endpoints')
report={'passed':True,'checks':checks,'gearStates':8,'frameRefs':48,'scope':'consolidation bindings/cardinal dry clock/plane/endpoints;individual native evidence separate;selected native controller/restore evidence separate'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(f'{checks} recovery family consolidation checks PASS')
