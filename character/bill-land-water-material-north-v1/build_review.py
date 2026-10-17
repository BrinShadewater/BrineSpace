"""Publish actual captured evidence; passing mechanics do not certify art acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output'/P.name
data=json.loads((O/'records.json').read_text(encoding='utf-8'))
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert validation['passed'],validation
inventory=json.loads((P/'source-inventory.json').read_text(encoding='utf-8'))
dest=P/'captures';dest.mkdir(exist_ok=True)
records=[r for r in data['records'] if 'foot' in r]
registrations={};hashes={}
for r in records:
 name=r['name']
 for kind in ['source','room']:
  f=O/f'{name}-{kind}.png';shutil.copy2(f,dest/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 im=Image.open(dest/f'{name}-source.png').convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest()
 assert key in inventory,(name,key)
 registrations[name]=inventory[key]
boards=[]
for gear in ['bare','helmet']:
 rows=[r for r in records if r['name'].startswith(gear+'-') and 'tick' in r]
 assert len(rows)==45
 board=Image.new('RGB',(1500,((len(rows)+7)//8)*280),'#182932');draw=ImageDraw.Draw(board)
 for i,r in enumerate(rows):
  x=(i%8)*187;y=(i//8)*280;name=r['name']
  source=Image.open(dest/f'{name}-source.png').convert('RGBA')
  profiles=registrations[name];profile=profiles[0]
  assert all((p['pivot'],p['standingHeight'])==(profile['pivot'],profile['standingHeight']) for p in profiles),name
  scale=2*65.28/profile['standingHeight']
  painted=source.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS)
  physical=Image.new('RGBA',(400,400));physical.alpha_composite(painted,(round(200-profile['pivot'][0]*scale),round(280-profile['pivot'][1]*scale)))
  physical=physical.resize((180,180),Image.Resampling.LANCZOS)
  board.paste(physical,(x+3,y+35),physical)
  draw.text((x+3,y+3),f"{gear} tick{r['tick']} {r['state']}",fill='white')
  draw.text((x+3,y+260),f"wet {r['materialWeight']:.3f}",fill='white')
 file=f'{gear}-advancing-source.png';board.save(P/file);boards.append(file)
 native=Image.new('RGB',(1600,((len(rows)+7)//8)*220),'#182932');draw=ImageDraw.Draw(native)
 for i,r in enumerate(rows):
  # Same fixed-size crop around the captured physical root; no pose resizing.
  cx=255+(r['foot'][0]-7680)*398/384;cy=287+(r['foot'][1]-8064)*398/384
  room=Image.open(dest/f"{r['name']}-room.png")
  crop=room.crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70))
  x=(i%8)*200;y=(i//8)*220;native.paste(crop,(x,y+20))
  draw.text((x+3,y+3),f"tick{r['tick']} {r['state']} wet{r['materialWeight']:.2f}",fill='white')
 file=f'{gear}-advancing-native.png';native.save(P/file);boards.append(file)
guards=[r for r in records if '-guard-' in r['name']];assert len(guards)==14
board=Image.new('RGB',(1400,440),'#182932');draw=ImageDraw.Draw(board)
for i,r in enumerate(guards):
 cx=255+(r['foot'][0]-7680)*398/384;cy=287+(r['foot'][1]-8064)*398/384
 crop=Image.open(dest/f"{r['name']}-room.png").crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70))
 x=(i%7)*200;y=(i//7)*220;board.paste(crop,(x,y+20));draw.text((x+3,y+3),r['name'].replace('-candidate',''),fill='white')
board.save(P/'native-guards.png');boards.append('native-guards.png')
html='<!doctype html><meta charset="utf-8"><title>Bill North native entry review</title><style>body{background:#182932;color:#ddd;font:16px sans-serif}img{max-width:100%}</style><h1>Bill North native entry</h1><p>Actual normal actor on prescribed collision-clear room route and water history, both equipment states. Source boards are chronological captured textures; full room pairs retained below. Mechanics checks do not establish master consistency, floor contact or smooth motion. Source-bound head material placement is provisional.</p>'
for file in boards:html+=f'<img src="{file}">'
for r in records:
 name=r['name'];html+=f'<details><summary>{name}</summary><img src="captures/{name}-room.png"><img src="captures/{name}-source.png"></details>'
(P/'index.html').write_text(html,encoding='utf-8')
(P/'review.json').write_text(json.dumps(dict(validation=validation,checks=data['checks'],failures=data['failures'],capturePairs=len(records),sourceRegistration=registrations,captureHashes=hashes,visualReview='Pending actual native image inspection.',scope=data['scope']),indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=data['checks'],pairs=len(records),sourcesExact=len(registrations),boards=boards)))
