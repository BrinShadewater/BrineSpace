from PIL import Image,ImageDraw
from pathlib import Path
r=Path('assets/drone-motion-v2-2026-09-26'); b=Image.new('RGB',(1024,512),'#777777');d=ImageDraw.Draw(b)
for i,h in enumerate(['north','northeast','east','southeast','south','southwest','west','northwest']):
 im=Image.open(r/'poses'/f'{h}.png');x=i%4*256;y=i//4*256;b.paste(im,(x,y),im)
 for n in range(0,256,32):
  d.line((x+n,y,x+n,y+256),fill='#606060');d.line((x,y+n,x+256,y+n),fill='#606060');d.text((x+n,y),str(n));d.text((x,y+n),str(n))
b.save(r/'polish/grid.png')
