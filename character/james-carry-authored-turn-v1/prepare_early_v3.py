from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
common=(p/'early-prompt.txt').read_text(encoding='utf-8').split('\n\n',1)[1]
prompt='''EDIT TARGET: supplied SOUTH FRONT James. Turn the entire carried pose a SMALL20degrees toward the LEFT EDGE OF THE IMAGE. Absolute screen landmarks: nose tip shifts toward image LEFT, visible near ear lies on the RIGHT side of the head; shoulder on image RIGHT is slightly nearer/larger, shoulder on image LEFT slightly farther/narrower. Case center and nose point slightly LEFT, never RIGHT. Both eyes still visible and chest mostly frontal. Head/torso/hips/knees/case rotate together by only20degrees. DO NOT face image right. Preserve front target stocky proportions, head size, figure height, camera, matte grade and boot baseline. The supporting words LEFT refer to the physical LEFT edge of the canvas, not the character's anatomical left. No mirroring: anatomical-right wrench stays correct far-side belt, anatomical-left meter correct nearer belt.

'''+common
(p/'early-v3-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[p/'south-reference.png',p/'early-v3-prompt.txt',Path(__file__)]
(p/'early-v3-inputs.json').write_text(json.dumps({'preCallSha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'targetAngleDegrees':20,'sourceCanvas':[256,256],'standingRuler':148,'pivot':[128,224],'selected':False,'scope':'Nearest-cardinal early pose with explicit nose/ear/shoulder screen landmarks to correct wrong yaw; no mirroring.'},indent=2)+'\n',encoding='utf-8')
print('Early wrong-yaw revision uses explicit left-edge nose/right-edge ear landmarks; prompt/input hashes frozen.')
