from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose2-v301';o.mkdir(exist_ok=True)
source=r/'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/002.png'
shutil.copy2(p/'arrival-turn-pose2-v293/edit-target.png',o/'edit-target.png')
prompt='Edit this single sprite into the NEXT increment of its planted turn: rotate his entire head, shoulders, torso, hips and both boots together about twenty degrees farther away from the viewer, turning from left-facing toward back-facing. The backpack becomes more visible, chest less visible, face narrower in projection; remain an EARLY three-quarter angle with the left profile still visible, not full back. Case stays in both hands in front of his waist, with natural partial occlusion. No twisting the head independently. Keep EXACT original canvas occupancy, crown height, boot-sole baseline, small head and limb proportions. Feet pivot close under hips without stepping or sticking a foot out. Preserve original equipment design and matte dark colour values: backpack, one belt device, wrench hanging on belt, case, knee/ankle hardware; no added pockets or badges. Fine subtle diamond quilt, restrained seams, muted yellow panels and worn warm metal; no brightness lift or purple tint. One complete figure on transparent background.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(o/'inputs.json').write_text(json.dumps(dict(pose=2,sourceFile=source.relative_to(r).as_posix(),sourceSha256=sha(source),referenceSha256={(o/'edit-target.png').relative_to(r).as_posix():sha(o/'edit-target.png')},promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(str(o))
