from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'south-arrival-v325';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());inputs=json.loads((o/'inputs.json').read_bytes())
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert(n['checks'],n['failures'],len(n['results']))==(2542,0,2)
assert all(sha(r/f)==h for f,h in inputs['preLaunchSha256'].items())
assert all(len(row['observedSlots'])==17 and len(row['captures'])==21 and len(row['checkpoints'])==2 for row in n['results'])
assert len(json.loads((o/'review-boards.json').read_bytes()))==6
log=(o/'native_probe.log').read_text(encoding='utf-8');assert 'SCRIPT ERROR:' not in log and 'ERROR:' not in log
review=dict(disposition='normal_south_arrival_half_turn_enabled',checks=2542,failures=0,routes=2,nativeCapturesReviewed=42,freshSceneWholeRunDiskRestores=4,normalHalfTurnMs=1600,arrivalHalfTurnMs=1480,middleHoldMs=80,unloadMs=520,totalArrivalMs=2000,rawArtworkChanged=False,visualMotionAcceptance=False,fullGoalComplete=False,findings=['Earlier missing-south-clip diagnosis was wrong. The11-pose half-turn exists and is normally loaded; its1600ms plus520ms unload exceeded2s arrival guard. Key existence and budget admission had been conflated.', 'Arrival-specific remap shortens only duplicated200ms stationary side-view hold to80ms. Moving pose intervals and all11drawings preserved. Generic half-turn timing remains1600ms; unknown timing profile keeps fallback. JSON float clocks compared numerically with known profile, not strict Array type equality.', 'Actual collision-clear96-unit south approaches through normal update/move/arrive, both gears: all11turn and6unload slots seen, physically fixed arrival root and stage completion, exact north endpoint reuse.4fresh normal whole-run disk restores, source pose/actor/playback/clocks exact and pause holds.2542checks0;42native capture regions plus full11-pose bare source board viewed.', 'Review crop originally centered on clipped screenshot height and cut off resumed feet. Original full capture proved feet visible; assembler now anchors to nominal square capture centre using width. No original screenshot/body manipulation; no new native run needed for review crop correction.', 'These are prescribed controller routes/static advancing samples, not autonomous goal choice, title-screen Continue or continuous real-time motion acceptance. Existing source anatomy/material/head/gear/height/support and full family polish remain. Latest49carry/306turn/317and320unload candidates unselected.'])
(o/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
old_review=p/'arrival-controller-v321/review.json';historic=json.loads(old_review.read_bytes());historic['availabilityCorrectionV325']='South half-turn is present.321 availability test combined key existence with2s budget;1600+520ms exceeded budget.325 distinguishes this and enables arrival-specific1480ms clock.';old_review.write_text(json.dumps(historic,indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old)
d['southArrivalReview']=dict(version=325,file=(o/'review.json').relative_to(r).as_posix(),checks=2542,failures=0,capturesReviewed=42,freshSceneWholeRunDiskRestores=4,normalHalfTurnMs=1600,arrivalHalfTurnMs=1480,rawArtworkChanged=False,availabilityCorrection='clip_exists_but_original_budget_rejected')
d['nextVisualRepair']='325 enables existing11-pose SouthNorth arrival by reducing duplicated side hold200->80ms only during arrival, full1480+520=2s.2542checks0/42native captures/4fresh whole-run restores. West/east/south arrivals now have available turns; North direct. Next advancing paired pacing and master anatomy/material/head/gear/support/case/rise/helmet polish; autonomous goal choice/titleContinue/interruptions and whole-family consistency. Latest source candidates remain unselected.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James south arrival half-turn budget - October3,2026

V325 corrects earlier missing-clip diagnosis: SouthNorth11pose half-turn exists
in normal banks;1600ms plus520ms unload exceeded2s arrival guard. Availability
checks conflated key presence with timing admission. Arrival-specific clock now
reduces duplicated stationary side-view hold200to80ms, retaining all11drawings and
moving pose intervals;1480+520=2000ms. Generic half-turn remains1600ms and unknown
profile keeps fallback. Numeric profile checks handle JSON floats versus integer
constants; strict Array equality initially rejected matching clocks (log retained).

Actual normal96-unit south approaches in both gears:2542checks0, all11turn/6unload
slots observed, fixed physical arrival root, exact North endpoint reuse and stage
completion.4fresh-scene whole-run disk restores without candidate reinstall,
exact actor/playback/source/clocks, pause holds, owner unchanged/frozen hashes.
42native capture regions and full11-pose bare source board viewed. Review crop
centres on nominal square capture, not shortened viewport-clipped height; original
screenshots retain visible resumed feet. No body repaint/fit/raw artwork change.

Lessons: distinguish missing key from rejected duration. Composite duplicated holds
can be shortened locally without accelerating rotating poses or changing a general
clip. Check real JSON numeric types and all authored slots after timing remap.
Prescribed routes/sampled captures are not autonomous goals, titleContinue or
continuous real-time motion approval. Source master/material/anatomy/head/gear,
support/case/rise/helmet and whole-family polish remain; latest review art unselected.
Handoff: character/james-west-carry-walk-keys-v1/south-arrival-v325/HANDOFF.md.
'''
guides=record_guides(r,section,'### James normal arrival journey and exact unload entrance - October3,2026')
(o/'HANDOFF.md').write_text('''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James south arrival

## Objective and acceptance
Full master-matched James set, actual integration and whole-family polish.
Technical admission and sampled motion do not establish visual completion.

## Accepted decisions and constraints
Preserve masters, equipment identity, fixed support, general authored clips and
2s arrival budget. Belt wrench/tablet/forward torch; owner saves untouched.

## Current state
james_workshop_arrival.gd local clock remap enables existing SouthNorth half-turn:
only duplicated side hold200->80ms, arrival1480+unload520=2s, generic1600unchanged.
325normal paired route/restore probeUID/log/evidence, frozen inputs,11pose source
board,42captures/6review boards, retained profile diagnostic. Assembler corrects
viewport-clipped crop centre.321review availability correction, ledger/five guides.
No new artwork or latest review candidate admission.

## Verification
2542checks0;2south approaches, all11turn/6unload slots per gear, fixed physical
root/exact endpoint cut.4fresh whole-run disk restores, actor/playback/pose/clocks
exact and pause holds.42native regions/11source poses viewed; owner unchanged,
frozen hashes stable. Earlier availability diagnosis was budget rejection, not
missing clip. No autonomous goal/titleContinue/continuous real-time review proof.

## Next action
Paired advancing pacing/master anatomy/material/head/gear/support/case/rise and
helmet polish. Autonomous goal choice, full titleContinue and interruptions;
latest49carry/306turn/317and320unload fidelity and all-family consistency remain.
Full goal active, no external blocker.
''',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for f in o.rglob('*.png')];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(checks=2542,failures=0,capturesReviewed=42,freshDiskRestores=4,arrivalMs=2000,guides=guides,lfsRasters=len(rasters),fullGoalComplete=False)))
