from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for bg,name in [((29,43,51),'dark'),((218,225,224),'light')]:
 board=Image.new('RGB',(1024,1024),bg);d=ImageDraw.Draw(board)
 for row,(direction,gear) in enumerate([(dr,g) for dr in ['east','west'] for g in ['bare','helmet']]):
  swim=f'bill-swim-{direction}-coherent-v1' if gear=='bare' else f'bill-swim-helmet-{direction}-coherent-v1'
  death=f'bill-death-water-{direction}-coherent-v1' if gear=='bare' else f'bill-death-water-helmet-{direction}-coherent-v1'
  files=[(swim,f'swim-{direction}',0,{'east':(6,40),'west':(42,40)}[direction]),(death,f'death-water-{direction}',0,(0,0)),(death,f'death-water-{direction}',3,(0,0)),(death,f'death-water-{direction}',5,(0,0))]
  for col,(folder,state,i,pad) in enumerate(files):
   im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(P.parent/folder/'frames'/state/f'{i:03}.png').convert('RGBA'),pad);board.paste(im,(col*256,row*256),im);d.text((col*256+5,row*256+5),f'{gear} {state} {i}',fill='white' if name=='dark' else 'black')
 board.save(P/f'paired-east-west-master-{name}.png')
print('Built independent East/West paired master comparison')
