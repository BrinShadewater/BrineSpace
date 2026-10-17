from pathlib import Path
import json, math
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
H = Path(__file__).resolve().parent
font = ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'), 22)

def sheet(pack, name, rows, columns=6):
    board = Image.new('RGBA', (columns*256, 75+math.ceil(len(rows)/columns)*285), '#252b2e')
    draw = ImageDraw.Draw(board)
    draw.text((20, 15), 'KRUSHER DOM / COMPLETE HEAD AND NECK', font=font, fill='white')
    draw.text((20, 42), 'Original James body / original timing / revised identity', font=font, fill='#bed2d3')
    for n, (label, rel) in enumerate(rows):
        x, y = (n%columns)*256, 75+(n//columns)*285
        board.alpha_composite(Image.open(pack/rel).convert('RGBA'), (x,y))
        draw.text((x+8, y+258), label, font=font, fill='white')
    board.save(pack/name)

for gear in ['bare', 'helmet']:
    P = R/'character/krusher-meal-family-v3'
    m = json.loads((P/(gear+'-manifest.json')).read_text())
    sheet(P, gear+'-sheet.png', [(s['id']+' / '+str(i), p) for s in m['states'] for i,p in enumerate(s['frameFiles'])])
P = R/'character/krusher-helmet-transition-v3'
m = json.loads((P/'manifest.json').read_text())
sheet(P, 'contact-sheet.png', [('Helmet on / '+str(i), p) for i,p in enumerate(m['states'][0]['frameFiles'])])
P = R/'character/krusher-meal-service-v3'
records = json.loads((P/'revision.json').read_text())['records']
rows = sorted([(q['details']['newSourceIndex'],q['output']) for q in records if q['details']['newSourceIndex'] is not None])
sheet(P, 'new-poses-sheet.png', [('Pickup / '+str(i), p) for i,p in rows])

# A compact mobile-readable overview uses the same full sprite canvases,
# doubled strictly by nearest neighbour; no anatomy or pixel editing.
board = Image.new('RGBA', (1200, 950), '#252b2e')
draw = ImageDraw.Draw(board)
draw.text((20, 16), 'KRUSHER DOM / REVISED HEAD FIT', font=font, fill='white')
draw.text((20, 45), 'Meals, pickup and helmet changes / System Administrator', font=font, fill='#bed2d3')
choices = []
P = R/'character/krusher-meal-family-v3'
for g,k,i in [('bare','eat-east',2),('bare','drink-west',3),('helmet','eat-south',0),('helmet','eat-west',0)]:
    m=json.loads((P/(g+'-manifest.json')).read_text());s=next(s for s in m['states'] if s['id']==k)
    choices.append((g+' / '+k,P/s['frameFiles'][i]))
P = R/'character/krusher-meal-service-v3'
for i in [10,12]:
    q=next(q for q in records if q['details']['newSourceIndex']==i)
    choices.append(('Bare / pickup '+str(i), P/q['output']))
P = R/'character/krusher-helmet-transition-v3'
m=json.loads((P/'manifest.json').read_text())
for i in [5,11]:choices.append(('Helmet change / '+str(i),P/m['states'][0]['frameFiles'][i]))
for n,(label,path) in enumerate(choices):
    x,y=(n%4)*300,90+(n//4)*415
    # Fixed source window includes original body and all moving hands/shells.
    im=Image.open(path).convert('RGBA').crop((58,35,198,230)).resize((280,390),Image.Resampling.NEAREST)
    board.alpha_composite(im,(x+10,y));draw.text((x+10,y-27),label,font=font,fill='white')
board.save(H/'meal-equipment-head-fit-sheet.png')
print(json.dumps({'fullBodySheets':4,'overview':'character/krusher-head-fit-v3/meal-equipment-head-fit-sheet.png'}))
