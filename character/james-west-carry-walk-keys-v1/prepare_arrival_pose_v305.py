from pathlib import Path
from PIL import Image
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose1-v305';o.mkdir(exist_ok=True)
source=p/'arrival-turn-pose1-v304/fixed-canvas-source.png';shutil.copy2(p/'arrival-turn-pose1-v304/raw.png',o/'edit-target.png')
master=r/'character/branforth-west-direct-v2/master-input.png';Image.open(master).crop((530,115,710,280)).save(o/'original-master-face-reference.png')
prompt='Edit ONLY the facial identity in image1 to match James in image2, which is a FACE REFERENCE CROP, not an alternative pose or canvas. James is the older grey-haired mechanic with the distinctive thick grey downward moustache, weathered cheek and brow, sideburns, small nose profile and goggles resting on his forehead. Restore that moustache and older face in image1 at its EXISTING small head size and current early-turn facing angle. Keep current crown/head outline, torso, limbs, matte dark colour grade, clothing, backpack with gear emblem, belt device, wrench hanging on belt, held case, hands, boots, whole silhouette and exact canvas position. Do not resize, rotate or relight the character, change head orientation, add gear or make his face bright. Only restore this original facial likeness. One complete figure on transparent background.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
refs=[o/'edit-target.png',o/'original-master-face-reference.png',master]
(o/'inputs.json').write_text(json.dumps(dict(pose=1,sourceFile=source.relative_to(r).as_posix(),sourceSha256=sha(source),referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},masterFaceCrop=[530,115,710,280],promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n');print(str(o))
