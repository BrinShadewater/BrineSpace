from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose2-v297';o.mkdir(exist_ok=True)
source=r/'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/002.png'
shutil.copy2(p/'arrival-turn-pose2-v293/edit-target.png',o/'edit-target.png')
prompt='Refine this single game sprite with subtle fine material detail only. Preserve the EXACT original partly side-facing orientation and head direction, compact head size, shoulder and hip angle, full-body silhouette, case position, limb lengths, boots, scale and canvas placement. He is in the early part of a turn from left-facing toward facing away; preserve this existing early angle, not a full back view. Keep all original equipment shapes, locations and occlusion: wrench on belt, one belt device, case in both hands, backpack, knee and ankle hardware. Charcoal cloth has fine subtle diamond quilting, thin restrained seams, matte worn texture. Muted yellow panels and warm worn metal retain original brightness. No extra holster, new insignia, shine, colour shift or brightening. Transparent background; only this one figure at the same placement.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(o/'inputs.json').write_text(json.dumps(dict(pose=2,sourceFile=source.relative_to(r).as_posix(),sourceSha256=sha(source),referenceSha256={(o/'edit-target.png').relative_to(r).as_posix():sha(o/'edit-target.png')},promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(str(o))
