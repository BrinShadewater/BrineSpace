import hashlib,json,subprocess
from pathlib import Path
from milestone_notes import record_guides
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';journey=p/'water-journey-review-v345';hazards=p/'release-hazard-review-v346'
native=json.loads((journey/'journey-review.json').read_text());validation=json.loads((journey/'journey_probe-validation.json').read_text());art=json.loads((hazards/'review.json').read_text())
assert native['failures']==0 and validation['exitCode']==0 and validation['realProfileUnchanged']
assert art['pixelChecks']==192 and art['failures']==0
images=list(journey.glob('*.png'))+list(hazards.glob('*.png'));names=[x.relative_to(r).as_posix() for x in images]
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(names)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0')
assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
bindings={x.relative_to(r).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in [journey/'journey_probe.gd',r/'scripts/grid_canvas.gd',p/'water-stop-bridge-v340/phase_player.gd',p/'water-stop-bridge-v340/reorient_player.gd',p/'water-stop-bridge-v340/staged_grid.gd']}
report={'nativeChecks':native['checks'],'failures':0,'captures':len(native['captures']),'checkpointRestores':2,'scope':native['scope'],'realProfileUnchanged':True,'postRunBindings':bindings,'normalSelectionChanged':False,'visualReview':'All eight complete registered hazard boards and all ten native route crops viewed. Hazard source gear and grade consistent at this sample scale; no obvious equipment disappearance. Native crops dim under flood lighting; no fine material or temporal acceptance.','hazardSourcePoses':192,'lfsImages':len(images),'initialAttempts':'Initial parse error repaired; first stationary-clear route failed full 24-unit segment clearance. Final fixture selects a clear full-envelope route. Earlier console failure summaries available in conversation; initial files were overwritten by rerun.'}
(journey/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section=f'''### James release closeout, moving swim checkpoint and hazard source review — October 3, 2026

Owner prioritises wrapping James and shipping the next game version soon.
docs/JAMES_RELEASE_CLOSEOUT.md bounds remaining work to selected-set visual defects,
integration/Continue and packaged gameplay checks. Preserve accepted artwork and
stop further speculative fabric generation during this release pass.

V345 two prescribed24-unit flooded routes use actual James move(), real room
geometry and the whole active bridge envelope. {native['checks']}checks0; two fresh
main-scene whole-run disk restores with staged bank installed before restoration;
actor/playback/pause/clock and post-restore pixels exact, finite bridge completes.
Ten native crops viewed; deep flood lighting limits fine material assessment.
Owner profile unchanged under scratch APPDATA. ScriptUIDs paired. Does not prove
autonomous update/goal dispatch, title UI Continue, exterior, blocked fallback or
repeated-command completion. Repair bank remains unselected in normal gameplay.
First proposed stationary-clear foot failed moving segment clearance; select
fixtures against the entire route, not only a pose at its origin.

V346 eight source boards actually viewed:192 exact selected poses for distress,
recovery, ground death and water death; four directions/both gears. All alpha
bounds fit fixed256x400 registered tiles; gear/grade show no obvious source flash
or equipment disappearance. Initial narrow preview cropped poses and was replaced
before final review. Static source review does not certify continuous motion or
hazard/controller acceptance. No source art, grade, scale or normal bank changed.
Remaining: finish water runtime selection decision, selected-set continuous review,
known cargo/unload polish and furniture/hazard lifecycle, then a fresh release build
and packaged gameplay/Continue. Full goal incomplete; no build or upload produced.
Handoff: character/james-west-carry-walk-keys-v1/water-journey-review-v345/HANDOFF.md.
'''
record_guides(r,section,'### James native water renderer and actual actor dispatch — October 3, 2026')
handoff='# Project handoff\n\nUpdated: October 3, 2026 · Task: James release closeout\n\n## Objective and acceptance\nFinish James and prepare the next playable version soon. Full animation goal incomplete.\n\n## Accepted decisions and constraints\nRelease focus; preserve owner-approved poses/tools/grade and owner saves. No new material studies or artwork expansion.\n\n## Current state\n'+section+'\n## Verification\n'+str(native['checks'])+' native checks pass, two fresh scene disk restores, 192 exact hazard source poses, all eight source boards and ten native crops viewed; owner unchanged. Normal bank remains old.\n\n## Next action\nUse docs/JAMES_RELEASE_CLOSEOUT.md. Decide water runtime selection after remaining blocked/exterior/command behavior, complete selected-set motion/lifecycle review, then build and validate the new package.\n'
(journey/'HANDOFF.md').write_text(handoff)
(hazards/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterJourneyReview']={'version':345,'checks':native['checks'],'failures':0,'restores':2,'selected':False};data['releaseHazardReview']={'version':346,'poses':192,'boards':8,'normalChanged':False};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
print(f'Closed release review: {native["checks"]} native checks, 2 disk restores, 192 hazard source poses; {len(images)} LFS images; five guides updated')
