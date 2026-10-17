from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'north/pause-evidence.json').read_bytes());rows=e['records'];assert e['failures']==0
m=json.loads((R/'character/james-torch-material-residue-v2/helmet-manifest.json').read_bytes());clips={s['id']:s for s in m['states']};native=[];source=[]
for mode,size,limit,columns in [('native',(150,165),48,8),('source',(184,204),40,5)]:
    for page in range(math.ceil(len(rows)/limit)):
        batch=rows[page*limit:(page+1)*limit];b=Image.new('RGB',(columns*size[0],math.ceil(len(batch)/columns)*size[1]),'#303b40');d=ImageDraw.Draw(b)
        for n,r in enumerate(batch):
            assert r['helmet'];x=n%columns*size[0];y=n//columns*size[1]
            if mode=='native':
                fx,fy=r['footViewport'];im=Image.open(R/r['path'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));b.paste(im,(x,y+20))
            else:
                key='torch-draw-north' if r['key']=='idle-north' else r['key'];index=0 if r['key']=='idle-north' else r['index'];im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA');assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==r['sourceHash'];b.paste(im,(x,y+20),im)
            d.text((x+3,y+3),r['label']+' / '+r['key']+f" #{r['index']}",fill='white')
        name=f'pause-{mode}-page{page}.png';b.save(P/name);(native if mode=='native' else source).append(name)
(P/'pause-review.json').write_text(json.dumps({'nativeBoards':native,'sourceBoards':source,'captures':len(rows),'helmetSourceRGBAMatches':len(rows),'nativeHashes':{r['path']:hashlib.sha256((R/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows},'scope':'Actual North helmet ward pause/return/reentry unique sources plus two fresh-scene disk Continues. Whole selected paired sources, same physical foot and camera scale. Not other facing interruption/gear-change motion or locker fitting.'},indent=2)+'\n',encoding='utf-8');print('Helmet pause review:',len(rows),'captures')
