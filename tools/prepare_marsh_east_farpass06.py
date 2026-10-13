"""Whole selected stance plus neutral, at identical scale and registration."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
refs=[BASE/'selected-walk3-only.png',BASE/'selected-idle0-only.png']
board=Image.new('RGBA',(1472,736));records=[]
for i,path in enumerate(refs):
    f=Image.open(path).convert('RGBA');assert f.size==(736,736)
    board.alpha_composite(f,(i*736,0));records.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'offset':[i*736,0]})
target=BASE/'farpass-06-whole-selected-guide.png';board.save(target)
(BASE/'farpass-06-guide.json').write_text(json.dumps({'operation':'Two unchanged complete nearest4x selected figures, same736canvas/scale/foot registration; no anatomy edits','sources':records,'sha256':sha(target)},indent=2)+'\n')
prompt='''Re-author this entire transparent two-figure sprite guide as a closely matched complete two-figure sheet. Preserve the exact leg silhouette, overlap order, and foot positions of the LEFT figure. Its large foreground thigh is on the LEFT, connects to the LEFT rear knee and raised LEFT rear boot; the RIGHT/front supporting leg is partly hidden behind it. Keep those exact legs. Make the left figure a restrained running passing moment by bending both elbows, hands close to the waist, and a small forward torso lean. The knees stay low. Keep the RIGHT figure in its unchanged neutral standing pose. Both figures retain exactly the same fitted adult build, small blond head, body/limb size, collar, harness, equipment, boot construction, warm matte pixel grade and elevated right-facing camera as this guide. Reference TWO is the original own East master and controls the visible small right-temple metal device and identity. Plain suit details exactly as the guide. Reproduce TWO WHOLE connected figures with wide transparent separation from hair to soles. One common scale, neutral ruler preserved, complete quiet pixel clusters; transparent empty background throughout.'''
path=BASE/'farpass-06.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
ordered=[target,ROOT/'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png']
(BASE/'farpass-06.request.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'status':'frozen before generation','promptSha256':sha(path),'orderedReferences':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in ordered],'sheetGrid':[2,1],'transparentBackground':True},indent=2)+'\n')
print('Frozen whole selected stance/neutral guide and exact06 request.')
