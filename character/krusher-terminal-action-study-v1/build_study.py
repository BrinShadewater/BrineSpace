from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent
for folder in ['cells','registered','review']:(P/folder).mkdir(parents=True,exist_ok=True)
source=Image.open(P/'source-01.png').convert('RGBA')
base=Image.open(R/'character/krusher-equipment-study-v1/review/fitted-west.png').convert('RGBA')
cells=[];bounds=[]
for i in range(8):
    x=(i%4)*384;y=(i//4)*512
    cell=source.crop((x,y,x+384,y+512));a=np.array(cell.getchannel('A'));ys,xs=np.where(a>100)
    box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
    assert box[0]>2 and box[1]>2 and box[2]<382 and box[3]<510
    cell.save(P/f'cells/{i:03}.png');cells.append(cell);bounds.append(box)
scale=148/(bounds[0][3]-bounds[0][1])
# One density and one registration for every authored pose. Planted boots provide
# the anchor; no per-pose normalisation, warping, mirroring or invented inbetweens.
native_size=(round(384*scale),round(512*scale))
foot_x=(bounds[0][0]+bounds[0][2])/2
dest=(round(92-foot_x*scale),round(172-bounds[0][3]*scale))
board=Image.new('RGB',(1150,520),'#272b2e');draw=ImageDraw.Draw(board)
draw.text((14,12),'KRUSHER / TERMINAL ACTION / REGISTERED SOURCE STUDY',fill='white')
registered=[]
for i,cell in enumerate(cells):
    im=Image.new('RGBA',(184,184));im.alpha_composite(cell.resize(native_size,Image.Resampling.LANCZOS),dest)
    im.save(P/f'registered/{i:03}.png');registered.append(im)
    enlarged=im.resize((220,220),Image.Resampling.NEAREST)
    board.paste(enlarged,((i%4)*230+220,(i//4)*240+35),enlarged)
    draw.text(((i%4)*230+230,(i//4)*240+252),['neutral','grasp','lift','open','type down','type up','close','lower'][i],fill='white')
canonical=base.resize((220,220),Image.Resampling.NEAREST);board.paste(canonical,(0,35),canonical);draw.text((12,256),'Canonical idle',fill='white')
board.save(P/'review/registered-source.png')
manifest={'name':'Krusher Dom terminal action source study','status':'unselected; native scale and arm replacement review pending','source':'source-01.png','sourceSha256':hashlib.sha256((P/'source-01.png').read_bytes()).hexdigest(),'authoringMethod':'builtin imagegen','executionId':'d48ab767-3987-4c28-b295-89afc269d12e','references':['character/krusher-equipment-study-v1/review/fitted-west.png','character/krusher-equipment-study-v1/source-02.png'],'alphaRange':list(source.getchannel('A').getextrema()),'cellBounds':bounds,'commonScale':scale,'commonDestination':dest,'nativeSize':native_size,'limitations':['Generated whole bodies are not an approved replacement for the Bill body','Registered source study only; no final action manifest or runtime selection','Exact original idle entry/exit and protected body compositing still required']}
(P/'provenance.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['alphaRange','commonScale','commonDestination','nativeSize','cellBounds']}))
