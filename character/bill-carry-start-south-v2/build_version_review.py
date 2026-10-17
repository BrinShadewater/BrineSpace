"""Retain native Continue captures unchanged; build separate labelled review boards."""
from pathlib import Path
import json, shutil, html
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
O=P.parents[1]/'output/bill-carry-south-version-continue-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'))
v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and d['failures']==0 and len(d['records'])==12
(P/'version-captures').mkdir(exist_ok=True)
cards=[]
for gear in [False,True]:
 records=sorted([r for r in d['records'] if r['helmet']==gear],key=lambda r:(r['phase'],r['name']))
 board=Image.new('RGB',(840,660),'#182932');draw=ImageDraw.Draw(board)
 for i,r in enumerate(records):
  x=255+(r['foot'][0]-7680)*398/384
  y=287+(r['foot'][1]-8064)*398/384
  tag=r['name'];frames=[];bx=(i%2)*420;by=(i//2)*220
  draw.text((bx+10,by+8),tag,fill='#dde8e9')
  for j,stage in enumerate(['before','after']):
   for kind in ['room','source']:
    name=f'{tag}-{stage}-{kind}.png'
    shutil.copy2(O/name,P/'version-captures'/name)
   im=Image.open(O/f'{tag}-{stage}-room.png').convert('RGB')
   crop=im.crop((round(x-90),round(y-145),round(x+90),round(y+35)))
   board.paste(crop,(bx+10+j*200,by+35))
   draw.text((bx+10+j*200,by+23),stage,fill='#dde8e9')
   url=f'version-captures/{tag}-{stage}-room.png'
   frames.append(f'<div><p>{stage}</p><div class="crop"><img src="{url}" style="left:{90-x:.3f}px;top:{145-y:.3f}px"></div></div>')
  cards.append(f'<section><h2>{html.escape(tag)}</h2><div class="pair">'+''.join(frames)+'</div></section>')
 board.save(P/f'version-continue-{"helmet" if gear else "bare"}-review.png')
page='''<!doctype html><meta charset="utf-8"><title>Bill South Continue review</title>
<style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(390px,420px));gap:16px}section{background:#22343e;padding:12px}h2{font-size:15px}.pair{display:flex;gap:15px}.crop{position:relative;width:180px;height:180px;overflow:hidden}.crop img{position:absolute;width:1280px;max-width:none;height:900px}a{color:#adcddd}</style>
<h1>Bill South carrying · fresh Continue</h1><p>Three retained source versions, both equipment variants, first step and arrival. Unmodified native captures before and after ordinary disk/fresh-main restoration. Real workshop service with a prescribed clear South lane; natural routes and continuous contact review remain separate.</p><p><a href="./">South motion preview</a></p><main>CARDS</main>'''
(P/'version-continue.html').write_text(page.replace('CARDS',''.join(cards)),encoding='utf-8')
print('Retained 48 original captures; built 12 comparison cards and two review boards.')
