from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
R=Path(__file__).resolve().parent;OLD=R.with_name('veld-west-walk-master-v3')
frames=[];audit=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for i in range(4):
    canvas=Image.new('RGB',(736,480),'#263139');d=ImageDraw.Draw(canvas)
    for col,(base,label) in enumerate([(OLD,'West reference'),(R,'East counterpart')]):
        f=Image.open(base/f"frames/{'walk-west' if col==0 else 'walk-east'}/{i:03}.png").convert('RGBA')
        big=f.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(col*368,30),big)
        d.text((col*368+12,8),label+f' / {i+1}',font=font,fill='white')
        small=f.resize((56,56),Image.Resampling.LANCZOS);canvas.paste(small,(col*368+156,405),small)
        if col:
            a=np.array(f)[:,:,3];y,x=np.nonzero(a>127);_,xx=np.nonzero(a[y.min():y.min()+20]>127)
            audit.append({'frame':i+1,'headCollarWidth':int(xx.max()-xx.min()+1),'height':int(y.max()-y.min()+1)})
    frames.append(canvas)
frames[0].save(R/'east-west.gif',save_all=True,append_images=frames[1:],duration=225,loop=0)
sheet=Image.new('RGB',(736,210),'#263139');d=ImageDraw.Draw(sheet)
for i in range(4):
    f=Image.open(R/f'frames/walk-east/{i:03}.png');sheet.paste(f,(i*184,0),f);d.text((i*184+10,188),str(i+1),fill='white')
sheet.save(R/'contact-sheet.png')
(R/'size-audit.json').write_text(json.dumps(audit,indent=2))
print(audit)
