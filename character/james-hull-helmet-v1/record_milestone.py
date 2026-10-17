from pathlib import Path
import json, hashlib, os, uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,data):
    temporary=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');temporary.write_bytes(data);os.replace(temporary,p)
def write(p,value):atomic(p,(json.dumps(value,indent=2)+'\n').encode('utf-8'))
before=read(P/'runtime-input-before.json')
after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
assert before==after
write(P/'runtime-input-after.json',after)
guards={}
for fixture in ['north','cardinal','return','reassign','bill_compat','hull_regression']:
    guard=read(P/(fixture+'-validation.json'))
    assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged'] and not guard['profileDelta']
    assert 'ERROR:' not in (P/(fixture+'.log')).read_text(encoding='utf-8')
    assert (P/(fixture+'.gd.uid')).exists()
    guards[fixture]={key:guard[key] for key in ['exitCode','timedOut','realProfileUnchanged','profileDelta']}
assert 'HULL REPAIR PASS' in (P/'bill_compat.log').read_text(encoding='utf-8')
review=read(P/'review-evidence.json');regression=read(P/'hull-regression-evidence.json')
assert regression['checks']==740 and regression['failures']==0
assert sum(f['captures'] for f in review['families'].values())==455
assert sum(f['checks'] for f in review['families'].values())+740==28549
scope={
    'north':'Prescribed four helmet directions/five paid budgets/source phase seams plus one actual normal North dry helmeted paid rupture job, genuine core release,52 native captures and three paused real disk fresh-scene Continues. Original14seconds/5Metal/work/effects/completion. Worn gear through supported setter; not locker fitting or all natural owner layouts.',
    'cardinal':'Three actual dry helmeted paid rupture jobs, East/South/West in dedicated life-support fixture. Prescribed clear physical interior start and available wall band through inherited James floor/prop checks; ordinary Hull.approach/path/move and paid game updates.305 native captures. Not natural other-wall routing in owner layouts, cross-room travel, other-facing Continues or interruption acceptance.',
    'return':'Three actual dry helmeted North paid job cancellations during draw/held/stow, normal cancellation/refund/requeue,39 captures and three paused real disk fresh-scene Continues. Exact source-to-neutral recipe and fixed foot. Prescribed worn gear, not locker fitting, all facings or critical hazards.',
    'reassign':'Three actual dry helmeted North paid jobs with same-worker no-op and outgoing reassignment to temporary prescribed present waiting Bill, rapid return to James before peer update/claim, same paid work reentry.59 captures and three fresh-scene disk Continues. Not incoming Bill claim/service animation or other-facing interruption proof.'
}
for family,description in scope.items():
    p=P/family/'native-evidence.json';e=read(p);assert e['failures']==0
    e['fixtureInheritedScope']=e['scope'];e['scope']=description;write(p,e)
    review['families'][family]['scope']=description
    review['families'][family]['visualReview']={'nativeBoardsReviewed':len(review['families'][family]['nativeBoards']),'sourceBoardsReviewed':len(review['families'][family]['sourceBoards']),'assessment':'All captured native/source views reviewed against original helmet standing masters. Matte material, helmet/head placement, standing scale/proportions, planted foot and exact neutral joins retained. Native water/lighting overlay changes are separate from unchanged source RGBA.'}
