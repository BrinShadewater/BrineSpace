from pathlib import Path
import hashlib,json,os,uuid
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
def atomic(path,data):
    t=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,path)
def write(path,value):atomic(path,(json.dumps(value,indent=2)+'\n').encode())
guards={}
for name in ['validate','safety']:
    guard=json.loads((P/f'{name}-validation.json').read_bytes())
    assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged'] and guard['profileDelta']==[]
    guards[name]=guard
inputs=json.loads((P/'runtime-input-before.json').read_bytes())
after={path:hashlib.sha256((R/path).read_bytes()).hexdigest() for path in inputs}
assert inputs==after,'Relevant runtime/manifest inputs changed during final interval'
native=json.loads((P/'native-evidence.json').read_bytes());safety=json.loads((P/'safety-evidence.json').read_bytes());views=json.loads((P/'review-evidence.json').read_bytes())
assert native['failures']==0 and safety['failures']==0 and native['workSteps']==839
selection={'status':'installed_hull_lifecycle_native_verified_owner_review_pending','runtimeInstalled':True,'fullSetComplete':False,'newDrawings':0,'newSourceStates':0,
           'cleanSourceReview':{'nativeRGBAMatches':views['cleanSelectedSourceMatches'],'sourceBoard':views['cleanSourceBoard'],'preview':views['cleanPreview'],'reviewed':True,'timing':'50ms per unique selected pose; no full fourteen-second motion/lighting footage claim'},
           'native':native,'safety':safety,'profileGuards':guards,'runtimeInputHashes':after,'inputsStableDuringFinalInterval':True,
           'visualReview':'All52 final native views on two boards reviewed:45 unique normal selected North source slots, six draw/held/stow checkpoint before/after views, exact idle completion. Original matte whole poses/ruler/pivot, fixed repair foot; source clock joins do not recolor or transform body. Native water/vapor overlays change during the actual damaged-room repair independently of immutable source pixels. Not every repeated held-loop occurrence or continuous footage.',
           'clock':'Original paid progress owns draw first .52 / integer whole held cycles / stow last .52. Same repair duration and research-rate integration; derives duration cache from saved room job after fresh Continue. No added serialized state or drawings. Sparks/seam vapor only during held work.',
           'diagnostics':'First main proof passed before final unsupported-context guard; archived. First safety fixture incorrectly expected no next-tick job after cancelling serious damage. Existing auto_queue correctly pays/claims a fresh repair; fixture now checks immediate old-cache release and new source-entry reset without changing gameplay. Archived failed fixture and guard.',
           'remaining':'Smooth normal repair cancellation/interrupt choreography, actual other-facing/short-patch/research/gear contexts, broader ward/room repair families and master/furniture/rotation/owner/export polish. Full animation goal active/incomplete.'}
