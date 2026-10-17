from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose4-v296';o.mkdir(exist_ok=True)
source=r/'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/004.png'
target=p/'arrival-turn-pose4-v294/edit-target.png';shutil.copy2(target,o/'edit-target.png')
prompt='Edit this single sprite with a restrained material-detail refinement only. Preserve the EXACT existing back-facing three-quarter orientation, head facing away with only the existing tiny edge of ear/cheek visible, torso, backpack, arm/case occlusion, boots, full-body silhouette, scale and canvas position. Do not rotate him toward the viewer. Retain all original equipment shapes and positions: wrench on belt, belt device, case in both hands, backpack, knee and ankle hardware. Refine the charcoal fabric with fine subtle diamond quilting, thin restrained seams and matte worn texture; muted yellow panels and warm worn metal retain the current values. Keep the original small head and limb proportions. No added holsters, badges, tools, shine or brightening. Transparent background. One figure at the exact original placement.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(o/'inputs.json').write_text(json.dumps(dict(pose=4,sourceFile=source.relative_to(r).as_posix(),sourceSha256=sha(source),referenceSha256={(o/'edit-target.png').relative_to(r).as_posix():sha(o/'edit-target.png')},promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(str(o))
