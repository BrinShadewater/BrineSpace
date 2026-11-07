"""Preserve scoped dispatch results and show selected activity boundaries."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output/bill-walk-join-context-native-v1';D=R/'character/bill-east-walk-joins-v1/context-review-v1'
report=json.loads((O/'report.json').read_text(encoding='utf-8'));validation=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert validation['engineExit']==0 and report['checks']==82 and report['failures']==0 and len(report['contexts'])==9 and not validation['ownerChanges']
assert all(c['sourceMatchesBaseline'] and c['returnMatchesIdle'] for c in report['contexts'])
before=json.loads((O/'inputs-before.json').read_text(encoding='utf-8'));after=json.loads((O/'inputs-after.json').read_text(encoding='utf-8'))
changed=[p for p in before if before[p]!=after.get(p)];added=sorted(set(after)-set(before))
assert changed==[str(R/'scripts/main.gd')]
assert set(added)=={str(D/'family-comparison.png'),str(D/'family-review.json')}
assert all(before[str(R/p)]==after[str(R/p)] for p in ['scripts/grid_canvas.gd','tools/bill_east_walk_join_candidate_v1.gd'])
scope=dict(dispatchChecksPassed=True,checks=82,contexts=9,captures=len(report['captures']),ownerNonLogCount=validation['ownerNonLogCount'],ownerChanges=[],fullProjectFreezePassed=False,concurrentChangedFiles=changed,reviewOnlyAddedFiles=added,seconds=validation['seconds'],normalAdmission=False,limitations='Prescribed actual getter dispatch and retained room captures only. Not natural gear/water/death activity transitions or full loops. Main script changed concurrently; full-project freeze failed. The runner did not include its new fixture in the broad input map; exact current fixture is copied separately, no before/after freeze claimed for it.')
for name in ['report.json','validation.json','inputs-before.json','inputs-after.json']:shutil.copy2(O/name,D/name)
for c in report['captures']:
 for name in [c['worldFile'],c['sourceFile']]:shutil.copy2(O/name,D/name)
board=Image.new('RGBA',(1010,600),(23,37,45,255));draw=ImageDraw.Draw(board)
for row,state in enumerate(['run','carry','weld']):
 for col,label in enumerate([state,'idle after '+state]):
  capture=next(c for c in report['captures'] if c['label']==label)
  im=Image.open(O/capture['worldFile']).convert('RGBA').crop((315,155,820,310))
  board.alpha_composite(im,(col*505,row*200+30));draw.text((col*505+10,row*200+8),label,fill='white')
board.save(D/'native-boundaries.png')
for name in ['review_bill_walk_join_context_native_v1.gd','review_bill_walk_join_context_native_v1.gd.uid','run_bill_walk_join_context_native_v1.py']:
 shutil.copy2(R/'tools'/name,D/(name+'.txt'))
(D/'dispatch-review.json').write_text(json.dumps(scope,indent=2)+'\n',encoding='utf-8')
html='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Bill activity boundary review</title><style>body{background:#17252d;color:#dbe5e9;font:16px system-ui;margin:28px auto;max-width:1280px}img{display:block;max-width:100%;height:auto;margin:22px 0}a{color:#82d3df}p{max-width:950px;line-height:1.5}</style><h1>Bill: walking and activity boundaries</h1><p>The walking transition now clears when Bill changes activity or equipment. All 82 targeted room checks passed across nine prescribed contexts. The 2,931 saved-profile files were unchanged. A concurrent main-script change prevented a clean whole-project freeze.</p><p>Running, carrying and torch work still appear darker and coarser than the current master idle, walk and reach. These samples identify the remaining matching work; they do not certify full animation loops. The normal game selection is unchanged.</p><p><a href="../native-motion-v2/">Watch the walking joins</a></p><h2>Same-scale source comparison</h2><img src="family-comparison.png" alt="Current idle walk settling reach versus selected run carry weld"><h2>Actual room renderer: activity and return to idle</h2><img src="native-boundaries.png" alt="Native room captures of run carry and weld and return to idle"></html>'''
(D/'index.html').write_text(html,encoding='utf-8')
print(json.dumps(scope))
