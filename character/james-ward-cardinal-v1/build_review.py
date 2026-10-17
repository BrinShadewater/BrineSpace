from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];directions=['east','south','west']
evidence={d:json.loads((P/d/'native-evidence.json').read_bytes()) for d in directions}
rows=[]
for facing,e in evidence.items():
    assert e['failures']==0
    assert len({tuple(r['foot']) for r in e['records']})==1
    rows.extend(dict(r,case=facing) for r in e['records'])
m=json.loads((R/'character/james-torch-material-residue-v2/bare-manifest.json').read_bytes());clips={s['id']:s for s in m['states']}
def source(r):
    key='torch-draw-'+r['case'] if r['key'].startswith('idle-') else r['key'];index=0 if r['key'].startswith('idle-') else r['index']
    im=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==r['sourceHash'];return im
sources=[source(r) for r in rows];native_boards=[];source_boards=[]
for page in range(math.ceil(len(rows)/64)):
    batch=rows[page*64:(page+1)*64];b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');draw=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%8*150;y=n//8*165;fx,fy=r['footViewport'];im=Image.open(R/r['path'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));b.paste(im,(x,y+20));draw.text((x+3,y+3),r['case']+' / '+r['label'],fill='white');draw.text((x+3,y+151),r['key']+f" #{r['index']}",fill='white')
    name=f'native-page{page}.png';b.save(P/name);native_boards.append(name)
for page in range(math.ceil(len(rows)/40)):
    batch=rows[page*40:(page+1)*40];b=Image.new('RGB',(920,math.ceil(len(batch)/5)*204),'#303b40');draw=ImageDraw.Draw(b)
    for n,r in enumerate(batch):
        x=n%5*184;y=n//5*204;im=sources[page*40+n];b.paste(im,(x,y+20),im);draw.text((x+3,y+3),r['key']+f" #{r['index']}",fill='white')
    name=f'source-page{page}.png';b.save(P/name);source_boards.append(name)
master_root=R/'character/crew-runtime-matte-v1/branforth';masters=json.loads((master_root/'manifest.json').read_bytes());master_states={s['id']:s for s in masters['states']}
master_board=Image.new('RGB',(1104,648),'#303b40');draw=ImageDraw.Draw(master_board);master_paths={}
for row,d in enumerate(directions):
    path=master_root/master_states['idle-'+d]['frameFiles'][0];master=Image.open(path).convert('RGBA');master_paths[d]=str(path.relative_to(R))
    local=[(r,im) for r,im in zip(rows,sources) if r['case']==d];held=[im for r,im in local if r['key']=='weld-'+d]
    examples=[('standing master',master),('draw entry',local[0][1]),('held first',held[0]),('held middle',held[len(held)//2]),('stow end',Image.open(R/clips['torch-stow-'+d]['frameFiles'][-1].removeprefix('res://')).convert('RGBA')),('completed idle',local[-1][1])]
    for col,(label,im) in enumerate(examples):
        x=col*184;y=row*216;master_board.paste(im,(x,y+20),im);draw.text((x+3,y+3),d+' / '+label,fill='white');draw.line((x+20,y+192,x+164,y+192),fill='#657276')
master_board.save(P/'master-comparison.png')
def timed(work,d):
    key='torch-draw-'+d;elapsed=work
    if work>=18:return key,0
    if work>=17.48:key='torch-stow-'+d;elapsed=work-17.48
    elif work>=.52:
        key='weld-'+d;cycle=sum(clips[key]['frameDurationsMs'])/1000;budget=16.96;loops=max(1,math.floor(budget/cycle+.5));elapsed=((work-.52)/budget*loops*cycle)%cycle
    for i,ms in enumerate(clips[key]['frameDurationsMs']):
        if elapsed<ms/1000:return key,i
        elapsed-=ms/1000
    return key,len(clips[key]['frameFiles'])-1
covered={r['sourceHash'] for r in rows}
for r in rows:
    if r['label'].startswith('actual-'):assert timed(r['work'],r['case'])==(r['key'],r['index'])
frames=[];cache={}
for tick in range(951):
    work=min(18,tick*.02);b=Image.new('RGB',(600,240),'#303b40');draw=ImageDraw.Draw(b);draw.text((8,7),'James ward repair / 18-second source clock / no room overlays',fill='white')
    for col,d in enumerate(directions):
        key,index=timed(work,d);token=(key,index)
        if token not in cache:cache[token]=Image.open(R/clips[key]['frameFiles'][index].removeprefix('res://')).convert('RGBA')
        im=cache[token];assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest() in covered
        x=col*200+8;b.paste(im,(x,32),im);draw.text((x+70,220),d,fill='white')
    frames.append(b)
frames[0].save(P/'ward-cardinal-paid-clock.gif',save_all=True,append_images=frames[1:],duration=20,loop=0,disposal=2)
report={'nativeBoards':native_boards,'sourceBoards':source_boards,'masterComparison':'master-comparison.png','masterPaths':master_paths,'captures':len(rows),'nativeRGBAMatches':len(rows),'checks':sum(e['checks'] for e in evidence.values()),'freshContinues':sum(len(e['checkpoints']) for e in evidence.values()),'cases':{d:{k:v for k,v in e.items() if k!='records'} for d,e in evidence.items()},'nativeHashes':{r['path']:hashlib.sha256((R/r['path'].removeprefix('res://')).read_bytes()).hexdigest() for r in rows},'preview':'ward-cardinal-paid-clock.gif','scope':'Three actual paid18-second/8Metal cryo ward jobs in dedicated rotated/relocated ward plus ordinary storage room fixtures. Genuine core release, actual full cross-room approach with no actor foot/facing/path/collision overrides. Three fresh disk Continues per direction. Original RGBA sources and148 ruler/p92,172 comparison. Source-only18-second50Hz preview plus neutral hold, not continuous gameplay effects footage. Not owner layouts/other gears/ward types/pause-work/power/door/flood/incoming worker acceptance.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['captures','checks','freshContinues','nativeBoards','sourceBoards']}))
