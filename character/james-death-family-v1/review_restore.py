from pathlib import Path
from PIL import Image, ImageDraw
P = Path(__file__).resolve().parent
for mode in ['bare', 'helmet']:
    board = Image.new('RGB', (960, 380), '#303b40')
    draw = ImageDraw.Draw(board)
    for row, action in enumerate(['ground', 'water']):
        for col, direction in enumerate(['east', 'south', 'west', 'north']):
            label = f'{mode}-{action}-{direction}-terminal'
            im = Image.open(P/'restore-captures'/(label+'.png')).convert('RGB')
            x, y = im.width//2, im.height//2
            crop = im.crop((x-112, y-110, x+112, y+50))
            board.paste(crop, (col*240, row*190+26))
            draw.text((col*240+4,row*190+5), label, fill='white')
    board.save(P/f'native-restored-terminal-{mode}.png')
print('16 actual disk-restored terminal captures packaged into two review boards')
