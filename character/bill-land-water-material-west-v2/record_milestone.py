from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;SOURCE=P.parent/'bill-land-water-west-v4'
f=P/'review.json';e=json.loads(f.read_text(encoding='utf-8'));assert e['validation']['passed'] and e['checks']>=3051 and not e['targetedChanges']
e['visualReview']='Both full advancing entry boards and fourteen native/source guard pairs inspected. New V4 quilt/detail poses remain readable and helmet/head connected at captured station scale. Progressive wet material, dynamic walking/swimming endpoints and same-tick cancellation retained. All five interior fabric/badge edits closer to original master; normal walking/swim endpoint materials, face identity, metal brightness, shape changes and continuous unpaused motion still need complete consistency acceptance. No independently authored West exit or current-bank checkpoints/Continue.'
e['guardVisualReview']='All14synthetic active/takeover pairs inspected; current source binding clears material on gear/facing/death/stage/clock/geometry. Not natural priority/death completion.'
e['visualAcceptance']='Source material/detail pass improved; native technical entry proof passed. Full identity/material and continuous motion acceptance pending.'
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
sf=SOURCE/'review.json';se=json.loads(sf.read_text(encoding='utf-8'))
se['nativeProof']={'review':'../bill-land-water-material-west-v2/index.html','checks':e['checks'],'failures':0,'scope':'Corrected current fixture main/grid binding and exact fourteen loaded source pixels; moving entry/guards/material/clearance, two gears. Full identity/material/continuous motion, West exit/checkpoint/Continue remain pending.'}
sf.write_text(json.dumps(se,indent=2)+'\n',encoding='utf-8')

note=f'''## Bill West full intermediate detail pass and native revision — October 2, 2026

New unselected bill-land-water-west-v4 finishes original-master material/detail
edits across five entry intermediates. Adds arm-ready-v5/lift-v3/prone-v2 raw
sources/prompts, retaining V3crouch/push. Built-in generations:
exec-0ac37457-b3ca-4e3a-b738-d2381ffe8d73,
exec-051b3767-1a8c-4a58-a35c-7c5617a00781,
exec-9770dcdd-1880-4aeb-b070-aad43b96382f.
First arm detail draft exec-e1be26fb-33f9-431f-92a3-0f1c4ce10f94 rejected for
lower recentering/shortened build. Two-reference retry retains original standing
composition more closely. Raw/prompts/rejected candidate/hashes preserved in V1.

All actual1254square→320wholecanvas; arm sole223→224 wholeY+1, lift whole(-1,-14)
to crown130150, near-prone whole(+1,+1)to131188. Painted support preserved; no
per-pose anatomical fitting. Opaque180 silhouette IoU against V3:arm0.941547,
lift0.952082,prone0.882185 diagnostics, not anatomy acceptance. Face/hair and
minor silhouette changes generated despite material-only prompt. Common original
master148/full V3-V4 board/three native4x texture crops/all paired necks reviewed.
Quilting, square/ring badges and worn fittings closer to original master. Metals,
near-prone shape, head identity and normal endpoint materials remain polish.

Seven bare/helmet poses500ms,14decoded APNGframes/holds exact;8other V3paired
poses exact. Canonical West40x40helmet native scale1/rotation0, five explicit
anchors15779/148114/140117/130150/131188 and body/foreground protections. Seven
alpha160silhouettes connected; connectivity is not anatomical motion acceptance.

Initial scene accidentally referenced the old V1 fixture; its2987-check interval
proved the old bank and is archived, not V4 proof. Corrected scene link and
rebuild preparation; explicit current main/grid binding and decoded14loaded frame
checks prevent recurrence. Publisher identified mismatch by actual captured RGBA.
Historical normal inventory supplemented by current selected West walk manifests;
walking pixels match captures exactly, but normal bank was not prelaunch frozen.

New staged material-west-v2 binds V4 bank/anchors/current main fixture. Fresh
{e['checks']}native checks0fail/engine0/{e['validation']['seconds']}s; scratch APPDATA, all{e['validation']['realProfileFileCount']}owner
non-log files unchanged, all27targeted inputs stable. Dynamic actual outgoing/
incoming phases, union silhouette planar collision checks/rechecks,500ms material
and exact final gait source verified both gears. Actual normal Bill actor needs/
oxygen/navigation through prescribed10s room rise/hold/drain and graph route.
90advancing paired source/native captures in two full boards and14synthetic guard
pairs inspected;104pairs/208files,4APNGs/180decoded advancing intervals retained.
Wet rendering remains readable; does not certify palette/detail or uninterrupted
motion. No authored West exit, checkpoint/Continue/natural hydrology/jobs or normal
source admission. V2source/native historical proof retained; no global save writes.

Source/runtime builders, unique paired UIDs, tests/scratch runner and review media
saved. Review:character/bill-land-water-material-west-v2/index.html and
character/bill-land-water-west-v4/index.html. Full goal active/incomplete.
Lesson: a material-reference pose can pull an edit into its own canvas location;
retry exact original target+master without unrelated pose, verify common ruler.
Source texture/detail improvements need new actual loaded-bank native proof;
older green checks do not transfer. Scene preload identity and actual decoded
loaded frames must be asserted; a test named for a revision can run old art.
Review inventories must follow current selected sources, exact RGBA matches and
manifest metadata; do not guess pivots or imply whole-bank freeze coverage.
UI builders explicitly read/write UTF-8.
Next uninterrupted source/native motion and full endpoint/master consistency,
independently authored West exit/checkpoint/Continue, North/South transitions,
remaining cargo lifecycle and complete Bill cross-family style/perspective/
size/height/proportion/colour polish.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
handoff=f'''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West complete intermediate detail pass

## Objective and acceptance
Full Bill set matching masters/style/perspective/size/anatomy/matte grade, then
cross-family polish. This staged entry milestone leaves full goal incomplete.

## Accepted decisions and constraints
Original right master figure faces left. Common148 ruler/320p160224; wholecanvas
scale/contact or crown translations, no per-pose size fitting. Native helmet.
Preserve original source/runtime proofs/concurrent crew work; scratch APPDATA.

## Current state
Source WestV4 adds arm-ready/lift/prone master materials, retains V3crouch/push.
Raw/prompts/rejected arm draft V1; source builder/helmet/provenance/master/detail/
neck boards and paired player. Runtime materialWestV2/current-main fixture/grid/
view/unique UIDs/test/scratch runner,104capture pairs/two boards/guards/four APNGs.
Six guidance files updated. Normal actors/renderer/selection/save code unchanged.

## Verification
8paired V3poses exact;14decoded source frames500ms.5helmet fits protected,7connected
silhouettes. Shared master/texture/neck source boards reviewed.{e['checks']}native0fail/
engine0/{e['validation']['seconds']}s;{e['validation']['realProfileFileCount']}owner files unchanged/27inputs stable.
90advancing plus14guard pairs reviewed;180decoded advancing capture intervals.
Native technical source-phase/material/clearance proof passed; full identity/
endpoint material, metal brightness/shape changes and continuous motion remain.
No new bank checkpoints/Continue, authored exit or normal admission.

## Next action
Continuous motion/endpoint consistency, independent West exit/current checkpoints/
Continue. North/South transitions/cargo lifecycle/full Bill fidelity/polish remain.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(SOURCE/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Recorded full intermediate detail pass/current-bank native evidence and open scope; six guidance files updated.')
