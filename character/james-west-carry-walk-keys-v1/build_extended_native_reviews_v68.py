from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parent;out=p/'extended-windows-v68'
fs=[out/'native'/f'carry-middle-review-west-{i:03d}.png' for i in range(5)]+[out/'native'/f'carry-seam-review-west-{i:03d}.png' for i in range(4)]
for group in range(3):
    board=Image.new('RGBA',(1200,960))
    for row,f in enumerate(fs[group*3:group*3+3]):
        im=Image.open(f).convert('RGBA');assert im.size==(1200,320);board.paste(im,(0,row*320))
    board.save(out/f'native-review-{group}.png')
print('Nine native captures packed at original resolution into three chronological boards.')
