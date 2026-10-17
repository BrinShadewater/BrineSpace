"""Verify family consolidation; native/world installation is a separate gate."""
from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
for file,expected in json.loads((P/'source-bindings.json').read_text(encoding='utf-8')).items():
 check(hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==expected,'family source binding '+file)
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 check(m['pivot']==[128,128] and m['standingHeight']==148 and m['frameWidth']==256,'family plane')
 check(len(m['states'])==4,'four cardinal states')
 check({s['id'] for s in m['states']}=={'death-water-'+d for d in ['east','west','north','south']},'cardinal coverage')
 for s in m['states']:
  check(len(s['frameFiles'])==6 and not s['loop'] and s['frameDurationsMs']==[180,180,220,220,260,500],'one-shot clock')
  for file in s['frameFiles']:
   check(file.startswith('res://character/') and Image.open(ROOT/file.removeprefix('res://')).size==(256,256),'literal existing frame')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'gearStates':8,'frameRefs':48,'scope':'source-bound cardinal consolidation;directional native candidates separately validated;not runtime installation or mortality/restore proof'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} cardinal death consolidation checks PASS')
