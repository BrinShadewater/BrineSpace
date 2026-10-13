"""Make review boards from unaltered retained captures; no sprite edits."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil
R=Path(__file__).resolve().parents[1];O=R/'output/bill-actual-jobs-v3';D=R/'character/bill-actual-jobs-v1';D.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text());q=json.loads((O/'report.json').read_text());assert v['passed'] and v['checks']==2978
for name in ['report.json','validation.json']:shutil.copy2(O/name,D/name)
pages=[]
for start in range(0,len(q['captures']),6):
 board=Image.new('RGBA',(1200,780),'#17252d');draw=ImageDraw.Draw(board)
 for i,c in enumerate(q['captures'][start:start+6]):
  x=i%2*600;y=i//2*260
  # Full station frame shown at half size, with separate original source at 1x.
  world=Image.open(O/c['worldFile']).convert('RGBA');world.thumbnail((400,225))
  board.alpha_composite(world,(x,y+30))
  sprite=Image.open(O/c['sourceFile']).convert('RGBA')
  if sprite.size==(184,184):
   padded=Image.new('RGBA',(256,256));padded.alpha_composite(sprite,(36,52));sprite=padded
  assert sprite.size==(256,256)
  sprite.thumbnail((184,184))
  board.alpha_composite(sprite,(x+410,y+40))
  draw.text((x+6,y+8),c['label'],fill='white')
 name=f'review-{start//6+1}.png';board.save(D/name);pages.append(name)
html='''<!doctype html><meta charset="utf-8"><title>Bill — actual jobs</title><style>body{margin:24px auto;max-width:1200px;background:#14212a;color:#e4edf2;font:17px system-ui}img{width:100%;margin:12px 0}a{color:#aacfe4}</style><h1>Bill: actual construction and cargo jobs</h1><p>Paid construction completed with all six draw, weld and stow poses. Real workshop service completed pickup, generated carrying route and unloading. All eleven repaired East pickup poses displayed.</p><p>2,978 checks passed. Repaired East art staged for this review; other directions and carrying transitions retain the current selection. The normal game selection has not changed.</p><p>Each card shows the actual station capture and submitted sprite. These are sampled handoffs, not a continuous animation recording.</p>'''
html+=''.join(f'<img src="{name}" alt="Actual job handoffs {i+1}">' for i,name in enumerate(pages))
(D/'index.html').write_text(html,encoding='utf-8')
(D/'review.json').write_text(json.dumps({'native':v,'scope':q['scope'],'pages':pages,'visualReviewed':False,'normalAdmission':False},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':v['checks'],'captures':len(q['captures']),'pages':pages}))
