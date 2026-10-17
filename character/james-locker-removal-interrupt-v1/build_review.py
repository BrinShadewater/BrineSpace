from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
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
rows=e['records'];images=[source(r) for r in rows]
for kind,count,columns,width,height in [('native',64,8,150,165),('source',40,5,200,210)]:
 names=[]
 for page in range(math.ceil(len(rows)/count)):
  batch=list(zip(rows,images))[page*count:(page+1)*count];b=Image.new('RGB',(columns*width,math.ceil(len(batch)/columns)*height),'#303b40');d=ImageDraw.Draw(b)
  for i,(row,im) in enumerate(batch):
   x=i%columns*width;y=i//columns*height
   if kind=='source':
    im=im.crop((28,36,228,236));b.paste(im,(x,y+10),im)
   else:
    fx,fy=row['footViewport'];shot=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB');assert 100<fx<shot.width-100 and 130<fy<shot.height-30
    im=shot.crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));b.paste(im,(x,y+20))
   d.text((x+3,y+3),row['key']+' '+str(row['index']),fill='white')
   if kind=='native':d.text((x+3,y+152),'return' if '-return' in row['leg'] else 'forward/join',fill='white')
  name=f'{kind}-page{page}.png';b.save(P/name);names.append(name)
 review[kind]=names
# Exact full-source normal removal endpoints and shared physical pivot.
def normalized(mode,key,index=0):
 file=R/coverage['body' if mode=='bare' else 'equipment'][key]['path'];m=read(file);s=next(s for s in m['states'] if s['id']==key)
 rel=s['frameFiles'][index];p=R/rel.removeprefix('res://') if rel.startswith('res://') else file.parent/rel
 im=Image.open(p).convert('RGBA');canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(round(128-m['pivot'][0]),round(224-m['pivot'][1])));return canvas
bare=normalized('bare','idle-east');helmet=normalized('helmet','idle-east');first=normalized('bare','remove-helmet-east');last=normalized('bare','remove-helmet-east',-1)
endpoints={'helmetEntryExact':helmet.tobytes()==first.tobytes(),'bareExitExact':bare.tobytes()==last.tobytes()};assert all(endpoints.values())
b=Image.new('RGB',(1200,250),'#303b40');d=ImageDraw.Draw(b)
for i,index in enumerate([0,2,4,6,8,11]):
 im=normalized('bare','remove-helmet-east',index).crop((28,36,228,236));b.paste(im,(i*200,30),im);d.text((i*200+5,8),'helmet removal '+str(index),fill='white')
b.save(P/'removal-contact.png')
(P/'review-evidence.json').write_text(json.dumps({'boards':review,'checks':e['checks'],'captures':len(rows),'sourceRGBAMatches':len(rows),'removalEndpoints':endpoints,'scope':e['scope']},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':e['checks'],'captures':len(rows),'boards':review,'endpoints':endpoints}))
