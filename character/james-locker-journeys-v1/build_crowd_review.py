from pathlib import Path
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
for phase in ['occupied', 'next-crew']:
    board = Image.new('RGB', (1728, 1368), (45, 58, 63))
    for row, action in enumerate(['equip-helmet', 'remove-helmet', 'refill']):
        for q in range(4):
            image = Image.open(P / 'crowd-captures' / f'q{q}-{action}-{phase}.png').convert('RGB')
            assert image.size == (432, 432)
            x, y = q * 432, row * 456
            board.paste(image, (x, y + 24))
            ImageDraw.Draw(board).text((x + 5, y + 5), f'q{q} / {action} / {phase}', fill='white')
    board.save(P / f'native-crowd-{phase}-contact.png')
print('24 native sampled service/handoff views assembled at actual capture scale')
