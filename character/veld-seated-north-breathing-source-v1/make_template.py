from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
raw=Image.open(P.parent/'veld-seated-north-coherent-v1/sources/badge-edit-v2.png').convert('RGBA')
pose=raw.crop((1137,614,1336,987))
sheet=Image.new('RGBA',(1536,1024))
for row in range(2):
 for col in range(3):sheet.alpha_composite(pose,(col*512+156,row*512+90))
sheet.save(P/'sources/locked-neutral-template-v2.png')
