from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-east-v2';O=R/'output/bill-land-water-material-east-v3'
s=(P.parent/'bill-land-water-runtime-east-v1/build_review.py').read_text(encoding='utf-8').replace('bill-land-water-runtime-east-v1','bill-land-water-material-east-v3')
s=s.replace("rows=[x for x in data['records'] if x['name'].endswith('-candidate')]","rows=[x for x in data['records'] if x['name'].endswith('-candidate') and 'tick' in x]")
exec(compile(s,str(P/'build_review.py'),'exec'),{'__file__':str(P/'build_review.py')})
data=json.loads((O/'records.json').read_text());rows=[x for x in data['records'] if x['name'].endswith('-candidate') and 'tick' in x];prior=json.loads((R/'output/bill-land-water-material-east-v2/records.json').read_text());byname={x['name']:x for x in prior['records'] if 'tick' in x}
source_equal=0;native_equal=0
for row in rows:
 old=byname[row['name']];assert row['foot']==old['foot'] and row['water']==old['water'] and row['state']==old['state'] and row['direction']==old['direction']
 for kind in ['source','room']:
  equal=Image.open(P/'captures'/f"{row['name']}-{kind}.png").convert('RGBA').tobytes()==Image.open(OLD/'captures'/f"{row['name']}-{kind}.png").convert('RGBA').tobytes()
  if kind=='source':assert equal;source_equal+=equal
  else:native_equal+=equal
guards=[x for x in data['records'] if '-guard-' in x['name']];assert len(guards)==14
board=Image.new('RGB',(1400,850),'#182932');d=ImageDraw.Draw(board);hashes={}
for line,gear in enumerate(['bare','helmet']):
 group=[x for x in guards if x['name'].startswith(gear+'-')];assert len(group)==7
 for col,row in enumerate(group):
  name=row['name'];x=255+(row['foot'][0]-7680)*398/384;y=287+(row['foot'][1]-8064)*398/384
  for kind in ['source','room']:
   f=O/f'{name}-{kind}.png';shutil.copy2(f,P/'captures'/f.name);hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
  im=Image.open(P/'captures'/f'{name}-room.png').crop((round(x)-100,round(y)-130,round(x)+100,round(y)+70));board.paste(im,(col*200,line*425+20))
  source=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA');source.thumbnail((180,180),Image.Resampling.LANCZOS);board.paste(source,(col*200+(200-source.width)//2,line*425+230),source)
  d.text((col*200+3,line*425+3),f"{gear} {name.split('-guard-')[1].split('-candidate')[0]}",fill='white');d.text((col*200+3,line*425+410),f"material {row['materialWeight']:.3f}; raw source",fill='white')
board.save(P/'native-guards.png')
e=json.loads((P/'review.json').read_text());e.update(sourceCapturesExactToV2=source_equal,nativeCapturesExactToV2=native_equal,worldAndWaterExactToV2=True,nativeGuardPresentations=guards,nativeGuardCaptureSHA256=hashes,scope='190advancing boundary presentations plus14native synthetic active/takeover presentations. Source/world/water parity to V2 checked. Guard source thumbnails retain original canvas proportions, are not common-pivot registered.8APNG380decoded intervals cover advancing boundaries only; guard snapshots are separate evidence.');(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8').replace('Bill East — staged moving land/water bridge','Bill East — live material binding and takeovers').replace('<h2>bare enter','<h2>Native synthetic guards</h2><p>Active bridge followed by gear/facing/death/action/clock/geometry takeover. Normal material restored; these snapshots do not prove natural priority completion.</p><img src="native-guards.png"><h2>bare enter',1);(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(nativeGuards=len(guards),sourceExactToV2=source_equal,nativeExactToV2=native_equal,totalBoundaryPresentations=len(rows))))
