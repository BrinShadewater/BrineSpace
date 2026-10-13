"""Correct proven sole offsets by lossless whole-frame translation only."""
from pathlib import Path
import json, hashlib, shutil
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'character/marsh-east-walk-family-detail-v1'
OUT=ROOT/'character/marsh-east-walk-family-contact-v1'
RUN=ROOT/'output/marsh-animation-audit/east-walk-world-v2-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((RUN/'report.json').read_text())
assert r['checks']==1653 and r['failures']==70 and len(r['captures'])==43
failures=[l for l in (RUN/'engine.log').read_text().splitlines() if l.startswith('ERROR:')]
assert failures.count('ERROR: candidate preserves normal source sole depth at same actor root')==69
assert failures.count('ERROR: actual finite route arrives once')==1
assert len(failures)==70
assert {s['slot'] for s in r['samples'] if s['depthDifference']}=={0,2}
a=json.loads((RUN/'inputs-before.json').read_text());b=json.loads((RUN/'inputs-after.json').read_text())
changes=[p for p in a if a[p]!=b[p]]
assert changes==['scripts/james_cargo_player.gd'],changes
assert json.loads((RUN/'owner-before.json').read_text())==json.loads((RUN/'owner-after.json').read_text())
OUT.mkdir(exist_ok=True)
records=[]
for slot in range(6):
 old=SOURCE/f'{slot:03}.png';new=OUT/f'{slot:03}.png'
 im=Image.open(old).convert('RGBA');arr=np.asarray(im)
 if slot in [0,2]:
  assert np.all(arr[-1,:,3]==0),'visible outgoing bottom row'
  translated=np.zeros_like(arr);translated[1:]=arr[:-1]
  assert np.array_equal(translated[1:],arr[:-1])
  assert np.count_nonzero(translated[:,:,3])==np.count_nonzero(arr[:,:,3])
  Image.fromarray(translated).save(new)
 else:shutil.copyfile(old,new)
 records.append({'slot':slot,'beforePath':old.relative_to(ROOT).as_posix(),'beforeSha256':sha(old),'path':new.relative_to(ROOT).as_posix(),'sha256':sha(new),'translation':[0,1] if slot in [0,2] else [0,0],'method':'Exact full RGBA Y+1, transparent outgoing row/no visible clipping' if slot in [0,2] else 'Exact byte copy'})
manifest=json.loads((SOURCE/'manifest.json').read_text())
manifest['states'][0]['frameFiles']=['res://'+(OUT/f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
receipt={'records':records,'failedRunReportSha256':sha(RUN/'report.json'),'failedRunChanges':changes,'otherFailedIntervalInputsExact':len(a)-len(changes),'ownerNonLogStable':2931,'normalAdmission':False,'scope':'Staged six-phase bank; only whole-frame registration of proven source sole offsets0/2. Native V2 mixed canvas-position/source scale contact coordinate is corrected in subsequent probe; same-source1pixel disparity still established. V2 exact-arrival assertion exceeded normal approximate arrival contract. No gameplay/controller change.'}
(OUT/'registration.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Staged family registered:two complete RGBA drawings Y+1/no clipping;four exact byte copies;all metadata preserved')
