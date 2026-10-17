from pathlib import Path
import json
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
pack=json.loads((p/'bare-manifest.json').read_bytes());pages=[];count=0
for state in pack['states']:
    n=int(state['frameCount']);board=Image.new('RGB',(2400,((n+3)//4)*184),'#303b40');d=ImageDraw.Draw(board)
    for i in range(n):
        path=p/'native'/f'{state["id"]}-{i:03d}.png';im=Image.open(path).convert('RGB')
        assert im.size==(1200,320)
        x=i%4*600;y=i//4*184;board.paste(im.resize((600,160),Image.Resampling.LANCZOS),(x,y+24));d.text((x+4,y+4),f'{state["id"]} {i}',fill='white');count+=1
    name=state['id']+'-native-contact.png';board.save(p/name);pages.append(name)
(p/'native-review.json').write_text(json.dumps({'pairedNativePresentations':count,'gearPresentations':count*2,'pages':pages,'visualReviewPending':True,'continuousPlaybackWatched':False,'selected':False,'scope':'All prescribed finite frame slots sampled at exact source clock; paired full/82/54/27px native draw. Contact sheets shrink captures uniformly for review; full capture2 inspected separately. No continuous cadence/natural world/room lifecycle or normal admission.'},indent=2)+'\n')
print(json.dumps({'pairedPresentations':count,'pages':pages}))
