"""Publish successful prescribed-phase evidence after the input freeze completes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil
R=Path(__file__).resolve().parents[1];O=R/'output/bill-east-run-master-native-v2';D=R/'character/bill-east-run-master-v1';N=D/'native';N.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));report=json.loads((O/'report.json').read_text(encoding='utf-8'))
assert v['passed'] and v['checks']==75 and v['captures']==16 and not v['inputChanges'] and not v['ownerChanges']
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in report['captures']:
 for name in [c['worldFile'],c['sourceFile']]:shutil.copy2(O/name,N/name)
pages=[]
for page in range(4):
 slots=[page*2,page*2+1] if page<3 else ['idle before','idle after']
 board=Image.new('RGBA',(1010,390),'#17252d');draw=ImageDraw.Draw(board)
 for row,slot in enumerate(slots):
  label=f'run pose {slot}' if isinstance(slot,int) else slot
  for col,variant in enumerate(['selected','candidate']):
   c=next(c for c in report['captures'] if c['label']==label and c['variant']==variant)
   im=Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310))
   board.alpha_composite(im,(col*505,row*195+30));draw.text((col*505+8,row*195+8),f'{variant} / {label}',fill='white')
 name=f'comparison-{page}.png';board.save(N/name);pages.append(name)
html=(D/'index.html').read_text(encoding='utf-8')
html=html.replace('.row{display:flex;gap:16px;flex-wrap:wrap}', '.row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}')
html=html.replace('.sprite{width:384px;height:384px;image-rendering:auto}', '.sprite{width:100%;height:auto;image-rendering:auto}')
html=html.replace('</html>','<h2>Actual room renderer</h2><p>75 checks passed. All six poses and the loop wrap were verified through the retained renderer, with the same master idle before and after. All tested inputs and 2,931 saved-profile files were unchanged. These are prescribed stationary source phases, not a physical running route.</p>'+''.join(f'<img src="native/{name}" alt="Native running comparison {i+1}">' for i,name in enumerate(pages))+'</html>')
(D/'index.html').write_text(html,encoding='utf-8')
review=json.loads((D/'review.json').read_text(encoding='utf-8'));review.update(nativeTested=True,nativeScope=report['scope'],nativeValidation=v)
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=v['checks'],captures=v['captures'],inputs=v['inputCount'],ownerFiles=v['ownerNonLogCount'],comparisonPages=4)))
