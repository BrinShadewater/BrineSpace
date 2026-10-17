"""Refresh supplementary review boards from the active manifest."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;d=json.loads((R/'manifest.json').read_text());clips={e['id']:e for e in d['states']}
order=['north','northeast','east','southeast','south','southwest','west','northwest']
board=Image.new('RGBA',(1280,800),'#17272e');draw=ImageDraw.Draw(board)
for i,h in enumerate(order):
    e=clips['carry-'+h];im=Image.open(R/e['frameFiles'][0]).convert('RGBA');im.alpha_composite(Image.open(R/e['cargoFiles'][0]).convert('RGBA'))
    x=i%4*320;y=i//4*400;draw.text((x+12,y+12),h.upper()+' / LOADED',fill='#c5d7d9')
    board.alpha_composite(im.resize((300,300),Image.Resampling.LANCZOS),(x+10,y+40))
    board.alpha_composite(im.resize((152,152),Image.Resampling.LANCZOS),(x+84,y+246))
board.save(R/'completion/loaded-directions.png')
board=Image.new('RGBA',(1344,1344),'#17272e');draw=ImageDraw.Draw(board)
for i,(state,n) in enumerate([('idle',0),('drive',15),('reverse',15),('steer-left',30),('mine',85),('collect',80),('carry',0),('unload',100),('blocked',50),('power-on',30),('charging',15),('disabled',15)]):
    e=clips[state+'-south'];im=Image.open(R/e['frameFiles'][n]).convert('RGBA');im.alpha_composite(Image.open(R/e['effectFiles'][n]).convert('RGBA'))
    if 'cargoFiles' in e:im.alpha_composite(Image.open(R/e['cargoFiles'][n]).convert('RGBA'))
    x=i%4*336;y=i//4*448;draw.text((x+12,y+12),state.upper(),fill='#c5d7d9');board.alpha_composite(im.resize((336,336),Image.Resampling.LANCZOS),(x,y+40))
board.save(R/'completion/contact-sheet.png')
print('Updated loaded-direction and state review boards.')
