from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-coherent-v327';o.mkdir(exist_ok=True)
start=r/'character/james-cargo-half-turns-v1/frames/bare/carry-turn-south-north/010.png'
last=r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/005.png'
master=r/'character/branforth-west-direct-v2/master-input.png'
seed=Image.new('RGBA',(768,768))
for i in range(9):seed.paste(Image.open(start if i<8 else last).convert('RGBA'),((i%3)*256,(i//3)*256))
seed.resize((1254,1254),Image.Resampling.NEAREST).save(o/'layout-input.png')
prompt='''Create a coherent nine-frame game sprite animation by editing the supplied square 3-by-3 sprite grid. Read frames left to right, top to bottom. Preserve exactly the grid arrangement, common scale, canvas spacing, floor line and rear-facing North perspective. Image 1 is the registered layout and endpoint identity. Image 2 is the original character master, authority for soft curved quilted graphite fabric, restrained warm metal, muted engineering yellow, fine detail, matte finish and character proportions; its side view is material reference only. Image 3 shows the current unload motion to improve, not approved anatomy.

James gently lowers the equipment case he is carrying in front of himself to the floor just ahead of his boots, releases it, then straightens smoothly. Nine poses: 1 upright carrying; 2 slight knee and hip flexion; 3 modest forward bend; 4 lowering case; 5 lowest point, a shallow controlled bend; 6 releasing case; 7 half risen; 8 almost upright; 9 fully standing. All poses face directly away from the viewer. His boots remain planted in their original narrow stance, knees track over boots, neither leg bends sideways. Keep body volume, backpack dimensions, belt wrench location, head size and suit construction consistent through the whole sequence. Keep the wrench on his belt; his hands handle only the case. The case ends on the floor in front of him, partly visible between his legs from behind. This is a cargo unload, no torch or tablet. Enough intermediate rise poses to avoid a snap upward. Preserve original master curved soft quilting, avoid coarse diamond armor or bright glossy surfaces. Each character fits its own cell, soles at the same relative height, no camera rotation, cropping, stretching, pose-dependent scaling or foot sliding. Transparent background, no grid lines, lettering, shadows or scenery. Match the source endpoint standing height and registration; do not enlarge the figures to fill each cell.'''
(o/'prompt.txt').write_text(prompt)
refs=[o/'layout-input.png',master,p/'arrival-pacing-v326/bare-chronology.png']
(o/'generation-inputs.json').write_text(json.dumps(dict(mode='built-in imagegen',refs=[dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in refs],promptSha256=hashlib.sha256(prompt.encode()).hexdigest(),normalChanged=False),indent=2)+'\n')
print(str(o))
