from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parent;P=R/'polish';names=['north','northeast','east','southeast','south','southwest','west','northwest'];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
for theme,bg,fg in [('dark','#192930','#d9e5e9'),('light','#d7dde0','#20323a')]:
 b=Image.new('RGB',(1120,760),bg);d=ImageDraw.Draw(b)
 for i,h in enumerate(names):
  x=i%4*280;y=i//4*380;d.text((x+8,y+4),h+' / before -> polish',font=font,fill=fg)
  for col,path in enumerate([R/'poses'/f'{h}.png',P/'poses'/f'{h}.png']):
   im=Image.open(path).convert('RGBA');small=im.resize((140,140),Image.Resampling.LANCZOS);b.paste(small,(x+col*140,y+24),small)
   if col:b.paste(im,(x+12,y+125),im)
 b.save(P/('surface-polish-comparison.png' if theme=='dark' else 'surface-polish-comparison-light.png'))
print('Final exported-pixel comparison boards saved.')
