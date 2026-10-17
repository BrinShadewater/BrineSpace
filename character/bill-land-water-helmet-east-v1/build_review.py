from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;B=P.parent/'bill-land-water-east-v3'
frames=[Image.open(P/f'frames/land-swim-east/{i:03}.png').convert('RGBA') for i in range(6)]
game=Image.new('RGB',(1152,460),'#182932');d=ImageDraw.Draw(game)
for j,h in enumerate([82,54,27]):
 for i,im in enumerate(frames):
  small=im.resize((round(320*h/148),round(320*h/148)),Image.Resampling.LANCZOS);game.paste(small,(i*192+(192-small.width)//2,j*150+20),small)
 d.text((5,j*150+3),f'{h}px standing ruler',fill='white')
game.save(P/'gameplay-review.png')
detail=Image.new('RGB',(1280,440),'#182932');d=ImageDraw.Draw(detail)
for i,(x,y) in enumerate([(171,88),(177,118),(183,157),(187,188)]):
 for row,root in enumerate([B,P]):
  im=Image.open(root/f'frames/land-swim-east/{i+1:03}.png').convert('RGBA');crop=im.crop((x-35,y-15,x+45,y+40)).resize((320,220),Image.Resampling.NEAREST);detail.paste(crop,(i*320,row*220),crop)
  d.text((i*320+4,row*220+3),f'{"Bare" if row==0 else "Helmet"} {i+1}',fill='white')
detail.save(P/'neck-review.png')
e=json.loads((P/'helmet-registration.json').read_text());e['reviewArtifacts']=['paired-review.png','neck-review.png','gameplay-review.png'];e['visualReviewScope']='Static whole figures, enlarged head/neck/foreground sleeves and station densities only. Continuous motion and native support pending.'
(P/'helmet-registration.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text();html=html.replace('<div class="loops">','<img src="neck-review.png"><img src="gameplay-review.png"><div class="loops">');(P/'index.html').write_text(html,encoding='utf-8')
print('Head/neck crops and 82/54/27px station-density views prepared.')
