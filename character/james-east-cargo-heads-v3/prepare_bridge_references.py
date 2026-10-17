from pathlib import Path
import json,re,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-cargo-return-bridges-v1';out.mkdir(exist_ok=True)
branch=(r/'scripts/grid_canvas.gd').read_text().split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0]
banks={'bare':{},'helmet':{}};profiles={'bare':{},'helmet':{}}
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"',branch):
 path=r/rel;pack=json.loads(path.read_bytes());mode='bare' if kind=='load_manifest' else 'helmet'
 for state in pack['states']:
  if not state.get('frameFiles'):continue
  banks[mode][state['id']]=[(path.parent/f).resolve() for f in state['frameFiles']]
  profiles[mode][state['id']]=(pack.get('pivot',[46,86]),pack.get('standingHeight',74))
board=Image.new('RGBA',(768,512),(0,0,0,0));rows=[]
for y,mode in enumerate(('bare','helmet')):
 for x,(key,index) in enumerate((('carry-turn-east-west',-1),('unload-west',0),('idle-west',0))):
  path=banks[mode][key][index];im=Image.open(path).convert('RGBA');pivot,height=profiles[mode][key];assert height==148
  board.alpha_composite(im,(x*256+128-int(pivot[0]),y*256+224-int(pivot[1])))
  rows.append({'mode':mode,'key':key,'index':len(banks[mode][key])-1 if index<0 else index,'path':path.relative_to(r).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pivot':pivot,'standingHeight':height})
board.save(out/'west-bridge-reference.png')
(out/'reference-evidence.json').write_text(json.dumps({'sources':rows,'grid':'3columns x2rows; bare then helmet; held turn endpoint, unload start, selected idle; aligned pivot128224/H148','selected':False},indent=2)+'\n')
print('Paired West bridge references prepared with exact source hashes.')