write(P/'selection-review.json',selection)
for relative in ['character/james-repair-contact-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    path=R/relative;data=json.loads(path.read_bytes());data['hullLifecycleReview']='res://character/james-hull-lifecycle-v1/selection-review.json';write(path,data)
block='''## James hull repair tool lifecycle — October 1, 2026

Installed whole selected torch draw/held/stow on James's ordinary dry bare hull
repair. branforth_npc.gd derives its pose/clock from existing room-paid progress:
first .52 draw, integer complete held cycles, last .52 stow. Duration cache is
rehydrated from the saved room job on Continue; no new serialized field, art or
state coverage. Original duration/research progress integration retained.
hull_repair.gd optional sync/release hooks; grid_canvas clears obsolete cosmetic
player state while the paid clock presents poses. station_effects/flood_visuals
gate sparks and seam vapor to held work. Unsupported gear/media/stage/travel
keeps old actor timer and animation. Safety guards disable stale work immediately.

Final5630native checks/0failures: prescribed four-direction clocks/seams at
3/6/10/14/16 budgets; actual normal paid rupture repair/natural North approach,
839work frames plus completion (14seconds), no extra charge, fixed work foot.
Three real disk Continues into fresh scenes during partial draw/held/stow:
exact actor/player/source/pause/room progress and derived duration.52native
views reviewed on two boards:45unique source slots, six checkpoint views and
completion. Source RGBA/ruler/p92,172 unchanged; identical final stow/idle join.
All repeated held-loop occurrences are not individually captured. GIF uses
50ms/unique pose and first occurrence, not real-time footage. Damage-driven
water/vapor varies independently of source grade and masks lower body in late
views; no body rescaling. Fixed screenshot crop486,362 throughout.

Final20safety checks/0failures: unsupported context timer preserved; actual
partial-entry cancel/flood/death, immediate death renderer. Cancellation releases
old cache immediately; next normal tick auto-queues a new paid repair for serious
damage by existing owner rule, with a fresh source entry. Initial safety fixture
mistook this for stale motion; retained failed evidence, corrected the fixture
without changing gameplay. Flood changes to existing wet repair; no dry torch.
Both final intervals engine0/no timeout/strict owner unchanged/scratch APPDATA.
Seven relevant runtime/manifest hashes stable across final full interval.

Lesson: bind source phases to the saved paid clock, fit complete held loops so
both authored joins remain exact, derive presentation caches on restoration,
and distinguish cancellation from a legitimately auto-queued replacement job.
Normal cancellation still needs smooth source-return choreography; other natural
facings/short patch/research/gear, ward/room families, owner/export and wider
consistency polish remain. Full animation goal active/incomplete.
Evidence/HANDOFF:character/james-hull-lifecycle-v1.

'''
guides=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for i,path in enumerate(guides):
    old=path.read_bytes()
    if block.splitlines()[0].encode() in old:continue
    b=block.encode();atomic(path,b+old if i==0 else old+b'\n'+b.rstrip()+b'\n')
handoff='''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James hull tool lifecycle

## Objective and acceptance
Full matching animation set and cross-family polish. Active/incomplete. Ordinary
hull lifecycle installed/native visually reviewed; owner acceptance pending.

## Accepted decisions and constraints
Matte selected whole poses,148ruler/p92,172, fixed work foot, forward torch and
belt wrench. Original repair costs/budgets/safety/gear rules; serious hull damage
automatically queues again after cancellation. Construction doorway spark target
retained. Preserve concurrent work/owner profile; native scratch APPDATA only.

## Current state
branforth_npc: derived hull duration/progress pose, integer held cycles, cache
restore from room job; optional hull_repair sync/release hooks; grid_canvas
deterministic source clock; station_effects/flood_visuals held-only effects.
No new art/state coverage/save field. New paired validate/safety fixtures and
native evidence/52views/two boards/source-order GIF. Parent selections/five
guides updated. Initial main/safety proof variants archived, no live own process.

## Verification
Final5630native checks/0failures;20safety checks/0failures. Both engine0/no timeout/
strict real profile unchanged. Seven runtime/manifest hashes stable across final
full run. Prescribed4directions and3/6/10/14/16budgets; exact joins. One real paid
North rupture job, normal approach, fixed feet,14sec work/completion once/no
extra charge; three actual fresh Continue phases exact, pause freezes source.
All52final views reviewed,45unique source slots plus six checkpoint/completion.
Later water overlays hide lower body; unchanged source proof distinguishes this
from grade/scale drift. GIF50ms/unique first pose, not continuous14sec footage.
Four unsupported contexts preserve old timer; cancel/death/flood guards work.
Cancel's next-tick new job is intended auto-queue, not stale cache. Scoped diff
whitespace check passes. Not every repeated loop occurrence/all natural facings,
short patch/research speed/gear or smooth cancellation/interrupt choreography.

## Next action
Complete smooth normal repair cancellation/source returns without delaying safety
or confusing fresh auto-queued work; actual interruption/Continue. Broaden natural
repair facings and ward/room families, then full master/gear/furniture/rotation/
owner/export consistency polish. Coverage is not full-goal completion.
'''
atomic(P/'HANDOFF.md',handoff.encode())
print('Recorded installed hull lifecycle, bounded proofs, parents and five guides.')
