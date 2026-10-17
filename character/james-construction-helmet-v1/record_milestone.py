from pathlib import Path
import json,hashlib,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,data):
    temporary=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');temporary.write_bytes(data);os.replace(temporary,p)
def write(p,value):atomic(p,(json.dumps(value,indent=2)+'\n').encode('utf-8'))
before=read(P/'runtime-input-before.json');after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before};assert before==after
write(P/'runtime-input-after.json',after)
guards={}
for fixture in ['lifecycle','north','continue','safety','bill_compat','source_paths']:
    guard=read(P/(fixture+'-validation.json'))
    assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged'] and not guard['profileDelta']
    assert 'ERROR:' not in (P/(fixture+'.log')).read_text(encoding='utf-8')
    assert (P/(fixture+'.gd.uid')).exists()
    guards[fixture]={k:guard[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']}
assert 'CREW CONSTRUCTION failures=0' in (P/'bill_compat.log').read_text(encoding='utf-8')
review=read(P/'review-evidence.json');source_paths=read(P/'source-paths-evidence.json')
assert source_paths['checks']==15259 and source_paths['failures']==0 and source_paths['arbitrarySourceEntries']==696
assert sum(f['checks'] for f in review['families'].values())+15259==32964
assert sum(f['distinctCaptures'] for f in review['families'].values())==506
assert sum(f['sourceRGBAMatches'] for f in review['families'].values())==1326
scopes={
    'lifecycle':('lifecycle/validate-evidence.json','Four actual dry helmeted paid life-support builds after genuine core release, ordinary approach/work/economy/controller/completion, initial scene/foot resets between directions. Original ten-second work budget and5Metal per build.351 distinct work/completed native views; repeated source visits reuse first capture,1171 source change records verified. Worn gear via supported setter, not locker fitting or owner-layout acceptance.'),
    'north':('north/evidence.json','One actual dry helmeted North paid build, six power/locked-door holds across draw/held/stow, current source-derived exit/hold/reverse-return, repeated power loss mid-held return, pause and exact paid work/contact/snapshot/sparks checks.131 native captures. Not all-facing interruptions or fresh Continue at all phases.'),
    'continue':('continue-evidence.json','Three actual dry helmeted paid build disk checkpoints into fresh main scenes: North partial exit, East held neutral, South partial return after power loss. Exact source/actor/player/visual clock/pause/order/Metal,21 captures, normal update through completion once. Not all-facing/phase combinations, locker fitting or owner layouts.'),
    'safety':('safety/evidence.json','Three actual dry helmeted South paid-job retractions preempted by removed order, death and critical room flooding. Three native preemption-entry views; immediate helmeted death source membership checked before next update, normal controller clears tool/work/effects. No new visual acceptance of death/flood replacement families.')
}
for family,(relative,scope) in scopes.items():
    p=P/relative;e=read(p);assert e['failures']==0;e['fixtureInheritedScope']=e['scope'];e['scope']=scope;write(p,e)
    review['families'][family]['scope']=scope
    review['families'][family]['visualReview']={'nativeBoardsReviewed':len(review['families'][family]['nativeBoards']),'sourceBoardsReviewed':len(review['families'][family]['sourceBoards']),'assessment':'All distinct recorded native/source views reviewed against original helmet standing masters. Same matte grade, head/helmet placement, standing ruler/proportions, planted foot and exact neutral joins retained.'}
review['visualReview']={'masterReviewed':True,'nativeBoardsReviewed':11,'sourceBoardsReviewed':15,'distinctCapturesReviewed':506,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',review)
selection={'status':'installed_dry_helmet_construction_native_fixtures_reviewed_owner_review_pending','productionFiles':['scripts/crew_construction.gd','scripts/james_construction_motion.gd','scripts/branforth_npc.gd','scripts/bill_npc.gd'],'sourcesChanged':False,'newSourceStates':0,'fullSetComplete':False,'explicitChecks':32964,'failures':0,'distinctNativeCaptures':506,'originalHelmetRGBAMatches':1326,'freshContinues':3,'review':'review-evidence.json','sourceRecipes':source_paths,'compatibility':'Original tests/test_crew_construction.gd passes for Bill/Veld/James in allfour directions; bare compatibility and default shared behavior retained. No invented assertion count.','guards':guards,'inputHashes':'Ten whole-file inputs equal before all native launches and after terminal results; fixture-only safety panel collapse does not alter those dependencies.','archive':'before-safety-panel-collapse: initial24checks/engine0 passed, but first safety native view was covered by build-card panel. Archived initial native evidence/log/guard, collapsed existing UI panel in fixture, final24checks/engine0 and three clear source views reviewed. No production UI change.','scope':{k:v[1] for k,v in scopes.items()}}
write(P/'selection-review.json',selection)
for relative in ['character/james-construction-controller-v2/selection-review.json','character/james-construction-motion-v1/selection-review.json','character/james-construction-interrupt-v1/selection-review.json','character/james-hull-helmet-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    p=R/relative;value=read(p);value['helmetConstructionReview']='character/james-construction-helmet-v1/selection-review.json';write(p,value)
note='''## James dry helmet construction installed — October 1, 2026

character/james-construction-helmet-v1 completes dry helmet claim/reconcile and
original draw/weld/stow presentation for James construction. Four production
files: crew_construction, james_construction_motion, branforth_npc and bill_npc.
Only the custom James advance_construction_motion capability permits helmet
construction; generic actor equipment exclusion remains. Shared snapshot admission
has an explicit James construction opt-in; defaults still reject helmeted weld,
and flooded standing weld remains rejected. Existing paid10seconds/5Metal per
life-support build, ports/routes/safety/research and room completion retained.

Interrupted construction motion now binds saved equipment, selects matching whole
source pool, measures matching held cycle and restores player.current_equipment
with retained held clock on return. Gear changes invalidate old recipes; absent
equipment defaults bare for legacy saves. Paired original12states/counts/durations
are equal. No new PNGs, source states, rescale, retime, anatomy or grade changes.

14748 checks0failures: four genuine dry helmet paid builds with ordinary approach/
controller/work/completion, initial scene/physical-foot resets between directions.
351 distinct work/completed views;1171 source visits match original RGBA, repeat
visits reuse first capture. One North build1434checks0failures/131captures covers
power and locked doors in allthree work phases, current-source exit/neutral hold/
reverse return, repeated loss mid-held return, pause/contact/paid-work/sparks.
Three actual fresh disk main-scene Continues1499checks0failures/21captures: North
partial exit, East hold, South partial return; exact actor/player/source/paused
clock/paid order/Metal and completion once. Not allfacing/phase combinations.

South safety24checks0failures covers removed order/death/critical flooding while
retracting; immediate helmet death source membership before next update and normal
tool/work/effects cleanup. Native captures show preemption-entry poses, not new
visual acceptance of replacement families. First safety native view had a build
card covering the actor: before-safety-panel-collapse retains original green run;
fixture collapses existing UI panel, final24checks and three clear views reviewed.
No production UI change. All native fixtures use supported prescribed worn gear,
not locker fitting integration or natural owner-layout acceptance.

15259 source-path/admission checks0failures cover all696 paired bare/helmet source
indices: exact whole-RGBA arbitrary exit/neutral/reentry/re-interruption algebra,
timing parity and corruption/family/gear guards using actual helmet scratch saved
exit. Legacy bare case is prescribed metadata conversion, not new bare Continue.
Original tests/test_crew_construction.gd also passes Bill/Veld/James four directions.
32964 explicit checks total, separate shared fixture pass has no invented count.
Six final engine0/no-timeout clean logs/scratch APPDATA/strict owner profile
unchanged; ten whole-file inputs frozen before launches equal after terminal runs.

All1326 source records exact original paired RGBA;506 distinct native/source views,
eleven native/fifteen source boards and four-direction helmet master comparison
reviewed. Same184 canvas/p92,172/148 standing ruler, matte colour/proportions,
head/helmet placement, planted foot and neutral joins retained. Owner review
pending. interruption-source-order.gif is50ms per captured source pose, simplified
order, not continuous real-time native gameplay footage. Inherited bare scope
wording preserved separately and corrected in final evidence metadata.

Lesson: gear-aware frame lookup alone is insufficient. The claiming controller,
reconciliation, canonical saved recipe, held-cycle lookup and restored player's
equipment must agree. Keep legacy defaults and generic validation strict. A green
native test with an obscured actor is not visual acceptance: preserve it and
repeat only the obstructed capture context with normal UI made visible.

Remaining: other-facing full construction interruption/repeated-loss matrix,
full fresh Continue facing/phase matrix, actual locker fitting into jobs, natural
owner layouts/alternate room ports and furniture; wider full-set/master/rotation/
cross-family and owner/export polish. Full James animation objective remains active.
'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(guides):
    data=p.read_bytes();assert note.splitlines()[0].encode() not in data
    atomic(p,note.encode('utf-8')+b'\n'+data if i==0 else data.rstrip(b'\r\n')+b'\n\n'+note.encode('utf-8'))
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James dry helmet construction

## Objective and acceptance
Full James set matching masters/style/perspective/size/height/proportion/grade,
then cross-family polish. Dry helmet construction installed and fixture reviewed;
owner review pending, full objective remains incomplete.

## Accepted decisions and constraints
Original matte paired184/p92,172/148 sources, paid10seconds/cost/ports/routes/safety.
Preserve owner save/furniture and concurrent Bill/Veld work. Prescribed worn gear
and initial scene/foot resets are not natural owner-layout or locker fitting proof.

## Current state
Four production files: crew_construction, james_construction_motion, branforth_npc,
bill_npc. James-specific helmet claim/reconcile and snapshot admission; gear-bound
interruption recipes and matching held player clock/equipment restored. Legacy bare
defaults and generic helmet/flood weld exclusions retained. No new source artwork.
Six paired UID fixtures, five guides and five parent selections updated.

## Verification
32964 explicit checks0failures, shared Bill/Veld/James construction fixture passes.
Four real helmet builds, North six holds/repeated loss/pause, three fresh disk main
Continues and South order/death/flood cleanup.696 paired source recipe entries.
1326 original RGBA records/506 distinct captures,11native/15source boards/master
reviewed. Six final engine0/no-timeout/clean-log scratch guards, strict owner profile
unchanged; ten prelaunch/after hashes equal. Initial safety panel-obscured capture
archived; fixture panel collapse and final three clear views reviewed. GIF simplified
50ms/source pose order, not continuous native footage.

## Next action
Other-facing construction interruption/repeated-loss matrix and facing/phase
fresh Continue, actual locker fitting into jobs/natural owner layouts/ports/furniture;
wider full-set/master/rotation/cross-family/owner/export polish. Goal stays active.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'checks':32964,'distinctCaptures':506,'sourceRecords':1326,'freshContinues':3,'guards':6,'inputs':10,'guides':5}))
