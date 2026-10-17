from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
inventory=(R/'character/james-animation-coverage-2026-09-30/audit.py').read_text()
exec(compile(inventory,'selection_inventory','exec'),{'__file__':str(P/'audit.py')})
coverage=read(P/'runtime-coverage.json')
e=read(P/'evidence.json');assert e['failures']==0
def source(row):
    file=R/coverage['equipment' if row['gear'] else 'body'][row['key']]['path']
    m=read(file);s=next(s for s in m['states'] if s['id']==row['key'])
    rel=s['frameFiles'][row['index']];p=R/rel.removeprefix('res://') if rel.startswith('res://') else file.parent/rel
    im=Image.open(p).convert('RGBA')
    assert hashlib.sha256(im.tobytes().hex().encode()).hexdigest()==row['sourceHash']
    assert m['standingHeight']==row['standingHeight'] and m['pivot']==row['pivot']
    canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-m['pivot'][0]),round(224-m['pivot'][1])))
    return canvas
review={}
for direction in ['north','east','south','west']:
    rows=[r for r in e['records'] if r['leg'].startswith(direction+'-')];images=[source(r) for r in rows]
    native=[];sources=[]
    for page in range(math.ceil(len(rows)/64)):
        batch=rows[page*64:(page+1)*64];b=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');d=ImageDraw.Draw(b)
        for i,row in enumerate(batch):
            fx,fy=row['footViewport'];im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));x=i%8*150;y=i//8*165
            b.paste(im,(x,y+20));d.text((x+3,y+3),row['key'],fill='white');d.text((x+3,y+152),str(row['index'])+' '+row['gear'],fill='white')
        name=f'{direction}-native-page{page}.png';b.save(P/name);native.append(name)
    for page in range(math.ceil(len(rows)/40)):
        batch=list(zip(rows,images))[page*40:(page+1)*40];b=Image.new('RGB',(1000,math.ceil(len(batch)/5)*210),'#303b40');d=ImageDraw.Draw(b)
        for i,(row,im) in enumerate(batch):
            x=i%5*200;y=i//5*210;im=im.crop((28,36,228,236));b.paste(im,(x,y+10),im);d.text((x+3,y+3),row['key']+' '+str(row['index']),fill='white')
        name=f'{direction}-source-page{page}.png';b.save(P/name);sources.append(name)
    review[direction]={'records':len(rows),'sourceRGBAMatches':len(rows),'nativeBoards':native,'sourceBoards':sources}
# Fitting endpoints share the physical ruler with the selected bare/helmet idle.
b=Image.new('RGB',(1200,250),'#303b40');d=ImageDraw.Draw(b)
rows=[r for r in e['records'] if r['leg']=='north-locker' and r['key']=='equip-helmet-east']
for col,index in enumerate([0,2,4,6,8,11]):
    row=next(r for r in rows if r['index']==index);im=source(row).crop((28,36,228,236));b.paste(im,(col*200,30),im);d.text((col*200+5,8),'helmet fitting '+str(index),fill='white')
b.save(P/'fitting-contact.png')
def normalized(mode,key,index=0):
    file=R/coverage['body' if mode=='bare' else 'equipment'][key]['path'];m=read(file);s=next(s for s in m['states'] if s['id']==key)
    rel=s['frameFiles'][index];p=R/rel.removeprefix('res://') if rel.startswith('res://') else file.parent/rel
    im=Image.open(p).convert('RGBA');canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-m['pivot'][0]),round(224-m['pivot'][1])));return canvas
bare=normalized('bare','idle-east');helmet=normalized('helmet','idle-east')
first=source(next(r for r in rows if r['index']==0));last=source(next(r for r in rows if r['index']==11))
endpoints={'bareEntryExact':bare.tobytes()==first.tobytes(),'helmetExitExact':helmet.tobytes()==last.tobytes()}
b=Image.new('RGB',(1200,250),'#303b40');d=ImageDraw.Draw(b)
for i,(label,im) in enumerate([('bare master',bare),('fitting entry',first),('fitting end',last),('helmet master',helmet),('torch draw entry',normalized('helmet','torch-draw-east')),('torch stow end',normalized('helmet','torch-stow-east',-1))]):
    im=im.crop((28,36,228,236));b.paste(im,(i*200,30),im);d.text((i*200+5,8),label,fill='white')
b.save(P/'master-fitting-torch-joins.png')
(P/'review-evidence.json').write_text(json.dumps({'directions':review,'checks':e['checks'],'captures':len(e['records']),'fittingEndpoints':endpoints,'scope':'Actual AirlockService route, fitting and paid build native/source views, captured once per source slot per leg. Full original RGBA verified and declared pivot/standing ruler checked. No continuously watched real-time or every-position routing proof.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':e['checks'],'captures':len(e['records']),'directions':review}))
