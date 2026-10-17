from pathlib import Path
from PIL import Image
import json
p=Path(__file__).resolve().parent
def components(f):
    im=Image.open(f).convert('RGBA');alpha=im.getchannel('A');pixels=alpha.load();left={(x,y) for y in range(im.height) for x in range(im.width) if pixels[x,y]>=128};result=[]
    while left:
        first=left.pop();todo=[first];group=[first]
        while todo:
            x,y=todo.pop()
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in left:left.remove(q);todo.append(q);group.append(q)
        result.append({'pixels':len(group),'bounds':[min(x for x,y in group),min(y for x,y in group),max(x for x,y in group)+1,max(y for x,y in group)+1]})
    return sorted(result,key=lambda d:-d['pixels'])
results=[]
for i in (0,8,12,20,28,36,44,48):
    a=components(p/f'walk{i:02d}-belt-anatomy-v4.png');b=components(p/f'walk{i:02d}-case-master-v5.png')
    results.append({'phase':i,'prior':a,'candidate':b})
(p/'case-master-v5-components.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
for d in results:print(f"Phase{d['phase']}: prior detached {d['prior'][1:]}; candidate detached {d['candidate'][1:]}")
