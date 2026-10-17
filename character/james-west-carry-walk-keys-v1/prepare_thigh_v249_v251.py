from pathlib import Path
import subprocess,json,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
for phase,version in [(0,249),(47,250),(3,251)]:
 subprocess.run(['C:/Python314/python.exe',str(p/'prepare_thigh_neighbors.py'),str(phase),str(version)],check=True,capture_output=True)
 if phase==0:
  out=p/'thigh-construction-phase0-v249';base=p/'thigh-construction-phase0-v244';d=json.loads((out/'inputs.json').read_bytes())
  Image.open(base/'bare-head-protected.png').convert('RGBA').crop(d['cropBox']).resize((1024,1024),Image.Resampling.NEAREST).save(out/'edit-target.png')
  prompt='''Edit Image1 only, the fixed40x40 James phase0 thigh crop with corrected quilt construction. Image2 is original-master charcoal quilt and muted yellow seam material, not a pose or pattern-placement reference. Preserve the existing diamond quilting, its seams, stitch positions, narrow yellow seam, original thigh outlines, knee fittings and all overlap precisely. The charcoal fabric is slightly too bright compared with adjacent corrected poses. Reduce ONLY the charcoal upper-thigh fabric midtone brightness by approximately one eighth, keeping it warm dark charcoal with subtle matte quilting. Preserve the same small quilt stitches; no stronger ridges or new contrast. Keep the muted yellow seam unchanged in colour, position and thickness. Do not brighten or change the metal knee plates, belt fittings, hands or case. Correction region native sprite x112..140,y145..163, relative crop x8..36,y9..27. No added panels, pockets, tools, rivets, gold decoration, black masses, purple or body resizing. Return identical1024x1024 crop registration with real transparency, same pose, no background/text/glow/pixel-art conversion.'''
  (out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
  d.update(baseFolder=base.relative_to(r).as_posix(),sourceSha256={f.relative_to(r).as_posix():sha(f) for f in [base/'bare-head-protected.png',base/'helmet-head-protected.png',r/'character/branforth-west-direct-v2/master-input.png']},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in [out/'edit-target.png',out/'master-quilt-reference.png']},promptSha256=sha(out/'prompt.txt'),remakeOf=244)
  (out/'inputs.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('Prepared phase0 fabric correction and neighbouring47/3 construction.')
