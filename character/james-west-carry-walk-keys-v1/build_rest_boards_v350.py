from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent/'release-rest-review-v350'
phases=['entry-0.0','entry-0.5','entry-0.999','held','exit-0.0','exit-0.5','exit-0.999']
for room in ['crew_hab','crew_lounge']:
    for rotation in range(4):
        board=Image.new('RGB',(7*220,2*250),(47,58,63));draw=ImageDraw.Draw(board)
        for row,gear in enumerate(['bare','helmet']):
            for col,phase in enumerate(phases):
                file=p/f'{gear}-{room}-{rotation}-{phase}.png';im=Image.open(file)
                board.paste(im,(220*col,250*row+25));draw.text((220*col+4,250*row+5),f'{gear} {phase}',fill='white')
        board.save(p/f'{room}-{rotation}-native.png')
print('Built eight actual furniture chronology boards')
