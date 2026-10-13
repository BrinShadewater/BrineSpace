"""Freeze a whole-pose request with explicit foreground/rear support identity."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-east-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prompt='''Create TWO complete adult Marsh figures facing RIGHT, true transparent background, generous separation. Figure ONE reproduces the complete leg arrangement in reference ONE: the visible foreground thigh runs down toward the LEFT/rear knee and rear boot, which is raised; the partly hidden far thigh runs down toward the RIGHT/front knee and front boot, which bears weight. Keep that exact near/far overlap order. The far supporting boot is under the pelvis. The foreground knee passes LOW beneath the pelvis, with its boot slightly raised behind. Bend both elbows for a gentle running passing moment, small forward lean. Compact stride, relaxed low knee, all limbs anatomically connected. Figure TWO is the unchanged neutral standing pose of reference TWO.

Reference TWO controls BOTH figures' adult anatomy, head and collar size, fitted chest, equipment, matte warm pixel density and material colours. Reference THREE is the original identity: blond adult profile and small metal device at visible right temple. Same elevated right-side camera, same scale and head/body proportions in both figures. Warm ivory suit panels and boot uppers, muted sage shoulders and pouches, slate joints, charcoal gloves and soles. Plain unadorned slate ankle bands exactly as reference TWO. Quiet crisp pixel clusters, restrained warm shading. Two complete figures from hair to soles, neutral calibrated to 147 occupied rows at production size; calibrate the whole sheet once from neutral. Natural slight compression in moving pose. Transparent empty space around every silhouette, no ground, cast shadow, glow, labels or text.'''
path=BASE/'farpass-05.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
refs=[BASE/'selected-walk3-only.png',BASE/'selected-idle0-only.png',ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png']
request={'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'sheetGrid':[2,1],'transparentBackground':True}
(BASE/'farpass-05.request.json').write_text(json.dumps(request,indent=2)+'\n')
print('Frozen05 prompt and three ordered reference hashes.')
