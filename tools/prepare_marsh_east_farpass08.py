"""Direct complete06 edit: keep its correct foreground trailing leg."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
prompt='''Edit reference ONE's COMPLETE two-figure sheet. Preserve its LEFT figure's leg overlap exactly: the large foreground ivory thigh remains slanted backward toward the LEFT/rear knee, with the other thigh partly hidden behind it slanting toward the RIGHT/front knee. Keep this arrangement; do not reverse the legs. Re-author the complete LEFT figure in that same pose with a SMALL bend of the LEFT/rear knee, lifting the whole LEFT/rear boot about eight production pixels higher than the RIGHT/front boot. Flatten the RIGHT/front boot onto the floor beneath the pelvis. The right/front FAR leg is the weight-bearing leg; the left/rear foreground leg is lifted. This is a restrained passing pose, not a lifted thigh or kick. Keep thighs low, short stride. Preserve complete head/torso/arms/camera and leg connections. The RIGHT figure remains its neutral ruler.

Reference TWO selected idle is the authority for anatomy and grade: same fitted adult, small head, quiet warm matte pixels, ivory/sage/slate/charcoal suit. Reference THREE original East master confirms blond identity, visible right-temple plate and small authentic ankle buckles. Closely match selected idle body and drawing density while keeping reference ONE's whole leg order. Two complete figures, one common neutral scale, genuine transparent empty background and separation. No floor, shadow, glow or text.'''
path=BASE/'farpass-08.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
refs=[BASE/'farpass-06.raw.png',BASE/'selected-idle0-only.png',ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png']
(BASE/'farpass-08.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],'sheetGrid':[2,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen08 direct complete06 leg-order edit request.')
