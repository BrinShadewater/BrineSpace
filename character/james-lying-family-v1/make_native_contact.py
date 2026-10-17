from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
b=Image.new('RGB',(1440,1140),'#303b40');draw=ImageDraw.Draw(b)
for mode in range(2):
 for row,action in enumerate(['lie-down','sleep','get-up']):
  for i in range(6):
   path=P/('retained-berth-helmet' if mode else 'retained-berth')/'branforth/seating-room'/('%s-%02d.png'%(action,i));at=(i*240,30+(mode*3+row)*190)
   b.paste(Image.open(path).crop((330,123,600,300)).resize((240,160)),at);draw.text((at[0]+6,at[1]-22),('helmet ' if mode else 'bare ')+action+' '+str(i),fill='white')
b.save(P/'native-all-berth-contact.png')
