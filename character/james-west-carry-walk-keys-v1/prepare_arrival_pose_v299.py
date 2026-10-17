from pathlib import Path
import hashlib,json,shutil
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'arrival-turn-pose3-v299';o.mkdir(exist_ok=True)
source=r/'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north/003.png'
shutil.copy2(p/'arrival-turn-refine-v290/edit-target.png',o/'edit-target.png')
prompt='Refine this single sprite with restrained fine fabric detail only. Preserve the exact existing three-quarter back-left orientation: head points in the same direction as shoulders and hips, only its existing narrow cheek/ear edge visible. Keep original small head, full-body silhouette, limb proportions, boots, scale and canvas placement. Preserve original dark matte brightness throughout, without lifting the charcoal fabric or face highlights. Fine subtle diamond quilting and thin seams, muted yellow panels, warm worn metal. Retain exact existing equipment shapes and locations: case held in both hands, backpack, wrench hanging on belt, belt device, knee and ankle hardware. No added pouches or symbols, no relighting, polish or purple tint. Transparent background, one figure only.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
(o/'inputs.json').write_text(json.dumps(dict(pose=3,sourceFile=source.relative_to(r).as_posix(),sourceSha256=sha(source),referenceSha256={(o/'edit-target.png').relative_to(r).as_posix():sha(o/'edit-target.png')},promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n')
print(str(o))
