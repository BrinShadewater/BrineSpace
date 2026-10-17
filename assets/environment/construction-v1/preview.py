"""Compile native captured frames, preserving their physical pixel scale."""
from pathlib import Path
from PIL import Image
import json,math
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'output/construction-art-v1'
size=float(json.loads((OUT/'capture-geometry.json').read_text())['cell_size'])
box=(math.floor(size)-8,math.floor(size)-8,math.ceil(size*4)+8,math.ceil(size*3)+8)
frames=[Image.open(OUT/f'motion-{i:02}.png').convert('RGB').crop(box) for i in range(20)]
frames[0].save(OUT/'building-animation-v1.gif',save_all=True,append_images=frames[1:],duration=[500]*19+[1500],loop=0,disposal=2)
sheet=Image.new('RGB',(frames[0].width*3,frames[0].height*2),'#233b41')
for j,i in enumerate([0,3,6,10,14,19]):sheet.paste(frames[i],((j%3)*frames[i].width,(j//3)*frames[i].height))
sheet.save(OUT/'building-stages-v1.png')
print('Native animation:',frames[0].size,'20 frames; physical pixels preserved')
