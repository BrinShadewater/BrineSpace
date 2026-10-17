from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-evidence.json').read_bytes());rows=e['records']
m=json.loads((R/'character/james-torch-material-residue-v2/bare-manifest.json').read_bytes());clips={s['id']:s for s in m['states']}
def source(r):
    key='torch-draw-west' if r['key']=='idle-west' else r['key'];index=0 if r['key']=='idle-west' else r['index']
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA');assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==r['sourceHash'];return im
sources=[source(r) for r in rows]
def crop(path,foot):
    fx,fy=foot;return Image.open(path).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20))
native=[];clean=[]
for page in range(math.ceil(len(rows)/48)):
    batch=rows[page*48:(page+1)*48];b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');d=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%8*150;y=n//8*165;b.paste(crop(R/r['path'].removeprefix('res://'),r['footViewport']),(x,y+20));d.text((x+3,y+3),r['label'],fill='white');d.text((x+3,y+151),r['key']+f" #{r['index']}",fill='white')
    name=f'native-page{page}.png';b.save(P/name);native.append(name)
for page in range(math.ceil(len(rows)/40)):
    batch=rows[page*40:(page+1)*40];b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');d=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%5*184;y=n//5*204;im=sources[page*40+n];b.paste(im,(x,y+20),im);d.text((x+3,y+3),r['key']+f" #{r['index']}",fill='white')
    name=f'source-page{page}.png';b.save(P/name);clean.append(name)
mr=R/'character/crew-runtime-matte-v1/branforth';mm=json.loads((mr/'manifest.json').read_bytes());ms={s['id']:s for s in mm['states']};mp=mr/ms['idle-west']['frameFiles'][0]
held=[im for r,im in zip(rows,sources) if r['key']=='weld-west'];examples=[('standing master',Image.open(mp).convert('RGBA')),('draw entry',sources[0]),('held first',held[0]),('held middle',held[len(held)//2]),('stow end',Image.open(R/clips['torch-stow-west']['frameFiles'][-1].removeprefix('res://')).convert('RGBA')),('completed idle',sources[-1])]
b=Image.new('RGB',(1104,216),'#303b40');d=ImageDraw.Draw(b)
for col,(label,im) in enumerate(examples):
    x=col*184;b.paste(im,(x,20),im);d.text((x+3,3),label,fill='white');d.line((x+20,192,x+164,192),fill='#657276')
b.save(P/'master-comparison.png')
probe=json.loads((P/'probe-evidence.json').read_bytes());new=next(r for r in rows if r['label']=='weld-before');b=Image.new('RGB',(600,300),'#303b40');d=ImageDraw.Draw(b)
for col,(label,path,foot) in enumerate([('Before: torch overlaps crate',P/'west-before.png',probe['footViewport']),('After: clear working height',R/new['path'].removeprefix('res://'),new['footViewport'])]):
    b.paste(crop(path,foot).resize((300,270),Image.Resampling.NEAREST),(col*300,24));d.text((col*300+6,6),label,fill='white')
b.save(P/'before-after.png')
frames=[]
for r in rows:
    if not r['label'].startswith('actual-'):continue
    b=Image.new('RGB',(300,292),'#303b40');b.paste(crop(R/r['path'].removeprefix('res://'),r['footViewport']).resize((300,270),Image.Resampling.NEAREST),(0,22));ImageDraw.Draw(b).text((6,4),r['key']+f" #{r['index']} / pose order",fill='white');frames.append(b)
frames[0].save(P/'native-source-order.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2)
report={'nativeBoards':native,'sourceBoards':clean,'masterComparison':'master-comparison.png','masterPath':str(mp.relative_to(R)),'beforeAfter':'before-after.png','preview':'native-source-order.gif','captures':len(rows),'nativeRGBAMatches':len(rows),'oldFoot':probe['foot'],'newFoot':rows[0]['foot'],'nativeHashes':{r['path']:hashlib.sha256((R/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows},'scope':'West native whole-source changes and three paused real disk fresh Continues, actual normal paid job/cost/reward at new ordinary approach. All88 source RGBA exact. Comparison uses per-view viewport feet and same native zoom; same148/p92,172 master source ruler. Native GIF50ms/unique captured source pose, simplified source order rather than continuous real-time18-second gameplay. Original camera award recentering distinguished from physical contact. Clear registered prop rectangle ray at flame height; conservative rectangle clearance, not full silhouette/moving furniture/gear acceptance.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({'captures':len(rows),'boards':native+clean}))
