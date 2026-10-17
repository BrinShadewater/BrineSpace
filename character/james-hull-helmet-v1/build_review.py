from pathlib import Path
import json, math, hashlib
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
clips={s['id']:s for s in read(R/'character/james-torch-material-residue-v2/helmet-manifest.json')['states']}
bare={s['id']:s for s in read(R/'character/james-torch-material-residue-v2/bare-manifest.json')['states']}
assert clips.keys()==bare.keys()
for key in clips:
    assert clips[key]['frameDurationsMs']==bare[key]['frameDurationsMs']
    assert len(clips[key]['frameFiles'])==len(bare[key]['frameFiles'])
master_root=R/'character/james-shared-helmet-runtime-v1'
masters={s['id']:s for s in read(master_root/'manifest.json')['states']}
def source(row):
    key=row['key'];index=row['index']
    if key.startswith('idle-'):key=key.replace('idle-','torch-draw-');index=0
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==row['sourceHash']
    return im
reports={}
families=['north','cardinal','return','reassign']
for family in families:
    p=P/family/'native-evidence.json'
    if not p.exists():continue
    evidence=read(p);assert evidence['failures']==0
    rows=evidence['records'];sources=[source(row) for row in rows]
    native_boards=[];source_boards=[]
    for page in range(math.ceil(len(rows)/48)):
        batch=rows[page*48:(page+1)*48]
        b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');draw=ImageDraw.Draw(b)
        for n,row in enumerate(batch):
            fx,fy=row.get('footViewport',row.get('stretchFoot'))
            im=Image.open(R/row['path'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20))
            x=n%8*150;y=n//8*165;b.paste(im,(x,y+20));draw.text((x+3,y+3),row['key'],fill='white');draw.text((x+3,y+151),'#'+str(row['index']),fill='white')
        name=f'{family}-native-page{page}.png';b.save(P/name);native_boards.append(name)
    for page in range(math.ceil(len(rows)/40)):
        batch=rows[page*40:(page+1)*40]
        b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');draw=ImageDraw.Draw(b)
        for n,row in enumerate(batch):
            x=n%5*184;y=n//5*204;im=sources[page*40+n];b.paste(im,(x,y+20),im);draw.text((x+3,y+3),row['key']+' #'+str(row['index']),fill='white')
        name=f'{family}-source-page{page}.png';b.save(P/name);source_boards.append(name)
    reports[family]={'checks':evidence['checks'],'captures':len(rows),'sourceRGBAMatches':len(rows),'nativeBoards':native_boards,'sourceBoards':source_boards}
board=Image.new('RGB',(1104,864),'#303b40');draw=ImageDraw.Draw(board)
for n,direction in enumerate(['north','east','south','west']):
    master=Image.open(master_root/masters['idle-'+direction]['frameFiles'][0]).convert('RGBA')
    clip=lambda key,index:Image.open(R/clips[key+'-'+direction]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    poses=[master,clip('torch-draw',0),clip('weld',0),clip('weld',len(clips['weld-'+direction]['frameFiles'])//2),clip('torch-stow',-1),master]
    for column,(label,im) in enumerate(zip(['master','draw entry','held start','held middle','stow end','master'],poses)):
        x=column*184;y=n*216;board.paste(im,(x,y+20),im);draw.text((x+3,y+3),direction+' / '+label,fill='white');draw.line((x+20,y+192,x+164,y+192),fill='#657276')
board.save(P/'master-comparison.png')
frames=[]
for t in range(0,15000,20):
    b=Image.new('RGB',(800,240),'#303b40');draw=ImageDraw.Draw(b)
    draw.text((8,5),'James helmeted hull repair / original sources at14-second paid clock',fill='white')
    for n,direction in enumerate(['north','east','south','west']):
        work=min(t/1000,14)
        key='torch-draw-'+direction;elapsed=work
        if work>=13.48:key='torch-stow-'+direction;elapsed=work-13.48
        elif work>=.52:
            key='weld-'+direction;cycle=sum(clips[key]['frameDurationsMs'])/1000;budget=12.96
            elapsed=((work-.52)/budget*max(1,math.floor(budget/cycle+.5))*cycle)%cycle
        durations=clips[key]['frameDurationsMs'];slot=len(durations)-1;cursor=0
        for i,ms in enumerate(durations):
            cursor+=ms/1000
            if elapsed<cursor:slot=i;break
        im=Image.open(R/clips[key]['frameFiles'][slot].removeprefix('res://')).convert('RGBA');b.paste(im,(n*200+8,35),im);draw.text((n*200+8,224),direction,fill='white')
    frames.append(b)
frames[0].save(P/'paid-clock.gif',save_all=True,append_images=frames[1:],duration=20,loop=0,disposal=2)
(P/'review-evidence.json').write_text(json.dumps({'families':reports,'pairedTimingParity':True,'masterComparison':'master-comparison.png','preview':'paid-clock.gif','scope':'Native source-slot captures cropped at each recorded physical foot; exact original paired helmet RGBA. Preview reconstructs14-second paid clock, not continuous native effects footage. Dedicated cardinal fixture prescribes clear interior start and available wall band; no owner-layout or locker fitting acceptance.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports))
