from pathlib import Path
from PIL import Image
import sys
out=Path(sys.argv[1]);key=sys.argv[2];count=int(sys.argv[3]);assert count>0
for start in range(0,count,3):
    indices=list(range(start,min(count,start+3)));board=Image.new('RGBA',(1200,320*len(indices)))
    for row,i in enumerate(indices):
        im=Image.open(out/'native'/f'{key}-{i:03d}.png').convert('RGBA');assert im.size==(1200,320);board.paste(im,(0,row*320))
    board.save(out/f'native-review-{start//3}.png')
print(f'{count}actual native captures packed without resampling.')
