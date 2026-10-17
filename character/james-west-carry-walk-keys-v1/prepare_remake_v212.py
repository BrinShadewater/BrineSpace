from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;out=p/'lower-material-phase34-v212'
prompt='''Edit Image1 with a very small surface-finish correction only. This is the fixed lower-body crop of James carrying while walking west, phase34. Image2 is original-master charcoal quilting and worn warm silver hardware, a material reference only.
Retain every shape in Image1 at exactly its current coordinates: both boots point diagonally down-left, both heels remain up-right, the soles slope upward to the right. Do not turn either boot into a horizontal side view. Do not spread the feet, straighten ankles, rotate soles, move the toe armor or change any joint or strap. The last attempted edit incorrectly rotated and moved the boots. The only acceptable edit preserves the complete original pose and construction.
Gently subdue the brightest existing toe-plate and ankle-strap reflections to warm gray. Keep the same illustrated detail, fine metal edges, charcoal fabric and matte worn finish. Do not redesign hardware, add rivets, thicken outlines or create black masses. No purple or magenta. No pose transfer from any reference. Preserve exact transparency and crop composition, 1024x1024. No background, text, extra limbs or full figure. This is a restrained recoloring of existing surfaces, not a redraw.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
d=json.loads((out/'inputs.json').read_bytes());d['promptSha256']=hashlib.sha256((out/'prompt.txt').read_bytes()).hexdigest()
d['generationReferenceRoles']=['edit-target.png','master-metal-reference.png'];d['remakeOf']='lower-material-phase34-v210'
(out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(prompt)
