from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;pack=json.loads((P/'east-turn-v3-bare-manifest.json').read_bytes());pages=[]
for s in pack['states']:
    for page in range((len(s['frameFiles'])+5)//6):
        board=Image.new('RGB',(1200,1920),'#303b40')
        for row in range(6):
            i=page*6+row
            if i>=len(s['frameFiles']):break
            board.paste(Image.open(P/'turn-v3-native'/(s['id']+'-'+str(i).zfill(3)+'.png')),(0,row*320))
        name='native-turn-v3-'+s['id']+'-'+str(page)+'.png';board.save(P/name);pages.append(name)
(P/'turn-v3-native-review-pages.json').write_text(json.dumps({'pages':pages,'captures':46,'scope':'All46native paired source-clock scale captures,148/82/54/27. Actual player through staged manifests; no actual grid actor/task or continuous-world claim.'},indent=2))
print(len(pages))
