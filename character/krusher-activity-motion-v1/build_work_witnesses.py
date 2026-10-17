from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,math
H=Path(__file__).resolve().parent;lane=sys.argv[1];D=H/lane;q=json.loads((D/'report.json').read_text());groups={}
for r in q['records']:groups.setdefault((r['gear'],r['direction'],r['action']),[]).append(r)
rows=[]
for k,rs in groups.items():
 for i in sorted(set(round(i*(len(rs)-1)/6) for i in range(7))):rows.append(rs[i])
if lane.startswith('construction'):
 used={r['file'] for r in rows}
 for r in q['records']:
  if r['label'].startswith('transition-') and r['file'] not in used:rows.append(r);used.add(r['file'])
out=H/(lane+'-witnesses');out.mkdir(exist_ok=True)
for page in range(math.ceil(len(rows)/20)):
 board=Image.new('RGB',(1200,1060),'#1b272d');d=ImageDraw.Draw(board)
 for i,r in enumerate(rows[page*20:page*20+20]):
  x=i%5*240;y=i//5*265;s=r['screen'];im=Image.open(D/r['file']).convert('RGB')
  if 'crop' not in r:im=im.crop((round(s[0]-6),round(s[1]-6),round(s[0]+s[2]+6),round(s[1]+s[3]+6)))
  scale=min(2,225/im.width,220/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);board.paste(im,(x+(240-im.width)//2,y+39));d.text((x+4,y+4),r['gear']+' / '+r['action']+' / '+r['direction'],fill='white');d.text((x+4,y+19),r['label'][:35],fill='#b8dce2')
 board.save(out/('work-%02d.png'%page))
(H/(lane+'-witness-index.json')).write_text(json.dumps({'nativeCaptures':len(q['records']),'sampled':len(rows),'pages':math.ceil(len(rows)/20),'groups':[list(k) for k in groups]},indent=2));print({'lane':lane,'samples':len(rows),'pages':math.ceil(len(rows)/20)})
