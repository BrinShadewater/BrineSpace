import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=r/'output/james-release-closeout-v351';e=p/'release-build-review-v351'
build=json.loads((o/'build-validation.json').read_text());qa=json.loads((o/'release-validation.json').read_text());info=json.loads((o/'deliverable/build_info.json').read_text())
assert all(x['exitCode']==0 for x in build['checks']+qa['checks']) and len(qa['checks'])==2
assert build['realProfileUnchanged'] and qa['realProfileUnchanged'] and qa['qaOverrideRemoved']
assert any('0 failures; debug=false' in line for line in qa['logs']['native-release.log'])
assert any('missing=0 changed=0' in line and 'unexpected=0' in line for line in qa['logs']['asset-audit.log'])
assert (e/'release_smoke.gd.uid').exists()
paths=[x.relative_to(r).as_posix() for x in e.glob('*.png')]
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section=f'''### James Windows release candidate — October 3, 2026

V351 Windows candidate {info['build_id']} physically frozen from selected runtime
dependencies; source fingerprint {info['source_sha256']}. Preserved accepted James
artwork and installed V347 water rows. Corrected CrewLife profile lookup through
script ancestry: actual James cargo actor previously fell back to Bill's differently
sized distress/cargo-turn outline.57 focused human-profile/low-air admission checks0.
Existing concurrent CrewLife changes preserved. Exporter fixes: shared preloaded
icon registry receives normal importer roles (2 regression tests pass); referenced
Theora video collected/exported (9 manifest tests pass). Maintained exporter pass;
selected frozen source release-safety2 tests pass. Whole authoring checkout safety
check still flags10 older BRINE preview assertions, absent from selected snapshot.
Initial failed export attempts preserved: old icon parsing, omitted intro video and
fresh font-import Unicode diagnostics; successful retry reused generated import data.

Exact packed-art audit and actual release New Game/intro skip/saved-loop Continue/F8
pass; debug=false,0 failures, no missing-art placeholders. Native screenshots reviewed
as recorded in release-build-review-v351/review.json. Isolated scratch APPDATA,
owner unchanged; temporary override confined to separate QA copy and removed.
EXE/PCK hashes in output/james-release-closeout-v351/release-validation.json.
Native fixture exit reports32 leaked ObjectDB instances; no engine/script errors
captured during smoke. Long-session memory behaviour is outside this check.
Deliverable: output/james-release-closeout-v351/deliverable/BrineSpace.exe
(keep BrineSpace.pck alongside). Local Windows candidate only; no upload/commit.

Remaining review limits: not continuous visual acceptance of every selected clip,
autonomous water/exterior/hazard coverage or Mac gameplay. Coarse cargo quilt and
wide North unload stance remain polish concerns; no speculative material redo.
Full James animation goal remains incomplete; this milestone supplies a packaged
candidate for playtest and release decision. Handoff:
character/james-west-carry-walk-keys-v1/release-build-review-v351/HANDOFF.md.
'''
review={'version':351,'buildInfo':info,'buildValidation':build,'releaseValidation':qa,'visualReview':'Native New Game, F8 and saved-loop Continue screenshots viewed. Station visible without Fit/Locate; James visible at pod exit in Continue capture; readable icon/font UI and no obvious placeholder/cut-off. Source sit-down browser endpoint also retained. These stationary captures do not certify every clip in continuous motion.','shutdownWarning':'32 leaked ObjectDB instances at native fixture exit; no engine/script errors captured during smoke; long-session memory not certified.','remaining':'Ordinary autonomous water/exterior/hazard visual review and complete continuous selected-clip review; cargo quilt and north unload stance polish remain. Windows candidate only, no publication.'}
(e/'review.json').write_text(json.dumps(review,indent=2)+'\n')
record_guides(r,section,'### James native furniture lifecycle closeout — October 3, 2026')
handoff='# Project handoff\n\nUpdated: October 3, 2026 · Project: Brine Space · Task: James Windows release candidate\n\n## Objective and acceptance\nFinish James and prepare next playable version. Candidate packaged and tested; full visual goal remains incomplete.\n\n## Accepted decisions and constraints\nAccepted artwork preserved, forward torch/tablet/belt-wrench decisions retained, owner saves protected. Local Windows preparation authorised; no publication performed.\n\n## Current state\n'+section+'\n## Verification\nSee review.json for actual package identity, exact audit, release-template smoke and owner profile evidence. Three native package captures and source seated endpoint reviewed.\n\n## Next action\nPlaytest this exact Windows candidate. Resolve visible defects within existing accepted set; record remaining material/stance polish explicitly. Publication or Mac validation requires its own scope.\n'
(e/'HANDOFF.md').write_text(handoff);(o/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=p/'material-repair-progress.json';old=f.read_bytes();ledger=json.loads(old);ledger['releaseWindowsCandidate']={'version':351,'buildId':info['build_id'],'sourceSha256':info['source_sha256'],'checksPassed':True,'published':False,'fullVisualGoalComplete':False};assert f.read_bytes()==old;f.write_text(json.dumps(ledger,indent=2)+'\n')
f=r/'docs/JAMES_RELEASE_CLOSEOUT.md';old=f.read_bytes();s=old.decode();s=s.replace('Use the maintained release exporter and a fresh output directory once the selected James bank is settled. | Freeze the selected inputs, build, verify packaged assets and run a scratch-profile gameplay/Continue smoke test.',f'V351 local Windows candidate {info["build_id"]}: physically frozen inputs, maintained exporter, exact package audit and actual release New Game/saved-loop Continue/F8 pass. | Playtest this exact candidate; preserve review limits. No upload or Mac gameplay acceptance.')
s=s.replace('Next action: freeze selected release inputs and prepare a fresh playable candidate, exact package audit and scratch-profile gameplay/Continue check. Preserve the remaining review limits above.','Next action: playtest the V351 Windows candidate at output/james-release-closeout-v351/deliverable/BrineSpace.exe (PCK alongside). Preserve the remaining visual review limits above and keep release/publication decisions tied to this exact package.')
assert f.read_bytes()==old;f.write_text(s)
print(json.dumps({'buildId':info['build_id'],'candidate':str(o/'deliverable/BrineSpace.exe'),'published':False,'ownerUnchanged':True}))
