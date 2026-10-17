from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output'/P.name
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert validation['passed'],validation
data=json.loads((O/'records.json').read_text(encoding='utf-8'));inventory=json.loads((P/'source-inventory.json').read_text(encoding='utf-8'))
dest=P/'captures';dest.mkdir(exist_ok=True);records=[r for r in data['records'] if 'foot' in r]
registrations={};hashes={}
for r in records:
 name=r['name']
 for kind in ['source','room']:
  f=O/f'{name}-{kind}.png';shutil.copy2(f,dest/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 im=Image.open(dest/f'{name}-source.png').convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest();assert key in inventory,(name,key)
 registrations[name]=inventory[key]
def physical_source(name):
 source=Image.open(dest/f'{name}-source.png').convert('RGBA');profiles=registrations[name];profile=profiles[0]
 assert all((p['pivot'],p['standingHeight'])==(profile['pivot'],profile['standingHeight']) for p in profiles),name
 scale=2*65.28/profile['standingHeight'];painted=source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS)
 result=Image.new('RGBA',(400,400));result.alpha_composite(painted,(round(200-profile['pivot'][0]*scale),round(280-profile['pivot'][1]*scale)));return result.resize((180,180),Image.Resampling.LANCZOS)
def native_crop(r):
 cx=255+(r['foot'][0]-7680)*398/384;cy=287+(r['foot'][1]-8064)*398/384
 return Image.open(dest/f"{r['name']}-room.png").crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70))
boards=[]
for gear,phase,lo,hi in [('bare','entry',60,105),('helmet','entry',60,105),('bare','exit',410,460),('helmet','exit',410,460)]:
 rows=[r for r in records if r['name'].startswith(gear+'-') and 'tick' in r and lo<=r['tick']<hi];assert len(rows)==hi-lo
 source_board=Image.new('RGB',(1500,((len(rows)+7)//8)*240),'#182932');native_board=Image.new('RGB',(1600,((len(rows)+7)//8)*220),'#182932')
 sd=ImageDraw.Draw(source_board);nd=ImageDraw.Draw(native_board)
 for i,r in enumerate(rows):
  x=(i%8)*187;y=(i//8)*240;image=physical_source(r['name']);source_board.paste(image,(x+3,y+25),image);sd.text((x+3,y+3),f"tick{r['tick']} {r['state']}",fill='white')
  x=(i%8)*200;y=(i//8)*220;native_board.paste(native_crop(r),(x,y+20));nd.text((x+3,y+3),f"tick{r['tick']} wet{r['materialWeight']:.2f}",fill='white')
 for kind,board in [('source',source_board),('native',native_board)]:
  file=f'{gear}-{phase}-{kind}.png';board.save(P/file);boards.append(file)
guards=[r for r in records if '-guard-' in r['name']];assert len(guards)==28
board=Image.new('RGB',(1400,880),'#182932');draw=ImageDraw.Draw(board)
for i,r in enumerate(guards):
 x=(i%7)*200;y=(i//7)*220;board.paste(native_crop(r),(x,y+20));draw.text((x+3,y+3),r['name'].replace('-candidate',''),fill='white')
board.save(P/'native-guards.png');boards.append('native-guards.png')
html='<!doctype html><meta charset="utf-8"><title>Bill North native entry and exit</title><style>body{background:#182932;color:#ddd;font:16px sans-serif}img{max-width:100%}</style><h1>Bill North native entry and independent exit</h1><p>Actual normal actor/player on prescribed graph-clear workshop route and water rise/hold/drain. Common physical source canvases and fixed native-scale root-follow crops. Full master/grade/contact/motion acceptance and checkpoint/Continue pending.</p>'
for file in boards:html+=f'<h2>{file}</h2><img src="{file}">'
for r in records:
 name=r['name'];html+=f'<details><summary>{name}</summary><img src="captures/{name}-room.png"><img src="captures/{name}-source.png"></details>'
(P/'index.html').write_text(html,encoding='utf-8')
(P/'review.json').write_text(json.dumps(dict(validation=validation,checks=data['checks'],failures=data['failures'],capturePairs=len(records),sourceRegistration=registrations,captureHashes=hashes,visualReview='Pending actual native image inspection.',scope=data['scope']),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=data['checks'],pairs=len(records),sourcesExact=len(registrations),boards=boards)))
