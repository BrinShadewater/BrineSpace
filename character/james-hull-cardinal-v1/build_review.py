from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'native-evidence.json').read_bytes());rows=e['records']
m=json.loads((R/'character/james-torch-material-residue-v2/bare-manifest.json').read_bytes());clips={s['id']:s for s in m['states']}
master_root=R/'character/crew-runtime-matte-v1/branforth';masters=json.loads((master_root/'manifest.json').read_bytes());master_states={s['id']:s for s in masters['states']}
def source(r):
    key='torch-draw-'+r['case'] if r['key'].startswith('idle-') else r['key'];index=0 if r['key'].startswith('idle-') else r['index']
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==r['sourceHash'];return im
sources=[source(r) for r in rows]
feet={d:next(r['stretchFoot'] for r in rows if r['case']==d) for d in ['east','south','west']}
for r in rows:assert r['stretchFoot']==feet[r['case']]
boards=[]
for page in range(math.ceil(len(rows)/64)):
    batch=rows[page*64:(page+1)*64];b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');draw=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%8*150;y=n//8*165;fx,fy=feet[r['case']];im=Image.open(R/r['path'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));b.paste(im,(x,y+20));draw.text((x+3,y+3),r['key'],fill='white');draw.text((x+3,y+151),f"#{r['index']} / {r['work']:.3f}s",fill='white')
    name=f'native-page{page}.png';b.save(P/name);boards.append(name)
source_boards=[]
for page in range(math.ceil(len(rows)/40)):
    batch=rows[page*40:(page+1)*40];b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');draw=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%5*184;y=n//5*204;im=sources[page*40+n];b.paste(im,(x,y+20),im);draw.text((x+3,y+3),r['key']+f" #{r['index']}",fill='white')
    name=f'source-page{page}.png';b.save(P/name);source_boards.append(name)
master_board=Image.new('RGB',(1104,3*216),'#303b40');draw=ImageDraw.Draw(master_board);master_paths={}
for row,d in enumerate(['east','south','west']):
    path=master_root/master_states['idle-'+d]['frameFiles'][0];master=Image.open(path).convert('RGBA');master_paths[d]=str(path.relative_to(R))
    examples=[('standing master',master),('draw entry',Image.open(R/clips['torch-draw-'+d]['frameFiles'][0].removeprefix('res://')).convert('RGBA'))]
    held=[(r,im) for r,im in zip(rows,sources) if r['key']=='weld-'+d]
    examples.extend([('held first',held[0][1]),('held middle',held[len(held)//2][1]),('stow end',Image.open(R/clips['torch-stow-'+d]['frameFiles'][-1].removeprefix('res://')).convert('RGBA')),('completed idle',sources[next(i for i,r in enumerate(rows) if r['case']==d and r['key']=='idle-'+d)])])
    for column,(label,im) in enumerate(examples):
        x=column*184;y=row*216;master_board.paste(im,(x,y+20),im);draw.text((x+3,y+3),d+' / '+label,fill='white');draw.line((x+20,y+192,x+164,y+192),fill='#657276')
master_board.save(P/'master-comparison.png')
covered={r['sourceHash'] for r in rows};aliases=[];declared=0
for d in ['east','south','west']:
    for key in ['torch-draw-'+d,'weld-'+d,'torch-stow-'+d]:
        for index,path in enumerate(clips[key]['frameFiles']):
            rgba=Image.open(R/path.removeprefix('res://')).convert('RGBA').tobytes();h=hashlib.sha256(rgba.hex().encode()).hexdigest();assert h in covered;declared+=1
            if not any(r['key']==key and r['index']==index for r in rows):aliases.append({'key':key,'index':index,'nativePixelAliases':[r['key']+':'+str(r['index']) for r in rows if r['sourceHash']==h]})
def timed(work,d):
    key='torch-draw-'+d;elapsed=work
    if work>=14:return 'torch-draw-'+d,0
    if work>=13.48:key='torch-stow-'+d;elapsed=work-13.48
    elif work>=.52:
        key='weld-'+d;cycle=sum(clips[key]['frameDurationsMs'])/1000;budget=12.96;loops=max(1,math.floor(budget/cycle+.5));elapsed=((work-.52)/budget*loops*cycle)%cycle
    for i,ms in enumerate(clips[key]['frameDurationsMs']):
        if elapsed<ms/1000:return key,i
        elapsed-=ms/1000
    return key,len(clips[key]['frameFiles'])-1
for r in rows:
    if not r['key'].startswith('idle-'):assert timed(r['work'],r['case'])==(r['key'],r['index'])
frames=[]
cache={}
for tick in range(751):
    work=min(14,tick*.02);b=Image.new('RGB',(600,240),'#303b40');draw=ImageDraw.Draw(b);draw.text((8,7),'James / 14-second paid-clock source preview / no room overlays',fill='white')
    for col,d in enumerate(['east','south','west']):
        key,index=timed(work,d);token=(key,index)
        if token not in cache:cache[token]=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
        im=cache[token];assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest() in covered
        x=col*200+8;b.paste(im,(x,32),im);draw.text((x+70,220),d,fill='white')
    frames.append(b)
frames[0].save(P/'cardinal-paid-clock.gif',save_all=True,append_images=frames[1:],duration=20,loop=0,disposal=2)
hashes={r['path']:hashlib.sha256((R/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows}
(P/'review-evidence.json').write_text(json.dumps({'nativeBoards':boards,'sourceBoards':source_boards,'masterComparison':'master-comparison.png','masterPaths':master_paths,'captures':len(rows),'nativeRGBAMatches':len(rows),'declaredSourceReferencesPixelCovered':declared,'endpointAliases':aliases,'fixedNativeCropFeet':feet,'nativeHashes':hashes,'preview':'cardinal-paid-clock.gif','scope':'All captured selected native source changes and completion, exact source RGBA; same148 ruler/p92,172 master comparisons. First occurrences, not every repeat occurrence. Preview reconstructs fourteen-second paid clock at50Hz from native-verified original sources; source-only, no room effects or actual continuous gameplay footage. Dedicated wall availability/interior-start fixture; not naturally selected other walls in owner layouts.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'nativeBoards':len(boards),'sourceBoards':len(source_boards),'captures':len(rows),'sourceRefsCovered':declared,'aliases':aliases,'feet':feet}))
