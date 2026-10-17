from pathlib import Path
import json,math
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'actor-return-v9-evidence.json').read_bytes())
cases=[x for x in data['results'] if not x.get('diagnostic')]
boards=[]
for case in cases:
 trace=case['trace'];cols=min(6,max(1,len(trace)));rows=math.ceil(len(trace)/cols)
 board=Image.new('RGB',(cols*320,rows*500),'#303b40');draw=ImageDraw.Draw(board)
 for i,pose in enumerate(trace):
  x=(i%cols)*320;y=(i//cols)*500
  draw.text((x+5,y+4),f"{case['mode']} {pose['key']} / {pose['index']}",fill='white')
  source=Image.open(r/pose['source'].removeprefix('res://')).convert('RGBA')
  board.paste(source,(x+32,y+24),source)
  world=Image.open(r/pose['world'].removeprefix('res://')).convert('RGB');world.thumbnail((300,210),Image.Resampling.NEAREST)
  board.paste(world,(x+(320-world.width)//2,y+282))
 file=f"actual-v9-return-{case['mode']}-{case['target']}-review.png";board.save(p/file)
 boards.append({'mode':case['mode'],'stage':case['target'],'poses':len(trace),'file':file})
(p/'actor-return-v9-review.json').write_text(json.dumps({'boards':boards,'visualReviewPending':True,'selected':False,'scope':'All46native changing-pose source/world pairs through six prescribed actual power-loss returns. Main otherwise paused, actor stepped; static native captures, not continuous world movie.'},indent=2)+'\n')
print(f'{len(boards)}native source/room boards; {sum(x["poses"] for x in boards)}poses.')
