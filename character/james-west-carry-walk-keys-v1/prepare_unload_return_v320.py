from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-return-original-v320';o.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
refs=[p/'north-unload-return-source-v316/edit-target.png',p/'north-unload-start-source-v309/original-master-cloth-reference.png']
prompt='Edit Image1, a rear-view empty-handed unloading return. Image1 alone defines the exact bent pose, camera, anatomy, head position, canvas placement and boot support. Keep its silhouette and every joint/boot position; do not straighten, raise, lower, enlarge or shorten the man. Retain the case on the floor in front of him, visible between his lower legs, and the empty hands. The wrench remains on the right belt and the meter on the left. Refine the coarse blurry clothing rendering using Image2 ONLY as the original master fabric reference: subdued matte charcoal with fine softly curved quilt stitching, restrained worn warm metal cuffs and leg bands, muted ochre yellow. Keep Image1 backpack panels, emblem, straps, gear sizes and placements. Avoid large hard diamond quilting, bright white cuffs, gloss, purple grade and deep black patches around hands/backpack. Clean tiny colored edge artifacts. Preserve transparent background and the same square canvas. This is a surface-detail repair, not a new pose.'
(o/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
original=r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/004.png'
(o/'inputs.json').write_text(json.dumps(dict(originalTarget=original.relative_to(r).as_posix(),originalTargetSha256=sha(original),references={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(o/'prompt.txt'),normalChanged=False),indent=2)+'\n',encoding='utf-8')
print('320 original pose and actual master cloth references frozen.')
