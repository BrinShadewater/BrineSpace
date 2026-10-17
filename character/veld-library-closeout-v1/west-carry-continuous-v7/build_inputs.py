from pathlib import Path
from PIL import Image
P=Path(__file__).resolve().parent
reference=P.parent/'west-carry-master-match-v5/frames/bare/000.png'
im=Image.open(reference).convert('RGBA')
for name in ['first','last']:
 im.save(P/f'{name}-native.png')
 big=im.resize((768,768),Image.Resampling.LANCZOS)
 background=Image.new('RGB',(768,768),(12,18,24));background.paste(big,(0,0),big)
 background.save(P/f'{name}-input.png')
