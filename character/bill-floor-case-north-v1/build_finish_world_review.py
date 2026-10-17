from pathlib import Path
import json,hashlib,shutil,math
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-finish-world-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text());assert v['passed'] and d['failures']==0
C=P/'finish-world-captures';C.mkdir(exist_ok=True);hashes={};boards=[]
for event in ['suspension','power']:
 for gear in ['bare','helmet']:
  for phase in [10,32,55]:
   key=f'{event}-{gear}-{phase}';rows=[r for r in d['records'] if r['name'].startswith(key+'-')];assert len(rows)>=3
   board=Image.new('RGB',(200*min(6,len(rows)),240*math.ceil(len(rows)/6)),'#182932');draw=ImageDraw.Draw(board)
   root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
   for i,row in enumerate(rows):
    col=i%6;line=i//6
    for kind in ['room','source']:
     name=row['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name);hashes[name]=hashlib.sha256((C/name).read_bytes()).hexdigest()
    im=Image.open(C/(row['name']+'-room.png')).convert('RGB')
    board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(col*200+10,line*240+30))
    draw.text((col*200+10,line*240+6),row['name'][len(key)+1:],fill='#dde8e9')
    draw.text((col*200+10,line*240+215),'owned='+str(row['caseOwned'])+' exit='+str(row['finishActive']),fill='#dde8e9')
   name=f'{key}-finish-world-review.png';board.save(P/name);boards.append({'case':key,'file':name,'presentations':len(rows)})
html='''<!doctype html><meta charset="utf-8"><title>Bill live ordinary set-down exit</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:900px}figure{overflow:auto;margin:24px 0}img{max-width:none}</style><h1>Bill · staged live service-loss exit</h1><p>Twelve actual workshop exits: suspension and prescribed power loss, both gears, at .10/.32/.55s. Candidate actor/player finishes remaining original North contact/rise. Actual needs continue; cancelled service grants no reward. Root remains planted and floor ownership appears at the inferred release cue.</p><p>Static native samples retain the same physical root. Exact original source/room files retained. This is staged ordinary service-loss evidence, not normal selection, natural chooser, hazards/gear/mortality priority, checkpoint/Continue or continuous-motion acceptance. Terminal stance join still needs polish.</p>'''
for b in boards:html+=f'<h2>{b["case"]}</h2><figure><img src="{b["file"]}"></figure>'
(P/'finish-world-review.html').write_text(html,encoding='utf-8')
(P/'finish-world-review-evidence.json').write_text(json.dumps({'validation':v,'checks':d['checks'],'boards':boards,'captureHashes':hashes,'scope':d['scope']},indent=2)+'\n')
print(f'{len(boards)}native boards/{len(d["records"])}presentations/{len(hashes)}unchanged original captures retained.')
