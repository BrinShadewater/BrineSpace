from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'review.json').read_text(encoding='utf-8'))
assert e['validation']['passed'] and not e['targetedChanges']
assert e['decodedCaptureIntervals']==380 and len(e['nativeGuardPresentations'])==28
assert e['frozenInputCount']==522
e['visualReview']='Four complete advancing boards and28synthetic active/takeover native/source pairs reviewed. Independently drawn West exit rises through elbow/palm/knee/half-kneel/standing stages, canonical helmet collar remains connected in captured poses. Wet material decreases through exit and exact target walking phase replaces final source. Palette/detail/face differences at normal gait boundaries and continuous full-speed motion/physical contact remain pending; screenshot boards do not establish full temporal quality.'
e['visualAcceptance']='Native source-phase/material/clearance/guards passed and captured source/native poses reviewed. Full master consistency and motion acceptance pending.'
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note=f'''## Bill West independent entry/exit moving native milestone — October 2, 2026

New staged bill-land-water-material-west-v3 binds current WestV4 entry and newly
authored bill-water-exit-west-v1 bare/helmet banks. Both finite500ms bridges now
use actual normal Bill movement, medium/oxygen/safety/navigation, exact actual
outgoing/incoming gait phases, union loaded-alpha planar clearance admission and
every-update recheck, final gait rebind. Exit source is independently articulated,
not reversed entrance or mirrored East. Five new exit head anchors131172/130160/
133150/147120/15792; per-instance material weight decreases1→0 with source-bound
head/wake position while exiting. Current-main fixture only swaps GridCanvas;
explicit exact main/grid path assertions and28decoded loaded frame comparisons
prevent old fixture/bank evidence being attributed to new artwork.

Initial3735-check interval passed native mechanics but strict inventory audit
found four facing-takeover sources absent from172-input prelaunch freeze: active
swim-turn/start poses and East walking. Logs/records/inventory and all28guard
pairs retained as incomplete-inventory diagnostic, not complete source-stability
proof. Current manifest inventory expanded before rerun; prior guard pixels all
identified exactly without a historical fallback.

Fresh {e['checks']}native checks0fail/engine0/{e['validation']['seconds']}s, scratch APPDATA;
all{e['validation']['realProfileFileCount']}owner non-log files unchanged.522targeted inputs stable,
including four new bank manifests/28PNGs and current normal bare/helmet West walk,
West/East swim banks, start/stop/turn clips and loaded East walking used by
actual route and facing guards.20manifest inventory
contains312distinct decoded sources. Every advancing and guard source identifies
against exact captured RGBA and manifest pivot/height/size, no historical fallback
or guessed profile. Freeze covers this source scope/targeted code, not every
normal Bill family or transitive project dependency.

600ticks60Hz per gear on graph-validated route and prescribed10s water rise/hold/
drain; actor remains authoritative. Both entry/exit admitted and completed with
exact incoming gait textures.190advancing paired captures across four full boards,
380source-room files;8APNGs verify380decoded advancing intervals.28synthetic
active/takeover pairs across both phases/gears: gear/facing/death/stage/clock/
geometry cancel same tick and actual retained draw clears bridge material.
All guard source RGBA matches current frozen inventory.218pairs/436files retained.
Four advancing boards and complete guard board inspected: exit stages/readability
and canonical helmet collar coherent in captured poses, wet material decays and
walking source resumes. Source/native screenshot review does not establish
continuous temporal quality, actual floor contact or complete master consistency.
Normal endpoint material/detail/face differences and full-speed motion still open.

Normal production controller/source selection/save code unchanged. New source
review records this specific native proof; previous entry-only evidence retained.
No current-bank checkpoints/titleContinue, natural job/hydrology or normal source
admission. Builders, unique paired UIDs, stronger two-phase test, isolated runner,
frozen decoded inventory/captures/review media saved. Review:
character/bill-land-water-material-west-v3/index.html. Handoff same folder.
Full Bill goal active/incomplete; North/South bridges, cargo lifecycle and entire
cross-family master/style/perspective/size/anatomy/matte-grade polish remain.

Lesson: entry guard evidence does not transfer to independently authored exit.
Exercise active exit clocks too, label captures by phase to avoid overwriting
entry evidence. Facing takeover can expose an active start/turn clip before the
new facing loop; actor state/direction alone does not name actual shown artwork.
Freeze those transition and walking sources too, and resolve normal registration from exact decoded
pixels/manifest data. Freeze normal boundary and facing-takeover sources before
launch; a new bank path or green scene test alone does not prove loaded art.
Next uninterrupted source/native motion and full master/endpoint matching, current
entry/exit fresh-scene/disk/titleContinue proof and guarded production admission.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    p=R/rel;t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=p.read_text(encoding='utf-8')
    if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
source=P.parent/'bill-water-exit-west-v1/review.json';s=json.loads(source.read_text(encoding='utf-8'))
s['nativeProof']=dict(review='../bill-land-water-material-west-v3/index.html',checks=e['checks'],failures=0,scope='Correct current scene/renderer and all28entry/exit source pixels; actual movement/source-phase/finite material/clearance and both-phase synthetic guards. Full motion/master/contact and checkpoints/Continue pending.')
source.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West independent entry/exit native

## Objective and acceptance
Full Bill set matching original masters/style/perspective/scale/proportions/matte
grade, then full cross-family polish. This staged milestone leaves goal open.

## Accepted decisions and constraints
Actual normal actor controls movement/medium/safety. Fixture-only visual bridges,
WestV4 entry and independently authored West exit V1, no mirror/reversal.
Common native density/pivots, canonical helmet. Preserve accepted work and owner
data; all Godot validation scratch APPDATA, full owner fingerprint before/after.

## Current state
New material-west-v3 grid/view/current main fixture/unique UIDs, test/runner,
four source banks and current normal gait decoded inventory frozen. Four complete
advancing boards/8APNGs/28guard board pairs,218source-room capture pairs total.
Six guidance files and exit source review updated; production selections unchanged.

## Verification
{e['checks']}native checks0fail/engine0/{e['validation']['seconds']}s;
{e['validation']['realProfileFileCount']}owner non-log files unchanged,522inputs stable.
Current scene/main/grid and28loaded source pixels checked. Both500ms bridges
complete on exact actual incoming gait.190advancing plus28guard pairs sources
exact to frozen inventory;380APNG intervals verified. Four advancing boards and
all28guards reviewed. Full motion/master/contact acceptance still open.

## Next action
Continuous motion and endpoint/master comparison; current-bank fresh scene,
disk/checkpoint/titleContinue; guarded normal admission. North/South bridges,
cargo lifecycle and full Bill cross-family fidelity/polish remain.
''',encoding='utf-8')
print('Recorded actual West independent entry/exit native evidence, source scope and remaining acceptance in six guidance files.')
