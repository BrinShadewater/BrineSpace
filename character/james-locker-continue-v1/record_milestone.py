from pathlib import Path
import hashlib,json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_bytes())
def atomic(p,b):
 t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
def write(p,v):atomic(p,(json.dumps(v,indent=2)+'\n').encode())
g=read(P/'validate-validation.json');e=read(P/'evidence.json');v=read(P/'review-evidence.json')
assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta']
assert not any(s in (P/'validate.log').read_text() for s in ['ERROR:','SCRIPT ERROR:'])
assert (P/'validate.gd.uid').exists() and e['failures']==0 and len(e['cases'])==18
assert all(c['completed'] and c['diskRestored'] for c in e['cases'])
assert v['checkpointPairsExact']==18 and v['sourceRGBAMatches']==len(e['records']) and all(v['removalEndpoints'].values())
before=read(P/'runtime-input-before.json');after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
assert before==after;write(P/'runtime-input-after.json',after)
nb=len(v['boards']['native']);sb=len(v['boards']['source']);pb=len(v['checkpointPairBoards'])
v['visualReview']={'nativeBoardsReviewed':nb,'sourceBoardsReviewed':sb,'checkpointPairBoardsReviewed':pb,'removalContactReviewed':True,'finding':'Exact saved/restored selected poses retain foot contact, anatomy and matte grade. Powered-off room illumination differs from lit room; original sources remain exact. No new restore-induced pose or material discontinuity observed in these captures.','continuousNativeCadenceReviewed':False,'ownerAcceptance':'pending'}
write(P/'review-evidence.json',v)
selection={'status':'locker_disk_continue_poses_reviewed_owner_pending','productionChanges':False,'newSourceStates':0,'fullSetComplete':False,'checks':e['checks'],'failures':0,'cases':18,'captures':len(e['records']),'scope':e['scope'],'review':'review-evidence.json','guard':{k:g[k] for k in ['exitCode','timedOut','realProfileUnchanged','profileDelta']},'productionInputsUnchanged':len(before),'archive':'before-time-limit-correction: terminal exit124 at600 seconds,16 completed cases, owner profile unchanged; incomplete. Full18-case repeat exited0 with1800-second limit.'}
write(P/'selection-review.json',selection)
q=R/'character/james-locker-removal-interrupt-v1/selection-review.json';x=read(q);x['diskContinue']='character/james-locker-continue-v1/selection-review.json';write(q,x)
note=f'''## James locker disk Continue — October 1, 2026

All18 actual disk checkpoints passed: fitting/removal at source slots2/6/10,
each during forward action, power-loss return and suspended-room return.
{e['checks']:,}checks0failures; {len(e['records'])} selected-source/native captures.
Fresh main scenes in the same engine process restore exact actor/player state,
RGBA source, timer, foot, gear, world clock and resources. Paused updates remain
frozen; normal60Hz completion commits gear only for uninterrupted actions.
Removal prerequisites acquire the helmet through actual AirlockService.

All{nb} native,{sb} source and{pb} before/after boards plus removal contact reviewed.
All18 saved/restored source pairs match; normal removal endpoints exactly match
the selected helmet/bare masters after pivot alignment. No new restore-induced
pose or material discontinuity observed. Power-off native room lighting differs,
while exact original source artwork is retained. No art, grade, timing, manifest
or production changes; {len(before)} frozen production inputs stayed byte-identical.
Engine exited0 without timeout or logged errors; strict owner profile unchanged.

Earlier600-second run ended at its actual terminal timeout after16 cases; archived
in before-time-limit-correction, not counted as a full pass. Repeat retained the
full matrix and completed with1800-second limit. Evidence/HANDOFF:
character/james-locker-continue-v1. Supersedes pending Continue notes below.

Scope: prescribed East locker, same-process fresh-scene disk restore and per-leg
unique source captures. No title/fresh-process Continue, other locker orientations,
safety evacuation, natural owner layouts or continuously watched native cadence.
Owner acceptance and full James goal remain open. Next: remaining full motion,
furniture/exterior journeys and cross-family master consistency.

'''
q=R/'docs/CURRENT_STATUS.md';atomic(q,note.encode()+q.read_bytes())
lesson=f'''
## James locker saved-pose continuity — October 1, 2026

An admitted snapshot is not disk Continue proof. Exercise Save.capture/write/read
and restore_staged into a fresh main scene; compare exact actor/player snapshot,
selected full RGBA, source slot, timer, foot, gear, world clock and resources.
Then freeze paused updates and finish through the ordinary service controller.
All18 East fitting/removal checkpoints at slots2/6/10 crossed with forward,
power-return and suspension-return passed {e['checks']:,}checks0failures.
Removal prerequisite fitting uses actual AirlockService, not a worn-flag grant.

Reviewed{nb} native/{sb} source/{pb} paired boards and removal contact; all18
source pairs exact, normal removal endpoints exact pivot-aligned masters.
Retain the authored148 physical ruler across184/256 canvases; lifting a helmet
above the head must not trigger per-pose height normalization. Power-off scene
illumination is distinct from source-grade drift. No new restore-induced pose or
material discontinuity observed. No source/timing/production change; {len(before)}
production inputs and strict owner profile unchanged. Terminal engine0/clean log.

The original600-second runner reached its actual terminal timeout after16 cases;
preserve that incomplete run. Repeat full matrix with sufficient1800-second limit
and periodic progress evidence; observation waits are not process termination.
Evidence: character/james-locker-continue-v1. Same-process fresh scenes and per-leg
unique captures do not prove title/fresh-process Continue, natural layouts, other
locker orientations, safety preemption or continuous native cadence. Full James
goal and owner acceptance remain open.
'''
for q in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:atomic(q,q.read_bytes()+lesson.encode())
handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: James locker Continue

## Objective and acceptance
Complete James set and master/material/proportion consistency, then family polish.
This milestone covers18 disk fitting/removal checkpoints. Full goal/owner review open.

## Accepted decisions and constraints
Matte masters,148 standing ruler, original pivots, belt wrench. Scratch APPDATA and
strict real-owner fingerprint guard. No artwork/manifest/timing/production change.

## Current state
validate.gd/paired UID, isolated1800-second runner, review builder and recorder,
reports,294 captured selected poses and16 review boards plus removal contact.
Five maintained guidance files and previous removal review link updated atomically.
Original terminal600-second timeout archived;16 cases incomplete, guard unchanged.

## Verification
Repeat exactsession5915 terminal0/no timeout/clean log/strict owner unchanged.
{e['checks']}checks0failures/all18diskRestored+completed, exact snapshots/source/clock/
gear/foot/resources, paused freeze, ordinary60Hz completion. All5native/8source/
3paired boards and removal contact reviewed. All294fullRGBA sources verified;
18before/after pairs exact, normalized removal endpoints exactmasters.
{len(before)}production before/after hashes equal. No new restore-induced pose/grade
discontinuity found. Same-process fresh main scenes, prescribed East support,
per-leg unique captures: not title/fresh-process Continue, full native cadence,
other locker orientations, safety evacuation or natural owner-layout proof.

## Next action
Remaining full-motion/furniture/exterior journeys and cross-family master polish.
North ordinary swim boot source review complete in james-north-water-master-check-v1;
remaining West water death limb projection and North sleep/full-motion joins need review.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print(json.dumps({'checks':e['checks'],'cases':18,'captures':len(e['records']),'productionInputsUnchanged':len(before),'boardsReviewed':nb+sb+pb}))
