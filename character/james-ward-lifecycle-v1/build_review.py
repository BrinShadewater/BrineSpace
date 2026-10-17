from pathlib import Path
import json, hashlib, math
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
main=json.loads((P/'native-evidence.json').read_bytes()); pause=json.loads((P/'pause-evidence.json').read_bytes())
rows=main['records']+pause['records']
m=json.loads((R/'character/james-torch-material-residue-v2/bare-manifest.json').read_bytes()); clips={s['id']:s for s in m['states']}
def source(r):
    key='torch-draw-north' if r['key'].startswith('idle-') else r['key']; index=0 if r['key'].startswith('idle-') else r['index']
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==r['sourceHash']
    return im
sources=[source(r) for r in rows]
assert len({tuple(r['foot']) for r in rows})==1
native_boards=[]; source_boards=[]
for page in range(math.ceil(len(rows)/48)):
    batch=rows[page*48:(page+1)*48]; b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40'); d=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%8*150;y=n//8*165;fx,fy=r['footViewport']
        im=Image.open(R/r['path'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20))
        b.paste(im,(x,y+20));d.text((x+3,y+3),r['label'],fill='white');d.text((x+3,y+151),r['key']+f" #{r['index']}",fill='white')
    name=f'native-page{page}.png';b.save(P/name);native_boards.append(name)
for page in range(math.ceil(len(rows)/40)):
    batch=rows[page*40:(page+1)*40];b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');d=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%5*184;y=n//5*204;im=sources[page*40+n];b.paste(im,(x,y+20),im);d.text((x+3,y+3),r['key']+f" #{r['index']}",fill='white')
    name=f'source-page{page}.png';b.save(P/name);source_boards.append(name)
master_root=R/'character/crew-runtime-matte-v1/branforth';mm=json.loads((master_root/'manifest.json').read_bytes());ms={s['id']:s for s in mm['states']}
master_path=master_root/ms['idle-north']['frameFiles'][0]; master=Image.open(master_path).convert('RGBA')
held=[im for r,im in zip(rows,sources) if r['key']=='weld-north']
examples=[('standing master',master),('draw entry',sources[0]),('held first',held[0]),('held middle',held[len(held)//2]),('stow end',Image.open(R/clips['torch-stow-north']['frameFiles'][-1].removeprefix('res://')).convert('RGBA')),('completed idle',sources[next(i for i,r in enumerate(rows) if r['key']=='idle-north')])]
b=Image.new('RGB',(1104,216),'#303b40');d=ImageDraw.Draw(b)
for n,(label,im) in enumerate(examples):
    x=n*184;b.paste(im,(x,20),im);d.text((x+3,3),label,fill='white');d.line((x+20,192,x+164,192),fill='#657276')
b.save(P/'master-comparison.png')
def timed(work):
    key='torch-draw-north';elapsed=work
    if work>=18:return key,0
    if work>=17.48:key='torch-stow-north';elapsed=work-17.48
    elif work>=.52:
        key='weld-north';cycle=sum(clips[key]['frameDurationsMs'])/1000;budget=16.96;loops=max(1,math.floor(budget/cycle+.5));elapsed=((work-.52)/budget*loops*cycle)%cycle
    for i,ms in enumerate(clips[key]['frameDurationsMs']):
        if elapsed<ms/1000:return key,i
        elapsed-=ms/1000
    return key,len(clips[key]['frameFiles'])-1
for r in main['records']:
    if r['label'].startswith('actual-') and not r['key'].startswith('idle-'):assert timed(r['work'])==(r['key'],r['index'])
covered={r['sourceHash'] for r in rows};frames=[];cache={}
for tick in range(951):
    work=min(18,tick*.02);key,index=timed(work);token=(key,index)
    if token not in cache:cache[token]=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    im=cache[token];assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest() in covered
    b=Image.new('RGB',(600,240),'#303b40');d=ImageDraw.Draw(b);d.text((8,7),'James ward repair / 18-second paid-clock source preview',fill='white')
    for x,height in [(90,148),(270,82),(420,54),(540,27)]:
        scale=height/148;scaled=im.resize((round(184*scale),round(184*scale)),Image.Resampling.LANCZOS);b.paste(scaled,(round(x-92*scale),round(212-172*scale)),scaled);d.text((x-15,223),f'{height}px',fill='white')
    frames.append(b)
frames[0].save(P/'ward-paid-clock.gif',save_all=True,append_images=frames[1:],duration=20,loop=0,disposal=2)
review={'nativeBoards':native_boards,'sourceBoards':source_boards,'masterComparison':'master-comparison.png','masterPath':str(master_path.relative_to(R)),'captures':len(rows),'nativeRGBAMatches':len(rows),'physicalFoot':rows[0]['foot'],'preview':'ward-paid-clock.gif','nativeHashes':{r['path']:hashlib.sha256((R/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows},'scope':'52 actual lifecycle captures plus27 pause/reentry captures. Original whole-source RGBA matches, same148 ruler/p92,172 master comparison. Native crops use each recorded viewport foot: awarded room recenters camera at completion, physical foot stays fixed. Preview reconstructs18-second paid clock at50Hz plus1-second neutral hold from native-matched sources; source-only, no continuous gameplay lighting/effects footage. North dry bare James in dedicated normal ward worksite fixture.'}
(P/'review-evidence.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'captures':len(rows),'nativeBoards':native_boards,'sourceBoards':source_boards}))
