import json
from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent/'release-death-review-v349';data=json.loads((p/'native-review.json').read_text());assert data['failures']==0
for gear in ['bare','helmet']:
    for direction in ['west','east','north','south']:
        board=Image.new('RGB',(6*214,2*245),(47,58,63));draw=ImageDraw.Draw(board)
        for row,medium in enumerate(['ground','water']):
            for slot in range(6):
                file=p/f'{gear}-death-{medium}-{direction}-{slot}.png';im=Image.open(file)
                board.paste(im,(214*slot,245*row+25))
                draw.text((214*slot+4,245*row+6),f'{gear} {medium} {direction} / {slot}',fill='white')
        board.save(p/f'{gear}-{direction}-native.png')
print('Built eight native terminal-death chronology boards')
