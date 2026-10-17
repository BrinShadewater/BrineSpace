from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
names=['north','northeast','east','southeast','south','southwest','west','northwest']
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
frames=[]
for n in range(51):
    out=Image.new('RGB',(1120,760),'#17272e');d=ImageDraw.Draw(out)
    for i,name in enumerate(names):
        x=(i%4)*280;y=(i//4)*380
        state=next(s for s in data['states'] if s['id']=='move-'+name)
        pose=Image.open(ROOT/state['frameFiles'][n]).convert('RGBA')
        light=Image.open(ROOT/data['statusClips']['operational']['frameFiles'][n]).convert('RGBA')
        at=data['headings'][name]['lamp'];pose.alpha_composite(light,(at[0]-128,at[1]-128))
        out.paste(pose,(x+12,y+35),pose)
        small=pose.resize((87,87),Image.Resampling.LANCZOS);out.paste(small,(x+96,y+278),small)
        d.text((x+22,y+10),name.upper(),font=font,fill='#d8e7ee')
    frames.append(out)
frames[0].save(ROOT/'review/eight-directions.gif',save_all=True,append_images=frames[1:],duration=[33,33,34]*17,loop=0,optimize=False)
frames[0].save(ROOT/'review/eight-directions.png')
print('Eight directions / 51 frames / 30 fps / enlarged and native size')
