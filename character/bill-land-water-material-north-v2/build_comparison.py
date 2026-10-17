"""Compare the material revision at identical actual source, root, clock and water."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageStat,ImageChops
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-north-v1'
O=R/'output'/P.name
new=json.loads((O/'records.json').read_text(encoding='utf-8'))
old=json.loads((R/'output'/OLD.name/'records.json').read_text(encoding='utf-8'))
before={r['name']:r for r in old['records'] if 'foot' in r};after={r['name']:r for r in new['records'] if 'foot' in r}
assert before.keys()==after.keys()
same=[];differences=[]
for name,r in after.items():
 a=before[name]
 for field in ['foot','state','direction','materialWeight','materialHeadOffset','bridgeActive']:
  assert a[field]==r[field],(name,field,a[field],r[field])
 if 'tick' in r:
  for field in ['tick','clock','water','medium','pathPoints','goal','cell']:assert a[field]==r[field],(name,field)
 left=Image.open(OLD/'captures'/f'{name}-source.png').convert('RGBA');right=Image.open(P/'captures'/f'{name}-source.png').convert('RGBA')
 assert left.size==right.size and left.tobytes()==right.tobytes(),name
 same.append(name)
 selected=[69,72,75,78,81,84,87,90,93,96]
board=Image.new('RGB',(2000,880),'#182932');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for col,tick in enumerate(selected):
  name=f'{gear}-{tick:03d}-candidate';r=after[name]
  cx=255+(r['foot'][0]-7680)*398/384;cy=287+(r['foot'][1]-8064)*398/384
  crops=[]
  for path in [OLD,P]:crops.append(Image.open(path/'captures'/f'{name}-room.png').convert('RGB').crop((round(cx)-100,round(cy)-130,round(cx)+100,round(cy)+70)))
  x=col*200;y=row*440
  board.paste(crops[0],(x,y+20));board.paste(crops[1],(x,y+240));draw.text((x+3,y+3),f'{gear} {tick} previous',fill='white');draw.text((x+3,y+223),f'{gear} {tick} revised',fill='white')
  differences.append(dict(name=name,changedPixelBounds=ImageChops.difference(*crops).getbbox()))
board.save(P/'waterline-comparison.png')
result=dict(sourceRootClockWaterExactPairs=len(same),selectedNativeComparisons=differences,scope='Fixed native pixel scale and root crop; same actual source/pose/controller clock/water. Changed waterline and associated wake composition only; brightness and contact acceptance require visual review.')
(P/'comparison.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
html=(P/'index.html').read_text(encoding='utf-8');html+='<h2>Native waterline before/after</h2><p>Previous above, revised below, fixed native scale and identical source/root/clock/water.</p><img src="waterline-comparison.png">'
(P/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(dict(exactPairs=len(same),nativeComparisons=len(differences))))
