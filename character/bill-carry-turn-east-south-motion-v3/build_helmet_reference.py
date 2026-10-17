from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
f=json.loads((P/'frozen-bindings.json').read_text())
board=Image.new('RGBA',(768,512),(0,0,0,0))
for i,d in enumerate(['east','south']):
 im=Image.open(R/f['endpoints']['helmet'][d][6:]).convert('RGBA').crop((106,66,150,116)).resize((264,300),Image.Resampling.NEAREST)
 board.alpha_composite(im,(i*384+60,100))
board.save(P/'sources/helmet-master-crops.png')
print('Exact current held master helmet/collar crops;6xnearest,no generated pixels.')
