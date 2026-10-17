from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
for phase,version in [(35,215),(36,216)]:
 out=p/f'lower-material-phase{phase}-v{version}'
 prompt=f'''Edit Image1 only with a restrained matte surface-finish correction. This is the fixed lower-body crop of James carrying while walking west, phase{phase}. Image2 is the original master's charcoal quilting and worn warm silver hardware: material reference only.
Keep every existing toe, heel, sole, ankle and strap at exactly its Image1 coordinates. The feet are separating: the boot on the left points left, while the boot on the right retains its diagonal down-left toe and raised up-right heel. Preserve their different angles, exact spacing and near/far layering. No rotation, no straightening, no enlargement, no repositioning, no new fittings. Preserve calf shapes and knee positions. The previous failed edit of an adjacent frame turned the boots into another pose; do not do that here.
Reduce the large bright toe-plate and ankle-fitting reflections to subdued warm silver/gray. Preserve small readable highlights and fine existing metal edges, charcoal quilting and illustrated detail. Match the master's matte worn material rather than shiny white metal. Do not brighten the fabric, thicken outlines, smooth away hardware, introduce black shadow masses or purple/magenta. Recolor existing surfaces only; do not redraw anatomy or copy any reference pose.
Return the identical 1024x1024 crop composition with actual transparency, no background, glow, text, additional limbs or full figure. Preserve original illustrated sprite density, no pixel-art conversion.'''
 (out/'prompt.txt').write_text(prompt,encoding='utf-8')
 d=json.loads((out/'inputs.json').read_bytes());d['promptSha256']=hashlib.sha256((out/'prompt.txt').read_bytes()).hexdigest();d['generationReferenceRoles']=['edit-target.png','master-metal-reference.png']
 (out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