review['visualReview']={'masterReviewed':True,'nativeBoardsReviewed':12,'sourceBoardsReviewed':13,'capturedSourcesReviewed':455,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',review)
selection={'status':'installed_dry_helmet_hull_lifecycle_native_fixtures_reviewed_owner_review_pending','productionFiles':['scripts/branforth_npc.gd','scripts/hull_repair.gd','scripts/james_hull_resume.gd','scripts/bill_npc.gd'],'sourcesChanged':False,'newSourceStates':0,'fullSetComplete':False,'explicitChecks':28549,'failures':0,'captures':455,'originalHelmetRGBAMatches':455,'freshContinues':9,'review':'review-evidence.json','compatibility':{'bareHullCanonical':regression,'billHull':'Original tests/test_hull_repair.gd passes, including submerged generic repair behavior; no invented assertion count.'},'guards':guards,'frozenInputs':'Ten whole-file input hashes equal before all six native launches and after terminal results.','scope':scope,'lessons':['Original paired timing parity is required before sharing paid-clock recipes across equipment.','Authoritative work controller, animation eligibility and save admission must agree: original controller forced helmeted dry James to generic repair.','Optional shared helmet Hull admission is explicit for James only; shared default, construction and flooded weld remain rejected. Generic submerged repair retained.','Canonical gear-bound return/reentry from the preceding ward milestone works for dry Hull after family exclusion is removed; missing equipment remains bare.','Do not infer natural cardinal routing or all-facing fresh Continue from dedicated wall-band fixtures.']}
write(P/'selection-review.json',selection)
for relative in ['character/james-hull-lifecycle-v1/selection-review.json','character/james-hull-cardinal-v1/selection-review.json','character/james-hull-return-v1/selection-review.json','character/james-hull-reassign-v1/selection-review.json','character/james-ward-helmet-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    p=R/relative;obj=read(p);obj['hullHelmetLifecycleReview']='character/james-hull-helmet-v1/selection-review.json';write(p,obj)
note='''## James dry helmet Hull lifecycle installed — October 1, 2026

character/james-hull-helmet-v1 connects original paired helmet torch sources to
the paid Hull draw/weld/stow controller and North cancellation/reassignment.
Four production files: branforth_npc, hull_repair, james_hull_resume and bill_npc.
The generic Hull controller formerly sent all helmeted actors to repair, while
James lifecycle/admission excluded helmets. Dry actors exposing James's custom
sync_hull_animation now use weld with either gear; other actors retain original
behavior. James explicitly opts into shared dry helmet Hull admission through a
separate optional flag. Shared default, helmet construction and flooded weld
remain rejected. Flooded actors retain generic repair, not dry standing weld.
Gear-bound whole-source return/reentry retained; legacy absent gear remains bare.
Original paired12states have equal frame counts/durations. No new PNGs, retiming,
rescaling, anatomy or grade changes; original paid work/cost/hazard rules remain.

6470 North checks0failures include prescribed four helmet directions/five paid
budgets/source seams and an actual normal North14second/5Metal rupture job.
52 native captures and three paused real disk fresh-scene Continues at draw/
held/stow; exact actor/player/room/source/paused clock and derived cache retained.
20463 checks0failures/305 captures cover three actual East/South/West paid jobs
in dedicated life-support fixture: prescribed clear interior start and available
wall band, inherited real floor/prop checks, ordinary approach/path/move/work.
This is not naturally chosen cardinal routing on the owner's layouts.

North actual cancellation422 checks0failures/39 captures/three fresh Continues
retains refund, paid-once replacement and exact current-source-to-neutral return.
Actual reassignment454 checks0failures/59 captures/three fresh Continues preserves
same-worker pose and rejoins exact paid helmet source after whole-source entry.
Temporary prescribed present Bill is removed before updates/checkpoints; no
incoming Bill service claim. Bare canonical compatibility740 checks0failures/
180 prescribed samples includes legacy saves and20 narrow family admission checks.
Original Bill hull fixture passes, including submerged generic repair behavior.

Six final engine0/no-timeout clean logs, strict owner profile unchanged with
scratch APPDATA. Ten whole-file inputs frozen before all final launches equal
after terminal results.28549 explicit checks overall; separate Bill pass has no
invented count. All455 captured helmet sources match exact original RGBA.
Twelve native/thirteen source boards and four-direction standing-master comparison
reviewed. Original184 canvas/p92,172/148 standing ruler, matte finish, stable
helmet/head and planted feet retained. Native water/lighting changes do not mean
source grade changes. Paid-clock GIF reconstructs14second source clock, not
continuous native gameplay effects footage. Inherited bare scope wording is
preserved separately and corrected in metadata. Owner acceptance remains pending.

Lesson: available equipment sources are not runtime coverage until the owning
work controller, animation hooks and saved-state admission agree. Prove actual
jobs and fresh Continue; keep family exceptions explicit rather than stripping
equipment or relaxing generic validation. Source parity and native physical
worksite review establish different requirements. Keep legacy bare compatibility.

Next: helmet construction lifecycle; other-facing interruptions/fresh Continues,
locker fitting integration, natural owner layouts, hazard/power/door/incoming
workers and moving furniture/claimed-point/full silhouette clearance. Continue
full-set/master/cross-family/rotation/owner/export polish. Full objective active.
'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(guides):
    data=p.read_bytes();assert note.splitlines()[0].encode() not in data
    atomic(p,note.encode('utf-8')+b'\n'+data if i==0 else data.rstrip(b'\r\n')+b'\n\n'+note.encode('utf-8'))
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James dry helmet Hull lifecycle

## Objective and acceptance
Full James set matching masters/style/perspective/size/height/proportion/grade,
then cross-family polish. This dry helmet Hull milestone installed and reviewed
in dedicated fixtures; owner review pending, full goal remains incomplete.

## Accepted decisions and constraints
Original paired matte sources184/p92,172/148, original paid work/cost/safety.
Preserve owner save/furniture and concurrent Bill/Veld work. Prescribed worn gear,
not locker fitting. Dedicated cardinal wall-band/interior start is not natural
owner-layout routing. Generic flooded repair remains unchanged.

## Current state
Four production files: branforth_npc, hull_repair, james_hull_resume, bill_npc.
James dry helmet draw/weld/stow, gear-bound return/reentry and explicit shared
Hull save admission. Shared defaults and helmet construction still excluded.
No new artwork. Six paired UID fixtures, five guides/six parent links updated.

## Verification
28549 explicit checks0failures; Bill Hull pass separately. Four actual paid jobs,
North cancellation/reentry at allthree work phases.455 exact original source RGBA
captures reviewed on12native/13source boards and master comparison. Nine paused
real disk fresh-scene Continues. Six engine0/no-timeout/clean-log scratch guards,
strict owner profile unchanged. Ten prelaunch/after input hashes equal. Bare
canonical180samples/legacy default compatibility retained. GIF source-only14s.

## Next action
Helmet construction lifecycle, other-facing interruptions/Continues, locker
fitting, natural owner layouts/hazards/power/doors/incoming workers and moving
furniture/claimed-point/full silhouette clearance. Wider full-set/master/
cross-family/rotation/owner/export polish. Active goal remains incomplete.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':28549,'captures':455,'freshContinues':9,'guards':6,'frozenInputs':10,'guides':5}))
