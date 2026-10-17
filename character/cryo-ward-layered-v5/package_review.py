"""Package native compositor frames without changing their painted pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[1]/'output/margot-cryo-landing-v13'
images=[]
for f in sorted(OUT.glob('layer-*.png')):
    frame=Image.new('RGBA',(240,404),(35,43,49,255))
    frame.alpha_composite(Image.open(f).crop((136,184,376,576)),(0,0))
    images.append(frame.convert('RGB'))
assert len(images)==101
images[0].save(HERE/'thaw-and-exit.gif',save_all=True,append_images=images[1:],duration=80,loop=0)
board=Image.new('RGB',(1440,429),(35,43,49));draw=ImageDraw.Draw(board)
for i,n in enumerate([0,35,54,65,83,100]):
    board.paste(images[n],(i*240,0));draw.text((i*240+15,409),f'{n*.08:.2f}s',fill='white')
board.save(HERE/'animation-review.png')
Image.open(OUT/'layer-000.png').save(HERE/'frames/pet-closed-occupied.png')
Image.open(OUT/'empty-open.png').save(HERE/'frames/pet-open-runtime.png')
print('PASS:101 native compositor samples, eight-second review, occupied/empty endpoint exports')
