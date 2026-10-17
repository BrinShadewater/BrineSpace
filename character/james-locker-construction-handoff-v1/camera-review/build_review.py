from pathlib import Path
import json,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2]
def read(p):return json.loads(p.read_bytes())
a=read(P.parent/'evidence.json');b=read(P/'evidence.json');g=read(P/'validate-validation.json')
assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
a['cases']=[c for c in a['cases'] if c['direction'] in ['south','west']];a['records']=[r for r in a['records'] if r['leg'].startswith(('south-','west-'))]
assert a['cases']==b['cases'] and len(a['records'])==len(b['records'])
for x,y in zip(a['records'],b['records']):
 assert {k:v for k,v in x.items() if k not in ['capture','footViewport']}=={k:v for k,v in y.items() if k not in ['capture','footViewport']}
review={}
for direction in ['south','west']:
 rows=[r for r in b['records'] if r['leg'].startswith(direction+'-')];names=[]
 for page in range(math.ceil(len(rows)/64)):
  batch=rows[page*64:(page+1)*64];im=Image.new('RGB',(1200,math.ceil(len(batch)/8)*165),'#303b40');d=ImageDraw.Draw(im)
  for i,row in enumerate(batch):
   fx,fy=row['footViewport'];shot=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB');assert 150<fx<shot.width-150 and 180<fy<shot.height-30
   crop=shot.crop((round(fx)-75,round(fy)-115,round(fx)+75,round(fy)+20));x=i%8*150;y=i//8*165;im.paste(crop,(x,y+20));d.text((x+3,y+3),row['key'],fill='white');d.text((x+3,y+152),str(row['index']),fill='white')
  name=f'{direction}-native-page{page}.png';im.save(P/name);names.append(name)
 review[direction]=names
(P/'review-evidence.json').write_text(json.dumps({'boards':review,'records':len(b['records']),'originalPoseClockSourceMatches':True,'scope':'Camera-only review repeat; ordinary game advancement unchanged. Original run has South/West UI-covered or offscreen captures; these boards replace their visual evidence. Per-leg source views do not establish native cadence.'},indent=2)+'\n')
print(json.dumps({'checks':b['checks'],'records':len(b['records']),'boards':sum(map(len,review.values()))}))
