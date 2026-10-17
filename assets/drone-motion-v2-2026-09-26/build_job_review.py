from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'manifest.json').read_text());states={s['id']:s for s in data['states']}
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
def composite(state,n):
    canvas=Image.new('RGBA',(352,300));origin=(48,20);root=state['rootOffsets'][n]
    if state.get('groundCargo') and state['cargoState'][n]!='held':
        offset=state['depositOffset'] if state['cargoState'][n]=='deposited' else [0,0]
        canvas.alpha_composite(Image.open(ROOT/state['groundCargo']),(round(origin[0]+offset[0]),round(origin[1]+offset[1])))
    im=Image.open(ROOT/state['frameFiles'][n]).convert('RGBA');im.alpha_composite(Image.open(ROOT/state['effectFiles'][n]));im.alpha_composite(Image.open(ROOT/state['cargoFiles'][n]))
    lamp=state['lamp'];im.alpha_composite(Image.open(ROOT/data['statusClips']['operational']['frameFiles'][n%51]),(lamp[0]-128,lamp[1]-128))
    canvas.alpha_composite(im,(round(origin[0]+root[0]),round(origin[1]+root[1])))
    return canvas
frames=[]
for n in range(0,270,3):
    board=Image.new('RGB',(1408,435),'#17272e');d=ImageDraw.Draw(board)
    for i,h in enumerate(['north','east','south','west']):
        state=states[f'job-collect-{h}'];im=composite(state,n);board.paste(im,(i*352,28),im)
        small=im.resize((120,102),Image.Resampling.LANCZOS);board.paste(small,(i*352+116,326),small)
        d.text((i*352+18,8),h.upper()+' / '+state['phases'][n],font=font,fill='#d8e7ee')
    frames.append(board)
frames[0].save(ROOT/'review/collection-jobs.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False)
story=Image.new('RGB',(1408,435*7),'#17272e')
for row,n in enumerate([0,42,63,105,171,195,240]):story.paste(frames[n//3],(0,row*435))
story.save(ROOT/'review/collection-storyboard.png')
board=Image.new('RGB',(1408,1120),'#17272e');d=ImageDraw.Draw(board)
for row,h in enumerate(['north','east','south','west']):
    for col,(action,n) in enumerate([('mine',0),('weld',0),('repair',0),('repair',60)]):
        state=states[f'job-{action}-{h}'];im=composite(state,n)
        board.paste(im,(col*352,row*280+12),im);d.text((col*352+8,row*280+4),h+' / '+action+' / '+state['phases'][n],font=font,fill='#d8e7ee')
board.save(ROOT/'review/job-transitions.png')
print('Saved collection motion, seven-stage storyboard and work transition review.')
