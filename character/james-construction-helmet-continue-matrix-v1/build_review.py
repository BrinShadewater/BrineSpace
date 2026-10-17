from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
clips={s['id']:s for s in read(R/'character/james-torch-material-residue-v2/helmet-manifest.json')['states']}
reports={}
files={direction: direction+"/continue-evidence.json" for direction in ["north","east","south","west"]}
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
(P/"review-evidence.json").write_text(json.dumps({"families":reports,"masterComparison":"master-comparison.png","scope":"Before/after fresh main-scene disk Continue and first five changed resumed source poses. Native foot crops, exact original helmet RGBA and four-direction master board. Not every resumed source slot or continuously watched native motion."},indent=2)+"\n",encoding="utf-8")
print(json.dumps(reports))
