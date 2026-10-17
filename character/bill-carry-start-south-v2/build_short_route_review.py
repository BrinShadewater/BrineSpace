"""Show unchanged native source/room captures at registered scale."""
from pathlib import Path
import json,shutil,html
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-carry-short-route-audit-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and d['failures']==0 and len(d['records'])==8
C=P/'short-route-captures';C.mkdir(exist_ok=True);cards=[];fallback=[]
archive=sorted(O.glob('interval-before-*'))[-1]
prior=json.loads((archive/'records.json').read_text(encoding='utf-8'))
old_samples={s['name']:s for r in prior['records'] if r['rotation']==0 for s in r['samples']}
for r in d['records']:
 samples=r['samples'];board=Image.new('RGB',(len(samples)*210,260),'#182932');draw=ImageDraw.Draw(board)
 for i,s in enumerate(samples):
  name=s['name'];x=255+(s['foot'][0]-7680)*398/384;y=287+(s['foot'][1]-8064)*398/384
  origin=O
  if not all((O/f'{name}-{kind}.png').exists() for kind in ['room','source']):
   assert r['rotation']==0 and name in old_samples
   old=old_samples[name]
   assert all(s[k]==old[k] for k in ['phase','direction','foot','state','key','entry','stowActive']),name
   origin=archive;fallback.append({'name':name,'interval':archive.name,'guard':'phase/direction/foot/state/key/entry/stow match corrected run; actual rotation0 in both intervals'})
  for kind in ['room','source']:shutil.copy2(origin/f'{name}-{kind}.png',C/f'{name}-{kind}.png')
  im=Image.open(origin/f'{name}-room.png').convert('RGB');board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(i*210+10,40))
  draw.text((i*210+10,10),s['phase']+' / '+s['direction'],fill='#dde8e9')
  draw.text((i*210+10,24),f"{s['time']:.3f}s",fill='#dde8e9')
  src=Image.open(origin/f'{name}-source.png').convert('RGBA')
  # Ordinary standing184/p92,172 and cargo256/p128,224 use one148 ruler.
  pivot=(92,172) if src.width==184 else (128,224)
  src.thumbnail((src.width//2,src.height//2),Image.Resampling.LANCZOS)
  board.paste(src,(i*210+145-pivot[0]//2,245-pivot[1]//2),src)
 board.save(P/f"short-route-{r['name']}-review.png")
 cards.append(f'<section><h2>{html.escape(r["name"])}</h2><p>Generated path {r["pathDistance"]:.2f} world units; actual travel {r["actualTravel"]:.2f}.</p><img src="short-route-{r["name"]}-review.png"></section>')
page='''<!doctype html><meta charset="utf-8"><title>Bill workshop short routes</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:20px}section{margin:20px 0;overflow:auto}img{max-width:none}a{color:#adcddd}</style><h1>Bill · workshop-generated cargo routes</h1><p>Four workshop rotations, both equipment variants. Actual generated paths from prescribed service dispatch; normal selected animation sources. Native room crops and registered half-size source thumbnails. Static samples do not establish full contact or continuous motion acceptance.</p><a href="./">South motion preview</a>CARDS'''
(P/'short-route-review.html').write_text(page.replace('CARDS',''.join(cards)),encoding='utf-8')
(P/'short-route-capture-provenance.json').write_text(json.dumps({'retainedEarlierRotationZeroCaptures':fallback,'note':'Seven rotation-zero bare pairs use earlier native actual rotation-zero captures after stale cleanup lost six pairs and one source file. Exact phase/root/state/entry comparison guards reuse. Other route captures from corrected run. No continuous film claim.'},indent=2)+'\n',encoding='utf-8')
print('Eight native route boards retained:',sum(len(r['samples']) for r in d['records']),'source/room pairs')
