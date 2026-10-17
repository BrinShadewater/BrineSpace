from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
board=Image.new('RGB',(1536,2048),(34,52,62));draw=ImageDraw.Draw(board)
for row,(direction,gear) in enumerate((d,g) for d in ['east','west','north','south'] for g in ['bare','helmet']):
 folder=P.parent/(f'bill-recover-air-{direction}-coherent-v1' if gear=='bare' else f'bill-recover-air-helmet-{direction}-coherent-v1')
 for col,i in enumerate(range(6)):
  im=Image.open(folder/'frames'/f'recover-air-{direction}'/f'{i:03}.png');board.paste(im,(col*256,row*256),im)
  draw.text((col*256+6,row*256+6),f'{direction} {gear} pose{i}',fill='white')
board.save(P/'family-master-comparison.png')
print('Built all-cardinal idle/recovery comparison')
