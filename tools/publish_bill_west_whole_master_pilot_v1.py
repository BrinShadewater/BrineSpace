from pathlib import Path
from PIL import Image
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-west-whole-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((D/'keyposes-review.json').read_text());refs=json.loads((D/'references.json').read_text());protected={r['source']:r['sourceSha256'] for r in refs}
for slot in [12,24,36]:
 for r in json.loads((D/f'pose-{slot:03}/references.json').read_text()):protected[r['source']]=r['sourceSha256']
protected['character/bill-water-exit-west-master-v8/sources/master-west-reference.png']=sha(R/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png')
assert all(sha(R/p)==h for p,h in protected.items())
for record in q['records']:
 assert abs(record['heightDelta'])<=2 and record['silhouetteIoU']>.94 and abs(record['wholeShiftY'])<=1
assert q['records'][1]['widthDelta']==0 and q['records'][3]['widthDelta']==-2
rejections=[{'slot':slot,'revision':1,'rawSHA256':sha(D/f'pose-{slot:03}/raw-rejected-v1.png'),'reason':'Closed-foot passing pose changed to wide stride by copying the stride000 supporting pose. Rejected in full, no anatomical fitting.'} for slot in [12,36]]
q.update(protectedInputs=protected,rejections=rejections,visualReviewed=True,findings='Four whole keypose edits improve angular warm face and detailed matte charcoal quilting. Height deltas1/2/1/-1; original whole bottoms exact; wholeY0/-1/0/+1; widths+4/0/+1/-2; silhouettesIoU .942-.967. Passing poses preserve narrow overlapping boots after rejecting wide-stride v1 outputs. Hair/patch/harness detail still varies; four static landmarks do not establish complete48phase material/cadence or rigid boot contact.',nativeRun=False,generationCalls=6,preferredWholePoses=4,normalAdmission=False)
html='''<!doctype html><meta charset="utf-8"><title>Bill — West whole master poses</title><style>body{background:#1f2328;color:#eee;font:18px system-ui;margin:24px auto;max-width:1400px}img.board{width:100%}a{color:#9cdae4}.poses{display:flex;flex-wrap:wrap;gap:20px}.pose img{width:256px;height:256px;background:#26333c}p{line-height:1.4}</style><h1>Bill: West master-style walking poses</h1><p>Four whole stride landmarks now have a clearer angular face and detailed matte suit. The previous pose geometry is retained: unchanged foot baseline, height differences within two source pixels.</p><p>Two wide-stride generations were rejected and replaced by narrow passing poses. This is an uninstalled four-pose study; the full 48-frame loop remains to be completed. Small previews are source exports, not native gameplay captures.</p><p><a href="../bill-installed-coverage-2026-10-04/">Current installed coverage</a> · <a href="keyposes-review.json">Pose review and provenance</a></p><div class="poses">'''
for slot in [0,12,24,36]:html+=f'<div class="pose">Stride {slot:03}<br><img src="candidate-{slot:03}.png" alt="Whole West stride {slot:03}"></div>'
html+='</div><h2>Previous preferred poses and new whole edits</h2><img class="board" src="keyposes-comparison.png"><h2>Original master and first stride</h2><img class="board" src="comparison.png">';(D/'index.html').write_text(html,encoding='utf-8')
names=['prepare_bill_west_whole_master_pilot_v1.py','build_bill_west_whole_master_pilot_v1.py','prepare_bill_west_whole_master_keyposes_v1.py','build_bill_west_whole_master_keyposes_v1.py','publish_bill_west_whole_master_pilot_v1.py']
for name in names:ast.parse((R/'tools'/name).read_text())
pngs=[p.relative_to(R).as_posix() for p in D.rglob('*.png')];r=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(pngs)+'\0').encode(),capture_output=True,check=True,cwd=R);items=r.stdout.decode().split('\0');assert all(items[i+2]=='lfs' for i in range(0,len(items)-1,3))
q.update(pythonSyntax=5,pngLFS=len(pngs));(D/'keyposes-review.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps({'preferredWholePoses':4,'rejectedGenerations':2,'protectedInputs':len(protected),'pngLFS':len(pngs),'pythonSyntax':5,'normalAdmission':False}))
