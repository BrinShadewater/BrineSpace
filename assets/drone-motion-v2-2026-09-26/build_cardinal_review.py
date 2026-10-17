"""Full cardinal action matrix and travel/action same-scale comparisons."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'manifest.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
dirs=['north','east','south','west'];actions=['mine','collect','weld','repair']
states={s['id']:s for s in data['states']}
frames=[]
for n in range(0,102,3):
    board=Image.new('RGB',(1120,1400),'#17272e');draw=ImageDraw.Draw(board)
    for row,direction in enumerate(dirs):
        for col,action in enumerate(actions):
            state=states[f'work-{action}-{direction}'];im=Image.open(ROOT/state['frameFiles'][n]).convert('RGBA')
            im.alpha_composite(Image.open(ROOT/state['effectFiles'][n]))
            light=Image.open(ROOT/data['statusClips']['operational']['frameFiles'][n%51])
            lamp=state['lamp'];im.alpha_composite(light,(lamp[0]-128,lamp[1]-128))
            x=col*280;y=row*350;board.paste(im,(x+12,y+26),im)
            small=im.resize((87,87),Image.Resampling.LANCZOS);board.paste(small,(x+96,y+259),small)
            draw.text((x+12,y+6),f'{direction.upper()} / {action.upper()}',font=font,fill='#d8e7ee')
    frames.append(board)
frames[0].save(ROOT/'review/cardinal-work.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
for n in [0,5,11,17,25,33]:frames[n].save(ROOT/'review'/f'cardinal-phase-{n*3:03}.png')
# No bounding-box normalization: all panels use the exported pixels unchanged.
board=Image.new('RGB',(1400,1580),'#17272e');draw=ImageDraw.Draw(board)
headings=['north','northeast','east','southeast','south','southwest','west','northwest']
for i,h in enumerate(headings):
    x=i%4*350;y=i//4*330
    im=Image.open(ROOT/data['headings'][h]['pose'])
    board.paste(im,(x+47,y+28),im);small=im.resize((87,87),Image.Resampling.LANCZOS);board.paste(small,(x+130,y+239),small)
    draw.text((x+20,y+8),h.upper(),font=font,fill='#d8e7ee')
draw.text((20,675),'TRAVEL / MINE / COLLECT / WELD / REPAIR — unchanged export scale per heading',font=font,fill='#d8e7ee')
for row,h in enumerate(dirs):
    for col,a in enumerate(['travel']+actions):
        im=Image.open(ROOT/(data['headings'][h]['pose'] if a=='travel' else data['actions'][a]['directions'][h]['pose']))
        # Same 0.65 comparison scale; no independent fitting by sprite bounds.
        im=im.resize((166,166),Image.Resampling.LANCZOS);x=col*280+55;y=715+row*211
        board.paste(im,(x,y+20),im);draw.text((x,y),f'{h} / {a}',font=font,fill='#b8cdd7')
board.save(ROOT/'review/size-pass.png')
print('16 action loops reviewed at enlarged/native scale; 8 travel headings + 20 same-scale action comparisons.')
