import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=p/'release-rest-review-v350'
d=json.loads((o/'native-review.json').read_text());v=json.loads((o/'native_probe-validation.json').read_text())
assert d['failures']==0 and d['checks']==497 and len(d['cases'])==16 and v['exitCode']==0 and v['realProfileUnchanged']
assert (o/'native_probe.gd.uid').exists()
paths=[x.relative_to(r).as_posix() for x in o.rglob('*.png')]
a=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(a[i]==b'lfs' for i in range(2,len(a)-1,3))
section='''### James native furniture lifecycle closeout — October 3, 2026

V350 normal James actor/player:497 native checks0,16 habitation/lounge cases across
four actual authored rotations and both gears,112 prescribed pose captures. Actual
room activity entry/update into held rest, actor snapshot restoration, service power
loss and finite exit pass. Physical furniture approach remains fixed. All8native
chronology boards viewed: dedicated East bunk fits lower berth; seated lounge figure
remains visible within registered chair; no obvious cut-off in samples. First station
per room/rotation only; no autonomous arrival, whole-run rest checkpoint or continuous
motion claim. Initial fixture free placement forced rotation0: its duplicate images
and report preserved in first-pass-zero-rotation, excluded from four-layout evidence.
Corrected fixture asserts actual placed rotation. Both runs isolated APPDATA and
owner profile unchanged. PairedUID; all241PNG media including initial evidence LFS.
Browser additionally sampled selected walk/weld and sit-down early/held poses at148px;
source preview alone is not furniture evidence. Accepted artwork/runtime unchanged.
Next: freeze selected release inputs, build and packaged gameplay/Continue smoke;
ordinary autonomous water/hazard visual review remains limited. Known cargo fabric
and North unload stance polish remain. Full goal incomplete; no publication.
Handoff: character/james-west-carry-walk-keys-v1/release-rest-review-v350/HANDOFF.md.
'''
record_guides(r,section,'### James fresh selected bank and native death closeout — October 3, 2026')
review={'version':350,'checks':497,'failures':0,'cases':16,'captures':112,'scope':d['scope'],'visualReview':'Eight corrected native boards viewed; East bunk fits lower berth, registered lounge chair retains visible seated actor. Browser walk/weld and sit-down early/held sampled at148px. No continuous motion claim.','initialSetupCorrection':'Free placement forces rotation0; initial duplicate layout evidence preserved, excluded. Corrected fixture sets and asserts actual room rotation.','mediaLfs':len(paths),'ownerUnchanged':True,'runtimeChanged':False}
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n')
handoff='# Project handoff\n\nUpdated: October 3, 2026 · Project: Brine Space · Task: James rest closeout\n\n## Objective and acceptance\nFinish existing James animations and prepare next release. Full goal incomplete.\n\n## Accepted decisions and constraints\nPreserve accepted artwork, furniture registration and owner saves. No speculative new material generations.\n\n## Current state\n'+section+'\n## Verification\n497 native checks0,16 actual room/rotation/gear cases,112 captures,8 boards viewed. Actor snapshot and power-loss exit pass. Scope limitations in review.json.\n\n## Next action\nFreeze selected runtime inputs and prepare fresh playable build, exact package audit and scratch-profile New Game/Continue smoke.\n'
(o/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=p/'material-repair-progress.json';old=f.read_bytes();ledger=json.loads(old);ledger['releaseNativeRestReview']={'version':350,'checks':497,'cases':16,'captures':112};assert f.read_bytes()==old;f.write_text(json.dumps(ledger,indent=2)+'\n')
f=r/'docs/JAMES_RELEASE_CLOSEOUT.md';old=f.read_bytes();s=old.decode();s=s.replace('Four directions in both gears reviewed as source samples. | Native furniture contact, occlusion and interruption review.','V350 normal James furniture lifecycle:497 checks0,16 actual habitation/lounge layout/gear cases,112 captures; eight boards viewed. Entry, held-rest actor restore and power-loss finite exit pass. | First registered station per layout checked; autonomous arrival and whole-run rest checkpoint not established.')
s=s.replace('V346 reviews all 192 selected source poses across four directions and both gears; exact pixel matches to V333 inventory.','V346 source coverage; V349 actual die() dispatch and normal renderer:419 checks0,16 direction/gear/medium cases,96 captures, eight boards viewed.')
s=s.replace('Existing selected turns and arrival joins are present; incoming workshop heading and finite unloading handoff are integrated.','Selected turns and arrival joins present; V348 North/South turn entry/end samples retain legs and fixed standing scale. Incoming workshop heading and unloading handoff integrated.')
s=s.replace('Confirm consistent height and intact south legs in the final selected playback.','Continuous selected-turn observation remains limited; source/endpoint checks passed.')
s=s.replace('Next action: review the selected full set in motion and close the concrete defects.','Next action: freeze selected release inputs and prepare a fresh playable candidate, exact package audit and scratch-profile gameplay/Continue check. Preserve the remaining review limits above.')
assert f.read_bytes()==old;f.write_text(s)
print(f'V350 recorded:497 checks0,16 cases,112 captures; {len(paths)} LFS images; five guides/checklist/handoffs updated')
