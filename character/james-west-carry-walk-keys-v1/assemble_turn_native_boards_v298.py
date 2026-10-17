from pathlib import Path
from PIL import Image
import sys
p=Path(__file__).resolve().parent/(sys.argv[1] if len(sys.argv)>1 else 'arrival-turn-chronology-v298')
count=int(sys.argv[2]) if len(sys.argv)>2 else 6
for start in range(0,count,3):
 w,h=Image.open(p/f'native-phase{start:02}.png').size
 rows=min(3,count-start)
 im=Image.new('RGBA',(w,h*rows))
 for j in range(rows):im.alpha_composite(Image.open(p/f'native-phase{start+j:02}.png').convert('RGBA'),(0,j*h))
 im.save(p/f'native-phases{start}-{start+rows-1}-review.png')
print(f'{count} native captures assembled without rescaling.')
