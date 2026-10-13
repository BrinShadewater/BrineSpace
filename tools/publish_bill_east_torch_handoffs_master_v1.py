"""Publish isolated production-clock and retained renderer evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-handoffs-master-v1';O=R/'output/bill-east-torch-handoffs-native-v1';N=D/'native';N.mkdir(exist_ok=True)
q=json.loads((D/'review.json').read_text());v=json.loads((O/'validation.json').read_text());report=json.loads((O/'report.json').read_text())
assert v['passed'] and v['captures']==25 and len(report['slots'])==18 and len(report['boundaries'])==5
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/p)==h for p,h in q['protectedInputs'].items())
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in report['captures']:
 for name in [c['worldFile'],c['sourceFile']]:shutil.copy2(O/name,N/name)
pages=[]
for key in q['sources']:
 entries=[c for c in report['captures'] if c['label'].startswith(key+' / ')]
 assert len(entries)==6
 board=Image.new('RGBA',(1010,585),'#17252d');draw=ImageDraw.Draw(board)
 for i,c in enumerate(entries):
  x=i%2*505;y=i//2*195;board.alpha_composite(Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310)),(x,y+30));draw.text((x+8,y+8),c['label'],fill='white')
 name=key+'-comparison.png';board.save(N/name);pages.append(name)
entries=[report['captures'][0]]+[c for c in report['captures'] if c['variant']=='boundary']+[report['captures'][-1]]
board=Image.new('RGBA',(1010,780),'#17252d');draw=ImageDraw.Draw(board)
for i,c in enumerate(entries):
 x=i%2*505;y=i//2*195;board.alpha_composite(Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310)),(x,y+30));draw.text((x+8,y+8),c['label']+' / '+c['key'],fill='white')
board.save(N/'boundaries.png');pages.append('boundaries.png')
html=(D/'index.html').read_text();html=html.replace('</html>',f'<h2>Production timer and room rendering</h2><p>{v["checks"]} checks passed:18source slots, five draw/weld/stow timer boundaries and25room/source pairs. Scratch profile and {v["ownerNonLogCount"]:,} original saved-profile files unchanged. Stationary prescribed construction timers; autonomous completion remains untested.</p>'+''.join(f'<img src="native/{p}" alt="Native {p}">' for p in pages)+'</html>');(D/'index.html').write_text(html)
q.update(nativeTested=True,nativeValidation=v,nativeScope=report['scope'],remainingMasterRepairs=['pickup-east','unload-east'],findings='Eight rebuilt intermediate poses retain connected near-arm sleeves, matte quilting and warm face, substantially closer to current idle/weld. Small head/hair/patch and tool hardware variation remain provisional. Exact four whole endpoints and selected520ms timing/contact preserved. Stationary production animation/action-clock boundaries checked; autonomous job/tool ownership, gear/save and normal admission untested.')
(D/'review.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(dict(checks=v['checks'],sourceSlots=18,boundaries=5,captures=25,nativePages=4)))
