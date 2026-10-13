"""Publish family renderer evidence and remaining visual mismatch."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-family-review-v1';O=R/'output/bill-east-family-native-v2';N=D/'native';N.mkdir(exist_ok=True)
v=json.loads((O/'validation.json').read_text());report=json.loads((O/'report.json').read_text());review=json.loads((D/'review.json').read_text())
assert v['passed'] and v['checks']==374 and v['captures']==50 and len(report['slots'])==175
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/p)==h for p,h in review['protectedInputs'].items())
for name in ['validation.json','report.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,N/name)
for c in report['captures']:
 for name in [c['worldFile'],c['sourceFile']]:shutil.copy2(O/name,N/name)
pages=[]
for key in review['sources']:
 board=Image.new('RGBA',(1010,585),'#17252d');draw=ImageDraw.Draw(board)
 entries=[c for c in report['captures'] if c['label'].startswith(key+' / ')]
 assert len(entries)==5
 for i,c in enumerate(entries):
  im=Image.open(O/c['worldFile']).convert('RGBA').crop((315,155,820,310))
  x=(i%2)*505;y=(i//2)*195
  board.alpha_composite(im,(x,y+30));draw.text((x+8,y+8),c['label'],fill='white')
 name=key+'-comparison.png';board.save(N/name);pages.append(name)
html=(D/'index.html').read_text(encoding='utf-8')
html=html.replace('</html>',f'<h2>Same room renderer</h2><p>374 checks passed across all175 source slots and50 room/source capture pairs. Sources and {v["ownerNonLogCount"]:,} saved-profile files were unchanged. These are prescribed stationary comparisons, not autonomous job transitions.</p>'+''.join(f'<img src="native/{p}" alt="Native {p.removesuffix("-comparison.png")}">' for p in pages)+'</html>')
finding='The repaired six-bank family is substantially closer in matte material and identity at a common scale. Run leans and carry changes gait naturally; small pose/head/hair/insignia changes remain provisional. Existing pickup/unload and torch draw/stow remain darker and less detailed, creating material discontinuities at the repaired carry/weld boundaries. No normal admission or owner acceptance. Native comparisons select sources explicitly; they do not certify real tool/cargo handoff controllers or physical movement.'
html=html.replace('<button id="speed">','<p><strong>Remaining repair:</strong> Existing pickup, unload and torch draw/stow are darker and less detailed than the repaired family. Match these short handoffs before normal admission.</p><button id="speed">')
(D/'index.html').write_text(html,encoding='utf-8')
review.update(nativeTested=True,nativeValidation=v,nativeScope=report['scope'],findings=finding,remainingMasterRepairs=['pickup-east','unload-east','torch-draw-east','torch-stow-east'],failedNativeV1='374checks/13failures caused by fixture truncating multiword action names to torch. V2 keeps torch-draw/torch-stow intact; unchanged artwork. Both tests scratchAPPDATA and owner inputs stable.')
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
print(json.dumps(dict(checks=374,sourceSlots=175,captures=50,pages=len(pages),remainingMasterRepairs=4)))
