from pathlib import Path
import json, hashlib, os, uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(p,data):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,p)
def write(p,obj):atomic(p,(json.dumps(obj,indent=2)+'\n').encode('utf-8'))
before=json.loads((P/'runtime-input-before.json').read_bytes())
after={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in before}
assert before==after, 'Frozen runtime/source inputs changed; inspect before recording.'
write(P/'runtime-input-after.json',after)
guards={n:json.loads((P/(n+'-validation.json')).read_bytes()) for n in ['validate','pause','hull_regression','bill_compat']}
assert all(g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and not g['profileDelta'] for g in guards.values())
assert 'WARD REPAIR: PASS' in (P/'bill_compat.log').read_text(encoding='utf-8')
main=json.loads((P/'native-evidence.json').read_bytes());pause=json.loads((P/'pause-evidence.json').read_bytes());hull=json.loads((P/'hull-regression-evidence.json').read_bytes());review=json.loads((P/'review-evidence.json').read_bytes())
assert main['failures']==pause['failures']==hull['failures']==0
review['visualReview']={'nativeBoardsReviewed':2,'sourceBoardsReviewed':2,'masterComparisonReviewed':True,'assessment':'Original matte sources retain stable body height and planted foot; draw/stow endpoints match standing master. Native work/return/reentry poses visible at correct viewport crops. Original flame/sparks only during held work. Owner review pending.'}
write(P/'review-evidence.json',review)
selection={'status':'installed_ward_lifecycle_native_reviewed_owner_review_pending','runtimeChanged':True,'sourcesChanged':False,'newDrawings':0,'newSourceStates':0,'fullSetComplete':False,'productionFiles':list(before)[:-1],'native':{k:v for k,v in main.items() if k!='records'},'pause':{k:v for k,v in pause.items() if k!='records'},'hullCompatibility':hull,'billCompatibility':'Original tests/test_ward_repair.gd passes unchanged through isolated wrapper. No James hook required by Bill.','freshDiskContinues':5,'review':'review-evidence.json','runtimeInputsBefore':'runtime-input-before.json','runtimeInputsAfter':'runtime-input-after.json','guards':guards,'archive':'before-release-guard-and-camera-fix','scope':'North dry bare James, normal paid18-second/8Metal cryo ward completion through genuine navigation and work in dedicated free-placed access fixture; normal toggle pause/resume and fresh scene disk restoration. No other gear/facing/companion ward/power/door/critical flood/incoming-worker or naturally selected owner-layout acceptance. Source-only paid-clock preview, not continuous gameplay footage.'}
write(P/'selection-review.json',selection)
for relative in ['character/james-hull-lifecycle-v1/selection-review.json','character/james-hull-return-v1/selection-review.json','character/james-hull-reassign-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    p=R/relative;obj=json.loads(p.read_bytes());obj['wardLifecycleReview']='character/james-ward-lifecycle-v1/selection-review.json';write(p,obj)
note='''## James installed ward lifecycle and retained-progress pause — October 1, 2026

James's dry bare derelict ward repair now uses the original matte whole-source
draw/held/stow phases on the existing paid18-second clock, with complete held
cycles. Original8Metal cost, navigation, crew work and recovered cryo ward reward
are retained. Normal pause returns the current source to neutral; resume enters
the exact retained paid pose before work advances. No new drawings/source states.

character/james-ward-lifecycle-v1:6568 native lifecycle checks/52 captures and
271 pause/reentry checks/27 captures, all0failures; three lifecycle plus two
return/reentry real disk fresh-scene Continues match source/player/clock/progress.
Hull recipe/source/snapshot compatibility720 checks/180 prescribed samples passes;
original Bill ward test passes. Four final guards engine0/no timeout and strict
owner profile unchanged; seven runtime/source hashes stable across final runs.
All79 native/source captures on two boards each and same148/p92,172 North master
comparison reviewed: stable body height, original matte palette and physical foot.
ward-paid-clock.gif reconstructs18-second source clock at50Hz plus neutral hold;
it is source-only, not continuous gameplay effects footage. Owner review pending.

Lessons: derive the ward animation cache from saved active ward/site progress.
Transient worker re-claim must preserve the saved entry paid clock. A newly
prepared return owns the release update, avoiding the generic idle timer decrement
that made the snapshot invalid. Shared entry recipes record owning goal/family;
legacy hull recipes retain their default. Do not relax snapshot admission.
First green lifecycle screenshots were offscreen and archived, not visually
accepted. Record viewport feet per view: award camera recentering differs from
physical foot/height drift. No per-pose rescale or colour repaint was used.

Scope: genuine North paid ward job in dedicated free-placed access rooms; no
other-facing/gear/companion-kind/power/door/critical-flood/incoming-worker or natural
owner-layout acceptance. Remaining room/electrical repair contexts, broader
master/cross-family/furniture/rotation/owner/export polish; full goal incomplete.

'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,p in enumerate(guides):
    data=p.read_bytes();assert note.splitlines()[0].encode() not in data
    atomic(p,note.encode('utf-8')+data if i==0 else data+b'\n'+note.encode('utf-8'))
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James ward lifecycle

## Objective and acceptance
Full James animation set and master/style/height/grade consistency, then wider
cross-family polish. Ward lifecycle milestone installed; broader goal incomplete.

## Accepted decisions and constraints
Original whole matte sources,148 ruler/p92,172; paid18seconds/8Metal retained.
North dry bare dedicated normal worksite fixture. Owner review pending.
Preserve concurrent Bill/Veld work and owner save/layouts.

## Current state
Six production files: branforth_npc, ward_repair, james_hull_resume,
james_hull_return, station_effects, grid_canvas. Derived ward paid clock;
whole-source draw/held/stow and return/reentry. No new art/source states.
Evidence, source-only timed preview and boards here; five guides and four parent
selections linked. Initial invalid return/offscreen screenshots archived.

## Verification
6568 lifecycle +271 pause checks0failures,79 native/source captures reviewed;
5 real disk fresh-scene Continues. Hull prescribed compatibility720/180 samples
and original Bill ward test pass. Four final guards engine0/no timeout and strict
owner profile unchanged; seven input hashes stable. Master comparison reviewed.
18-second50Hz preview reconstructs source clock; not gameplay lighting footage.

## Next action
Other ward facings/gear/companion types, power/door/critical flood/incoming worker
contexts; electrical room repair; broader master/cross-family/furniture/rotation,
owner visual acceptance and export. Keep goal active.
'''
atomic(P/'HANDOFF.md',handoff.encode('utf-8'))
print(json.dumps({'guidesUpdated':5,'parentSelectionsLinked':4,'nativeCapturesReviewed':79,'freshContinues':5,'inputHashesStable':len(before),'finalGuards':len(guards)}))
