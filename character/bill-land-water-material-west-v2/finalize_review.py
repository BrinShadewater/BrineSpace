from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib, shutil
P=Path(__file__).resolve().parent; R=P.parent.parent; O=R/'output/bill-land-water-material-west-v2'
e=json.loads((P/'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and not e['validation']['realProfileChanges']
data=json.loads((O/'records.json').read_text(encoding='utf-8'))
guards=[x for x in data['records'] if '-guard-' in x['name']]; assert len(guards)==14
board=Image.new('RGB',(1400,850),'#182932'); d=ImageDraw.Draw(board); hashes={}
for line,gear in enumerate(['bare','helmet']):
 group=[x for x in guards if x['name'].startswith(gear+'-')]; assert len(group)==7
 for col,row in enumerate(group):
  name=row['name']; x=255+(row['foot'][0]-7680)*398/384; y=287+(row['foot'][1]-8064)*398/384
  for kind in ['source','room']:
   f=O/f'{name}-{kind}.png'; shutil.copy2(f,P/'captures'/f.name); hashes[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
  im=Image.open(P/'captures'/f'{name}-room.png').crop((round(x)-100,round(y)-130,round(x)+100,round(y)+70)); board.paste(im,(col*200,line*425+20))
  source=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA'); source.thumbnail((180,180),Image.Resampling.LANCZOS); board.paste(source,(col*200+(200-source.width)//2,line*425+230),source)
  d.text((col*200+3,line*425+3),f"{gear} {name.split('-guard-')[1].split('-candidate')[0]}",fill='white'); d.text((col*200+3,line*425+410),f"material {row['materialWeight']:.3f}; raw source",fill='white')
board.save(P/'native-guards.png')
prior=json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8'))
post={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in prior}
e.update(nativeGuardPresentations=guards,nativeGuardCaptureSHA256=hashes,targetedPostSHA256=post,targetedChanges=[f for f in prior if prior[f]!=post[f]],visualReview='Visual review pending West two complete advancing boards and fourteen guard pairs. Actual planar navigation/source bridge and finite material are technical evidence. Full master grade and continuous motion pending; exit bridge and checkpoints/Continue missing for West.')
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8')
if 'native-guards.png' not in html: html += '<h2>Interruption captures</h2><p>Synthetic active/takeover snapshots; natural action completion remains pending.</p><img src="native-guards.png">'
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(guardPairs=len(guards),targetedStable=len(prior)-len(e['targetedChanges']),targetedChanged=e['targetedChanges'])))
