"""Record selected family with explicit source/native limits and fixture history."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-v2/supplemental/west-walk-polish-v1'
RUN=ROOT/'output/marsh-animation-audit/west-walk-selected-world-v1-2026-10-03'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
vpath=OUT/'world-review/verification.json';v=json.loads(vpath.read_text())
assert (v['checks'],v['failures'],v['inputsStable'],v['ownerNonLogStable'])==(1579,0,5524,2931)
for b in v['boards']:
    assert sha(ROOT/b['path'])==b['sha256'];b['reviewed']=True
v['visualReview']='All six complete native/source comparison boards and first full1600x900native inspected. Source full-figure/family/head/master/idle/start/stop/run review complete for changed poses; selected West walking improvement accepted within recorded scope.'
vpath.write_text(json.dumps(v,indent=2)+'\n')
frozen=json.loads((RUN/'inputs-after.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
inventory=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-west-walk/inventory.json'
browser=inventory.parent
receipt={'normalAdmission':True,'fullGoalComplete':False,'nativeVerificationSha256':sha(vpath),'normalInventorySha256':sha(inventory),'testedHashesStillExact':len(frozen),'reviewed':True,'sourceReviewSha256':sha(ROOT/'character/marsh-west-walk-family-detail-v1/review.json'),'closingBoardSha256':sha(ROOT/'character/marsh-west-walk-family-contact-v1/motion-review/closing-join-board.png'),'browserPageSha256':sha(browser/'motion-review.html'),'browserScreenshotSha256':sha(browser/'browser-quarter.png'),'browserObservations':['normal phase0 clock67 draw5','quarter phase5 clock8966 draw546','screenshot quarter phase4 clock11451 draw1142','quarter phase0 clock63051 draw13516','paused phase0 clock64010 draw13756'],'limits':'Sampled browser advancement, not continuous watched cadence. Original comparison actor absent from several walking crops: those rows support source comparison and selected actor placement, not full paired world comparison. Actual normal catalogue selection, source sole depth and prescribed routes proven; not complete2Dplanted foot, autonomous jobs, all rooms/rotations, paid building or disk fullRunSave/TitleContinue/full-library acceptance.'}
(OUT/'acceptance-review.json').write_text(json.dumps(receipt,indent=2)+'\n')
note="""

## Marsh West six-phase normal walking polish selected — October 3, 2026

All six whole-pose material edits now load through the normal catalogue in
character/marsh-v2/supplemental/west-walk-polish-v1. Exact byte copies of the
reviewed contact bank; no new generation or anatomy fitting in this admission.
Only walk-west changes; all227 other effective state metadata/source hashes
preserved. Timing, pivot92/172, height148 and stride preserved. Current normal
inventory:228states/1190slots/91body manifests, authoritative inventory
character/marsh-selected-normal-audit-2026-10-03-post-west-walk/inventory.json.
Earlier post-East inventory remains the historical original-West baseline.

Closing/opening board sequence5,0,1,2,3,4,5,0 inspected at native density and
fixed65.28/148 station density. New crowns27,24,25,25,24,24 versus original
26,24,25,26,24,25: maximum adjacent/closing3 versus2 pixels. Extra1nativepixel
is .441081world units; retained explicitly, no material discontinuity seen at
station density. Exact authored sole levels retained; crown bounds alone do
not establish anatomical head movement. Face and suit grade coherent in review.

Native normal selected catalogue with no candidate override:1579checks0failures,
260movement samples,2arrival records,36paired captures,3moving actor restores;
5524bounded inputs/2931owner non-log files stable under scratch APPDATA.
Engine exit0/no errors/warnings. All6complete928wide boards plus first full
1600x900native inspected. Original comparison actor absent from several walking
crops: those rows support source-art review and selected-actor placement, not
complete paired world comparison. Strict source sole depth remains exact.
Browser normal/quarter advancement sampled and paused; screenshot retained,
not continuous watched cadence. Source and physical checks are separate evidence.

Acceptance is bounded to this selected family. Full master-matched animation
goal remains active. Next North/South walking material families and cross-family
master/idle/action consistency, then broader natural jobs, water, equipment,
furniture, complete2Dplanted-foot and fullRunSave/TitleContinue acceptance.
Handoff:docs/MARSH_WEST_WALK_SELECTED_HANDOFF_2026-10-03.md.
"""
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('West normal admission recorded; tested hashes exact; four notes and skill mirror updated; full goal active.')
