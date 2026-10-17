from pathlib import Path
import re,json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2';catalog=json.loads((base/'catalog.json').read_text());selected={m:{} for m in ['bare','helmet']}
def register(file,mode):
 m=json.loads(file.read_text())
 for s in m['states']:selected[mode][s['id']]=(file.parent/s['frameFiles'][0],m)
for mode,group in [('bare','body'),('helmet','equipment')]:
 for rel in catalog[group]:register(base/rel,mode)
source=(R/'scripts/grid_canvas.gd').read_text();a=source.index('elif actor == "branforth":');b=source.index('\nfunc ',a)
for kind,path in re.findall(r'player\.(load_manifest|load_equipment_manifest)\((?:"diving-helmet", )?"res://([^"]+)"',source[a:b]):register(R/path,'bare' if kind=='load_manifest' else 'helmet')
records={}
for mode in ['bare','helmet']:
 for d in ['east','south','west','north']:
  for action in ['idle','swim']:
   file,m=selected[mode][action+'-'+d];im=Image.open(file).convert('RGBA');pos=[round(128-m['pivot'][0]),round(224-m['pivot'][1])];out=Image.new('RGBA',(256,360));out.alpha_composite(im,tuple(pos));dest=P/'endpoints'/mode/(action+'-'+d+'.png');dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest)
   records[mode+'-'+action+'-'+d]=dict(source=file.relative_to(R).as_posix(),sourceSha256=hashlib.sha256(file.read_bytes()).hexdigest(),pivot=m['pivot'],translation=pos,registered=dest.relative_to(P).as_posix())
(P/'endpoint-sources.json').write_text(json.dumps(records,indent=2)+'\n');print('Registered16 exact currently selected idle/swim endpoints into256x360,p128224')
