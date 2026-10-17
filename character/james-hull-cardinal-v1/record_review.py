from pathlib import Path
import hashlib,json,os,uuid
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
def atomic(path,data):
    t=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,path)
def write(path,data):atomic(path,(json.dumps(data,indent=2)+'\n').encode())
guards={name:json.loads((P/f'{name}-validation.json').read_bytes()) for name in ['validate','probe','access_probe']}
for g in guards.values():assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and g['profileDelta']==[]
inputs=json.loads((P/'runtime-input-before.json').read_bytes());after={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in inputs};assert inputs==after
native=json.loads((P/'native-evidence.json').read_bytes());views=json.loads((P/'review-evidence.json').read_bytes());assert native['failures']==0
assert all(c['completed'] and c['workSteps']==839 and c['metal']==95 for c in native['cases'])
master_hashes={path:hashlib.sha256((R/path).read_bytes()).hexdigest() for path in views['masterPaths'].values()}
selection={'status':'native_cardinal_fixture_reviewed_owner_review_pending','runtimeChanged':False,'sourcesChanged':False,'newDrawings':0,'newSourceStates':0,'fullSetComplete':False,'native':native,'visualReview':views,'allFinalNativeAndSourceBoardsReviewed':True,'masterComparisonReviewed':True,'masterHashes':master_hashes,'profileGuards':guards,'runtimeInputsStable':True,'runtimeInputHashes':after,'scopeLimit':'Dedicated free-placed life-support room and prescribed interior start/wall availability via inherited James subclass; production floor/prop tests and ordinary paid Hull approach/path/move/update/completion retained. Not naturally chosen non-North owner layout worksite, cross-room travel, other-facing Continue/interruptions or gear proof.','remaining':'Ward/room repair families, other-facing Continue/interruptions/gear, real alternate owner worksite access and incoming-worker handoffs; broader master/cross-family/furniture/rotation/owner/export polish. Full animation goal active/incomplete.'}
write(P/'selection-review.json',selection)
for relative in ['character/james-hull-lifecycle-v1/selection-review.json','character/james-hull-reassign-v1/selection-review.json','character/james-repair-contact-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    path=R/relative;data=json.loads(path.read_bytes());data['hullCardinalReview']='res://character/james-hull-cardinal-v1/selection-review.json';write(path,data)
block=f"""## James East/South/West paid hull repair review — October 1, 2026

Expanded physical job and visual evidence for the installed selected torch family.
No production runtime or source art changes, new drawings or state coverage.
Final {native['checks']} native checks/0 failures: three actual paid rupture repairs,
ordinary Hull.approach/path/move and normal game updates, draw/held/stow/completion.
Each pays original5Metal once and retains839work updates plus completion14seconds.
Planted real floor contacts, selected direction, existing paid pose clock,
exact148 standing ruler/p92,172, valid snapshots, sparks only during held work,
normal sealed hull/released worker/effects, no extra charge.

Scope: dedicated free-placed life-support test room; genuine core release into
inherited James subclass. Prescribed graph-valid interior start and available
wall band leave inherited floor/prop checks in force; regular controller chooses
its physical workpoint/facing. Geometry discovery first checked56 ordinary
room/rotation approaches:31reachable North,25blocked; no naturally selected
other facing. Then24 prescribed access cases demonstrated all four faces in
six room geometries. This does not prove naturally chosen non-North work in
owner layouts, cross-room travel, other-facing Continue/interruptions or gear.
Do not loosen production collision/repair access rules to force this coverage.
All three native intervals engine0/no timeout/scratch APPDATA/strict owner
profile unchanged. Nine frozen runtime/source/torch-contact inputs stable.

All {views['captures']} final selected native sources/completion captured and reviewed
on5native and8whole-source boards; exact source RGBA hashes. Actual standing
masters from crew-runtime-matte-v1/branforth idle East/South/West compared with
entry/held/stow/end at fixed148 ruler. Stable head/feet, matte grade and body
proportions; no per-pose scale/grade adjustment. Damage-driven water/vapor varies
independently of immutable source pixels. Fixed screenshot crop feet verified
against full native views; physical actor.foot, viewport stretch applied once.
All303declared East/South/West source-reference pixels are covered. At60Hz the
last short West stow slot31 is skipped as a key/index, but its RGBA is exactly
native drawWest0/completed idleWest0. Preserve that proven endpoint alias;
do not prolong paid work simply to make every source index appear in a capture.

cardinal-paid-clock.gif reconstructs the normal14second paid clock at50Hz using
only native-verified original whole source pixels (plus1second idle); no room
lighting/water/effects or actual continuous gameplay-footage claim. This replaces
compressed pose-order timing for a more useful pace review. Original source
phase/index math checked against every captured work clock. All masters and
selected sources retain their identity, perspective and standing scale.
Lesson: distinguish naturally selected worksite evidence from branch fixtures,
keep physical collision checks in the fixture, and compare source pixels/master
rulers separately from environment overlays. A source endpoint alias can prove
a clean completion join even when a tiny slot is unsampled at the native tick.
Ward/room repair, other-facing Continue/interruptions/gear, real alternate owner
worksite access/incoming handoffs and wider cross-family/master/furniture/
rotation/owner/export polish remain. Full animation goal active/incomplete.
Evidence/HANDOFF:character/james-hull-cardinal-v1.

"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes();b=block.encode();atomic(path,b+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+b)
handoff=f"""# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James cardinal hull repair

## Objective and acceptance
Full James animation set and master/style/height/grade consistency, then wider
cross-family polish. This milestone expands bare repair evidence; goal active.

## Accepted decisions and constraints
Selected whole matte sources,148 ruler/p92,172, original paid duration/cost.
No production art/controller edits. Dedicated wall-availability/interior-start
fixture; do not claim naturally selected alternate owner worksite or gear proof.
Preserve concurrent Bill/Veld work. Owner review remains pending.

## Current state
Fixtures, captured native/source boards, master-comparison.png and timed source
preview in this folder; five guides updated and four parent selections linked.
No new drawings or source states; original selection retained.

## Verification
{native['checks']} native checks0failures: East/South/West paid jobs complete once,
839work updates plus completion14seconds,5Metal each, fixed physical workpoints.
All {views['captures']} native sources/completion and8source/5native boards plus
master board reviewed.303declared source pixels covered including West stow31
exact draw0/idle0 alias. Source-only14second50Hz preview; not gameplay footage.
Nine inputs stable; all three native/profile guards pass strictly unchanged.
Geometry probes distinguish natural North selection from prescribed access.

## Next action
Ward/room repair families, other-facing Continue/interruptions/gear, real
alternate owner worksite access/incoming worker handoffs; broader master,
cross-family/furniture/rotation/owner/export polish. Full goal incomplete.
"""
atomic(P/'HANDOFF.md',handoff.encode());print(json.dumps({'checks':native['checks'],'captures':views['captures'],'sourcesCovered':views['declaredSourceReferencesPixelCovered'],'guides':len(paths)}))
