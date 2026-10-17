import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';m=p/'release-motion-review-v348';d=p/'release-death-review-v349'
inv=json.loads((m/'selected-inventory.json').read_text());native=json.loads((d/'native-review.json').read_text())
for folder,name in [(m,'inventory_probe'),(d,'native_probe')]:
    v=json.loads((folder/(name+'-validation.json')).read_text());assert v['exitCode']==0 and v['realProfileUnchanged'];assert (folder/(name+'.gd.uid')).exists()
assert inv['failures']==native['failures']==0
paths=[x.relative_to(r).as_posix() for folder in [m,d] for x in folder.glob('*.png')]
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
review={'version':349,'normalArtworkChanged':False,'nativeChecks':419,'cases':16,'captures':96,'scope':native['scope'],'visualReview':'All eight native chronology boards viewed: dry poses visible beside furnishings without obvious cut-off; wet lighting obscures fine materials. Browser sampled idle, north/south turn entry/endpoints, diagnostics early/later, repair, unloading middle/end and cargo at 82/148px. Loading screens excluded; preview loading race repaired. Not continuous observation of every group or pose.','protectedOriginalSlots':8058,'availablePlaybackGroups':22,'mediaLfs':len(paths),'ownerUnchanged':True,'remaining':'Walk/weld/rest and furniture/lifecycle review; recovery/distress natural triggers and ordinary exterior playback; final build and packaged gameplay/Continue. Coarse cargo quilt and north unloading stance remain polish concerns.'}
(d/'review.json').write_text(json.dumps(review,indent=2)+'\n')
section='''### James fresh selected bank and native death closeout — October 3, 2026

V348 fresh normal installed-loader inventory14565checks0:530bare/440helmet states.
All8058 original selected slots retain identical pixels, metadata and clocks versus
V333;384 added water rows are derived references. Verified source playback viewer
offers22groups, paired directions and82/148/54/27px rulers. Browser actually sampled
idle, North/South turn entry/endpoints, diagnostics early/later, repair, unloading
middle/end and cargo. Diagnostics screenshot retained. Loading race fixed before
final samples; no claim of watching every group/pose continuously. Known coarse
cargo quilt and wide North unload stance remain polish concerns; no artwork change.

V349 actual James die() and normal renderer:419native checks0,16direction/gear/medium
cases and96pose captures. Routes/work clear, foot stationary, correct death state
and terminal pose held. All8native chronology boards viewed: dry poses visible beside
furnishings without obvious cut-off; wet lighting too dim for fine grade/material
judgment. Prescribed clocks/explicit die(), not natural oxygen/starvation dispatch
or continuous motion evidence. Scratch APPDATA, owner unchanged, pairedUIDs;
105PNG media LFS. Next remaining selected motion/furniture/lifecycle review, then
fresh playable build and packaged gameplay/Continue. Full goal incomplete; no build
or publication. Viewer: character/james-west-carry-walk-keys-v1/release-motion-review-v348/index.html.
Handoff: character/james-west-carry-walk-keys-v1/release-death-review-v349/HANDOFF.md.
'''
record_guides(r,section,'### James swimming handoff installed for release closeout — October 3, 2026')
handoff='# Project handoff\n\nUpdated October 3, 2026 · James release checks\n\n## Objective and acceptance\nFinish existing James set and prepare next version soon. Full goal incomplete.\n\n## Accepted decisions and constraints\nPreserve accepted artwork/tools/owner saves. No new speculative material studies.\n\n## Current state\n'+section+'\n## Verification\nFresh bank14565checks0;8058original slots exact;419native death checks0/96captures;8boards and specified browser samples viewed. Scope limits in review.json.\n\n## Next action\nRemaining walk/weld/rest and furniture/lifecycle review, then fresh playable build and packaged gameplay/Continue. Avoid restarting stationary water/death proof.\n'
(d/'HANDOFF.md').write_text(handoff);(m/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=p/'material-repair-progress.json';old=f.read_bytes();data=json.loads(old);data['releaseSelectedReview']={'version':348,'checks':14565,'protectedOriginalSlots':8058,'groups':22};data['releaseNativeDeathReview']={'version':349,'checks':419,'cases':16,'captures':96};assert f.read_bytes()==old;f.write_text(json.dumps(data,indent=2)+'\n')
print('Closed V348/349:8058original slots unchanged;419native checks0;96captures/8reviewed boards;105LFS media;five guides updated')
