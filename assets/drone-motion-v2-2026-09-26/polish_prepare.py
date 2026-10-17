from PIL import Image
from pathlib import Path
r=Path('assets/drone-motion-v2-2026-09-26'); p=r/'polish';p.mkdir(exist_ok=True)
b=Image.new('RGBA',(2048,1024))
for i,h in enumerate(['north','northeast','east','southeast','south','southwest','west','northwest']):
 im=Image.open(r/'poses'/f'{h}.png').convert('RGBA').resize((512,512),Image.Resampling.NEAREST); b.alpha_composite(im,((i%4)*512,(i//4)*512))
b.save(p/'heading-edit-target.png')
