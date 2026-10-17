from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
clips={s['id']:s for s in read(R/'character/james-torch-material-residue-v2/helmet-manifest.json')['states']}
reports={}
files={direction: direction+"/evidence.json" for direction in ["east","south","west"]}
def source(row):
    key=row['key'];index=row['index']
    if key.startswith('idle-'):key=key.replace('idle-','torch-draw-');index=0
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==row['sourceHash']
    return im
for family,relative in files.items():
    evidence=read(P/relative);assert evidence['failures']==0
    rows=evidence['records'];sources=[source(row) for row in rows]
    unique={}
    for row,im in zip(rows,sources):
        if row['capture'] not in unique:unique[row['capture']]=(row,im)
    views=list(unique.values());native_boards=[];source_boards=[]
    for page in range(math.ceil(len(views)/64)):
        batch=views[page*64:(page+1)*64];b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');draw=ImageDraw.Draw(b)
        for n,(row,im) in enumerate(batch):
            fx,fy=row['footViewport'];native=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20))
            x=n%8*150;y=n//8*165;b.paste(native,(x,y+20));draw.text((x+3,y+3),row['key'],fill='white');draw.text((x+3,y+151),'#'+str(row['index']),fill='white')
        name=f'{family}-native-page{page}.png';b.save(P/name);native_boards.append(name)
    for page in range(math.ceil(len(views)/40)):
        batch=views[page*40:(page+1)*40];b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');draw=ImageDraw.Draw(b)
        for n,(row,im) in enumerate(batch):
            x=n%5*184;y=n//5*204;b.paste(im,(x,y+20),im);draw.text((x+3,y+3),row['key']+' #'+str(row['index']),fill='white')
        name=f'{family}-source-page{page}.png';b.save(P/name);source_boards.append(name)
    reports[family]={'checks':evidence['checks'],'records':len(rows),'sourceRGBAMatches':len(rows),'distinctCaptures':len(views),'nativeBoards':native_boards,'sourceBoards':source_boards}
master_root=R/'character/james-shared-helmet-runtime-v1';masters={s['id']:s for s in read(master_root/'manifest.json')['states']}
board=Image.new('RGB',(1104,864),'#303b40');draw=ImageDraw.Draw(board)
for n,d in enumerate(['north','east','south','west']):
    master=Image.open(master_root/masters['idle-'+d]['frameFiles'][0]).convert('RGBA')
    clip=lambda key,index:Image.open(R/clips[key+'-'+d]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    poses=[master,clip('torch-draw',0),clip('weld',0),clip('weld',len(clips['weld-'+d]['frameFiles'])//2),clip('torch-stow',-1),master]
    for column,(label,im) in enumerate(zip(['master','draw entry','held start','held middle','stow end','master'],poses)):
        x=column*184;y=n*216;board.paste(im,(x,y+20),im);draw.text((x+3,y+3),d+' / '+label,fill='white');draw.line((x+20,y+192,x+164,y+192),fill='#657276')
board.save(P/'master-comparison.png')
frames=[]
motion_rows=[r for r in read(P/'east/evidence.json')['records'] if r['label']=='east-weld-power']
for row in motion_rows:
    b=Image.new('RGB',(600,240),'#303b40');draw=ImageDraw.Draw(b)
    draw.text((8,5),'James helmeted construction power loss / source pose order',fill='white')
    im=source(row)
    for x,height in [(90,148),(275,82),(420,54),(545,27)]:
        scale=height/148;small=im.resize((round(184*scale),round(184*scale)),Image.Resampling.LANCZOS)
        b.paste(small,(round(x-92*scale),round(214-172*scale)),small)
    frames.append(b)
frames[0].save(P/'interruption-source-order.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2)
(P/'review-evidence.json').write_text(json.dumps({'families':reports,'masterComparison':'master-comparison.png','preview':'interruption-source-order.gif','scope':'Native work/motion views cropped at recorded physical foot; all recorded sourceRGBA checked, repeated lifecycle slots reuse first native capture. Original paired matte sources and four-direction helmet masters. GIF50ms per captured source pose is simplified interruption order, not continuous real-time native gameplay footage.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(reports))
