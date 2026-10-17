from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,math
H=Path(__file__).resolve().parent
name=sys.argv[1] if len(sys.argv)>1 else 'review-v2';D=H/name
q=json.loads((D/'report.json').read_text());chosen={}
for r in q['records']:
 source=r['source'];gear=r['episode'].split('-')[-1] if name=='review-v2' else r['episode'].split('-')[0]
 if source:chosen.setdefault((gear,source['key'],source['index']),r)
rows=list(chosen.values())
if '--sample' in sys.argv:
 groups={}
 for key,r in chosen.items():groups.setdefault(key[:2],[]).append(r)
 rows=[]
 for key,items in groups.items():
  items.sort(key=lambda r:r['source']['index'])
  picks=range(len(items)) if '-turn-' in key[1] else sorted(set(round(i*(len(items)-1)/6) for i in range(7)))
  rows.extend(items[i] for i in picks)
 name+='-sampled'
out=H/(name+'-witnesses');out.mkdir(exist_ok=True)
for page in range(math.ceil(len(rows)/20)):
 board=Image.new('RGB',(1200,4*265),'#1b272d');d=ImageDraw.Draw(board)
 for i,r in enumerate(rows[page*20:page*20+20]):
  x=i%5*240;y=i//5*265;im=Image.open(D/r['file']).convert('RGB')
  factor=min(2,225/im.width,220/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST)
  board.paste(im,(x+(240-im.width)//2,y+39));d.text((x+5,y+4),r['episode'].replace('salvage_workshop','workshop').replace('observation_room','reading')[:34],fill='white');d.text((x+5,y+19),str(r['source']['key'])+' / '+str(r['source']['index']),fill='#b8dce2')
 board.save(out/('review-%02d.png'%page))
(H/(name+'-witness-index.json')).write_text(json.dumps({'captures':len(q['records']),'uniqueSelectedPoses':len(rows),'pages':math.ceil(len(rows)/20),'selected':rows},indent=2))
print({'lane':name,'captures':len(q['records']),'uniqueSelectedPoses':len(rows),'pages':math.ceil(len(rows)/20)})
