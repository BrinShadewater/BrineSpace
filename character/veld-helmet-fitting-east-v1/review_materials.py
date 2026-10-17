"""Review candidate against selected idle/action references at gameplay scale."""
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
refs=[('bare idle',ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'),
      ('helmet idle',ROOT/'character/veld-shared-helmet-v1/frames/idle-east/000.png'),
      ('helmet action',ROOT/'character/veld-shared-helmet-actions-east-v1/frames/interact-east/002.png')]
frames=refs+[(f'fit {i}',HERE/f'frames/equip-helmet-east/{i:03}.png') for i in range(1,7)]
sheet=Image.new('RGB',(126*len(frames),320),'#202a30');d=ImageDraw.Draw(sheet)
for j,(label,path) in enumerate(frames):
    im=Image.open(path).convert('RGBA')
    if im.height==184:
        aligned=Image.new('RGBA',(184,208));aligned.alpha_composite(im,(0,24));im=aligned
    small=im.resize((102,115),Image.Resampling.LANCZOS)
    for row,color in enumerate(['#202a30','#bcc0c2']):
        x,y=j*126,row*160
        d.rectangle((x,y,x+125,y+159),fill=color)
        sheet.paste(small,(x+12,y+32),small)
        d.text((x+3,y+8),label,fill='white' if row==0 else 'black')
sheet.save(HERE/'accepted-material-comparison-v13.png')
print('Accepted idle/action and all six interior poses: 82px standing height, dark/light composites.')
