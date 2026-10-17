from pathlib import Path
from PIL import Image, ImageDraw
import json

p=Path(__file__).resolve().parent
o=p/'water-stop-bridge-v340'
data=json.loads((o/'traces.json').read_bytes())
assert data['failures']==0 and len(data['traces'])==48
for gear,label in [('', 'bare'),('diving-helmet','helmet')]:
    board=Image.new('RGB',(2048,1800),(48,59,64));draw=ImageDraw.Draw(board)
    for col,direction in enumerate(['east','south','west','north']):
        rows=[x for x in data['traces'] if x['gear']==gear and x['direction']==direction]
        for row,x in enumerate(rows):
            draw.text((col*512+5,row*300+4),f"{direction} swim{x['swimSlot']} -> stop / exact {x['pixelsEqual']}",fill='white')
            for side,key in enumerate(['before','after']):
                im=Image.open(o/x[key]).convert('RGBA')
                board.paste(im,(col*512+side*256,row*300+20),im)
    board.save(o/f'{label}-entry-review.png')
print('Two staged entry comparison boards built; motion review still required.')
