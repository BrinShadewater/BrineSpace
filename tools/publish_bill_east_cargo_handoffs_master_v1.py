"""Publish complete cargo slot evidence without claiming autonomous gameplay."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,math
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-cargo-handoffs-master-v1';O=R/'output/bill-east-cargo-handoffs-native-v1';N=D/'native';N.mkdir(exist_ok=True)
q=json.loads((D/'review.json').read_text());v=json.loads((O/'validation.json').read_text());report=json.loads((O/'report.json').read_text());assert v['passed'] and v['captures']==27 and len(report['slots'])==25
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in report['captures']:
 for name in [c['worldFile'],c['sourceFile']]:shutil.copy2(O/name,N/name)
pages=[]
for key in q['sources']:
 entries=[c for c in report['captures'] if c['label'].startswith(key+' / ')]
 for page in range(math.ceil(len(entries)/6)):
  chosen=entries[page*6:page*6+6];board=Image.new('RGBA',(1010,585),'#17252d');draw=ImageDraw.Draw(board)
  for i,c in enumerate(chosen):
   x=i%2*505;y=i//2*195;board.alpha_composite(Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310)),(x,y+30));draw.text((x+8,y+8),c['label'],fill='white')
  name=f'{key}-{page+1}-comparison.png';board.save(N/name);pages.append(name)
board=Image.new('RGBA',(1010,195),'#17252d');draw=ImageDraw.Draw(board)
for i,c in enumerate([report['captures'][0],report['captures'][-1]]):
 board.alpha_composite(Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310)),(i*505,30));draw.text((i*505+8,8),c['label'],fill='white')
board.save(N/'idle-boundaries.png');pages.append('idle-boundaries.png')
html=(D/'index.html').read_text(encoding='utf-8');html=html.replace('</html>',f'<h2>In-room source and action clock</h2><p>{v["checks"]} checks passed:25source slots and27room/source pairs. Production workshop unload action clock tested. {v["ownerNonLogCount"]:,} saved-profile files and all frozen inputs unchanged. Stationary source review; actual cargo jobs and moving routes still to verify.</p>'+''.join(f'<img src="native/{p}" alt="Native {p}">' for p in pages)+'</html>');(D/'index.html').write_text(html,encoding='utf-8')
q.update(nativeTested=True,nativeValidation=v,nativeScope=report['scope'],remainingEastMasterHandoffs=[],findings='Matte quilting and warm face substantially closer to current idle/carry. Original action depths, contact and clocks retained; identical source endpoints share exact repaired whole pixels. Minor hair/head/patch and case-latch/metal variation remain provisional. Source bounds and renderer checks do not prove named-hand/boot pressure or rigid case geometry. Six initial geometry mismatches rejected and preserved. No normal admission or owner acceptance; actual cargo dispatch/ownership/moving contact/completion/gear/save still untested.')
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(dict(checks=v['checks'],sourceSlots=25,captures=27,nativePages=len(pages))))
