from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(p,data):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,p)
def write(p,obj):atomic(p,(json.dumps(obj,indent=2)+'\n').encode('utf-8'))
before=json.loads((P/'runtime-input-before.json').read_bytes());after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before};assert before==after
write(P/'runtime-input-after.json',after)
guards={d:json.loads((P/(d+'-validation.json')).read_bytes()) for d in ['east','south','west']}
assert all(g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta'] for g in guards.values())
review=json.loads((P/'review-evidence.json').read_bytes())
review['visualReview']={'nativeBoardsReviewed':len(review['nativeBoards']),'sourceBoardsReviewed':len(review['sourceBoards']),'masterComparisonReviewed':True,'assessment':'All captured original whole poses retain master scale, planted physical foot, matte grade and original draw/stow idle joins. Native body views visible at actual doorway workpoints in all three directions. West native held views show nearby storage furniture overlapping the torch area; clear tool-to-door work line remains unproven and needs clearance investigation. Source-only preview; owner acceptance pending.','worksitePolishComplete':False,'nextFinding':'West native-page4/native-page3: inspect actual furniture/torch overlap and Ward.approach candidate clearance before declaring room contact polished.'}
write(P/'review-evidence.json',review)
selection={'status':'native_cardinal_ward_fixture_reviewed_owner_review_pending','runtimeChanged':False,'sourcesChanged':False,'newDrawings':0,'newSourceStates':0,'fullSetComplete':False,'review':'review-evidence.json','nativeChecks':review['checks'],'nativeCaptures':review['captures'],'freshDiskContinues':review['freshContinues'],'guards':guards,'runtimeInputsBefore':'runtime-input-before.json','runtimeInputsAfter':'runtime-input-after.json','scope':review['scope']}
write(P/'selection-review.json',selection)
for relative in ['character/james-ward-lifecycle-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    p=R/relative;obj=json.loads(p.read_bytes());obj['wardCardinalReview']='character/james-ward-cardinal-v1/selection-review.json';write(p,obj)
note=f'''## James cardinal ward approach and Continue review — October 1, 2026

character/james-ward-cardinal-v1 expands installed ward evidence to East/South/West.
Three actual paid18-second/8Metal cryo repairs through genuine core release,
ordinary cross-room navigation and original work/reward logic. Dedicated relocated
and rotated cryo ward with one normal storage access room per case; no actor
foot/facing/path/collision overrides or owner-layout changes. Draw/held/stow sources
remain selected original matte artwork; no production code/art/state edits.

{review['checks']} native checks0failures/{review['captures']} captured views;
{review['freshContinues']} paused real disk fresh-scene Continues (each direction
at draw/held/stow), exact actor/player/source/paid progress and derived18-second
cache. Original charge once and occupants retained at normal completion. All
{len(review['nativeBoards'])} native/{len(review['sourceBoards'])} source boards and
same148/p92,172 matching master board reviewed. Physical foot fixed per job;
viewport crops follow recorded camera foot after Continue/award recentering.
Three final engine0/no-timeout/strict owner-profile guards pass; seven shared
runtime/source hashes frozen across all three runs. ward-cardinal-paid-clock.gif
reconstructs18-second source clock at50Hz plus neutral hold, not continuous native
lighting/effects footage. Owner visual review pending.

Native West review exposes nearby storage furniture overlapping the torch area.
Body/source/master consistency passes; clear tool-to-door work line and room
interaction polish do not. Next inspect the actual prop clearance and approach
candidates; preserve owner furniture and original body anatomy. Do not substitute
technical phase/Continue success for worksite contact acceptance.

Lesson: choose work orientation through actual ward doorway rotation and ordinary
approach before touching actor pose. Prescribed ward location is fixture geometry,
not proof of natural owner-layout access. Save restoration owns paid pose timing
independently of direction and cosmetic playback. Compare body height/pivot and
grade with each matching master, not equal fitted image boxes or flame bounds.

Remaining: other gear/ward kinds, pause-work/critical flood/power/door interruptions,
incoming-worker handoffs and natural owner-layout access; wider full-set/master/
cross-family/furniture/rotation/owner/export polish. Full animation goal incomplete.

'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(guides):
    data=p.read_bytes();assert note.splitlines()[0].encode() not in data
    atomic(p,note.encode('utf-8')+data if i==0 else data.rstrip(b'\r\n')+b'\n\n'+note.rstrip().encode('utf-8')+b'\n')
handoff=f'''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James cardinal ward repair

## Objective and acceptance
Full James animation set, continually matching masters/style/perspective/height/
proportions/grade, then cross-family polish. This milestone adds directional
native and fresh Continue evidence; full goal remains incomplete.

## Accepted decisions and constraints
Original whole matte sources,148 ruler/p92,172. Actual paid18seconds/8Metal;
ordinary cross-room approach, dedicated rotated/relocated ward/storage fixtures.
No actor pose/path/collision overrides, new art or production controller edits.
Preserve concurrent Bill/Veld work and owner saves/layouts. Owner review pending.

## Current state
East/South/West native fixtures with paired UIDs, source/native boards, master
comparison and paid-clock preview here. Five guides and two parent selections
updated. Production ward lifecycle from previous milestone remains installed.

## Verification
{review['checks']} checks0failures/{review['captures']} captured source/native
views;9 real disk fresh-scene Continues,3 per direction. Original paid progress,
cost, paused clock, source/player and derived cache exact. Each18-second job
completes once. All boards/master comparison visually reviewed.
Three engine0/no-timeout/strict owner-profile guards; seven input hashes stable.
18-second50Hz preview reconstructs source clock, not continuous gameplay footage.

## Next action
First investigate West furniture/torch overlap and ordinary ward worksite
clearance. Original source/master consistency passes, full room contact unproven.
Other ward gears/kinds; pause-work/power/door/critical-flood/incoming-worker and
natural owner-layout access. Wider master/cross-family/furniture/rotation/owner/
export consistency and full-set polish. Goal active.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':review['checks'],'captures':review['captures'],'freshContinues':9,'guidesUpdated':5,'inputHashesStable':7}))
