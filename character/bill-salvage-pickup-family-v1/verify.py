"""Verify the aggregate, directional authorities and exact work/cargo handoffs."""
from pathlib import Path
import hashlib,json
from PIL import Image
P=Path(__file__).resolve().parent
checks=0
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
def pixels(path):return Image.open(path).convert('RGBA').tobytes()
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 h=json.loads((P/f'{gear}-hashes.json').read_text(encoding='utf-8'))
 check(m['pivot']==[128,128] and m['standingHeight']==148,'registration')
 check(m['textureFilter']=='linear' and m['precomposed'],'render contract')
 check(len(m['states'])==8,'eight states')
 check({s['id'] for s in m['states']}=={f'{a}-{d}' for a in ['salvage','swim-pickup'] for d in ['east','west','north','south']},'complete directional coverage')
 for authority in json.loads((P/f'{gear}-inputs.json').read_text(encoding='utf-8')):
  check(hashlib.sha256((P.parent/authority['folder']/'manifest.json').read_bytes()).hexdigest()==authority['manifestSha256'],'input manifest unchanged')
 for s in m['states']:
  direction=s['id'].rsplit('-',1)[1];work=s['id'].startswith('salvage-')
  check(len(s['frameFiles'])==6,'six frames')
  check(s['frameDurationsMs']==([140]*6 if work else [70,80,90,100,100,80]),'authored clock')
  check(s['loop']==work,'finite pickup / looping work')
  check(s['facings']==[direction]*6 and s['waterPoses']==[True]*6,'water orientation')
  for f in s['frameFiles']:
   check(Image.open(P/f).size==(256,256),'full registration plane')
   check(hashlib.sha256((P/f).read_bytes()).hexdigest()==h[f],'bound frame hash')
  if work:check(pixels(P/s['frameFiles'][0])==pixels(P/s['frameFiles'][-1]),'closed work loop')
  else:
   ws=next(r for r in m['states'] if r['id']=='salvage-'+direction)
   check(pixels(P/s['frameFiles'][0])==pixels(P/ws['frameFiles'][0]),'exact work join')
   folder=f'bill-swim-carry-{direction}-coherent-v1' if gear=='bare' else f'bill-swim-carry-helmet-{direction}-coherent-v1'
   target=Image.new('RGBA',(256,256));target.alpha_composite(Image.open(P.parent/folder/'frames'/f'swim-carry-{direction}'/'000.png').convert('RGBA'),{'east':(6,40),'west':(42,40),'north':(24,56),'south':(24,-24)}[direction])
   check(pixels(P/s['frameFiles'][-1])==target.tobytes(),'exact selected cargo join')
report={'passed':True,'checks':checks,'scope':'aggregate completeness, clocks, retained authority hashes and pixel-exact work/cargo joins; native playback validated separately'}
(P/'verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
