from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'standing-step-video-v2-native';D=P/'native-cycle-art-repair-v1';D.mkdir(exist_ok=True)
atlas=Image.new('RGBA',(1792,1536));bindings={};slots=list(range(16,54))
for index,n in enumerate(slots):
 source=S/'global-standing-ruler-v1/frames'/f'{n:03}.png';im=Image.open(source).convert('RGBA')
 atlas.alpha_composite(im,((index%7)*256,(index//7)*256));bindings[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
master=R/'character/veld-east-held-original-master-v1/frames/bare/000.png'
atlas.alpha_composite(Image.open(master).convert('RGBA'),((38%7)*256,(38//7)*256));bindings[master.relative_to(R).as_posix()]=hashlib.sha256(master.read_bytes()).hexdigest()
atlas.save(D/'whole-cycle-edit-target.png')
(D/'INPUT.json').write_text(json.dumps({'columns':7,'rows':6,'cellSize':[256,256],'motionCells':38,'sourceRawSlots':slots,'originalStandingRulerCell':38,'transparentCells':[39,40,41],'bindings':bindings,'roles':'Cells0..37 are whole-source motion targets, cell38 actual original master calibration/appearance authority, cells39..41 blank. Separate original-native4x reference is appearance authority. Entire source packing only, no anatomy/colour edits.','scope':'Full bilateral38pose guide and exact original standing reference; authoring input only, not artwork/contact/normal runtime acceptance.'},indent=2)+'\n',encoding='utf-8')
print('Complete38pose cycle plus original master packed into7x6 transparent guide.')
