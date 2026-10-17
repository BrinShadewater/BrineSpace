from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parent;out=p/'cycle-window-v73'
for group in range(3):
    indices=list(range(group*3,min(8,group*3+3)))
    board=Image.new('RGBA',(1200,320*len(indices)))
    for row,i in enumerate(indices):
        im=Image.open(out/'native'/f'carry-seam-review-west-{i:03d}.png').convert('RGBA')
        assert im.size==(1200,320);board.paste(im,(0,row*320))
    board.save(out/f'native-review-{group}.png')
print('Eight native captures packed at original resolution.')
