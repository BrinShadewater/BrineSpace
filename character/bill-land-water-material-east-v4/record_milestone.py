from pathlib import Path
import json
P=Path(__file__).resolve().parent; R=P.parent.parent
f=P/'review.json'; e=json.loads(f.read_text(encoding='utf-8')); assert e['checks']==3487 and not e['targetedChanges']
e['guardVisualReview']='All14 native/source synthetic active/takeover snapshots inspected. Material clears on source takeover; raw source thumbnails are not common-pivot registered. Death flag snapshot does not prove completed death action.'
f.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill East articulated water lift and native review — October 2, 2026

New unselected source V5 inserts one authored lift between registered crouch and
first buoyant pose, paired bare/helmet. Twelve original poses remain RGBA exact;
seven poses per gear retain500ms total, splitting prior100ms crouch hold50+50.
Common320canvas/p160,224/H148; no per-pose body-height fit. Crown gap66px now33+33.
Canonical native helmet fitted scale1/rotation0, explicit head region only;
body outside region and foreground arm/shoulder preserved. Fourteen decoded
source APNG frames exact. Raw sources, prompts and two rejected oversized drafts
retained. New generation exec-717e0171-0783-4e10-9f6b-4de5c5b98f84.

Canvas-relative neighbor edit succeeded where numeric portrait layout requests
produced oversized heads. Actual generated canvas1254 vs requested1280 normalized
as a complete canvas320/1254 with whole-pose translation(-2,-1). Conditioned on
already graded neighbors/master: do not reapply unrelated old raw-source curve.
Source master/lift detail boards inspected; matte face/suit/helmet coherent for
this candidate, full-family acceptance remains pending.

Staged material East V4 selects V5 entries with five explicit head anchors;
separate exits unchanged. Per-instance actual-source draw binding,500ms material
blend, physical actor/navigation/collision/phase/cancellation rules retained.
3487 native checks0fail/engine0/125.38s;2931owner files unchanged using scratch
APPDATA. All13targeted pre/post input hashes stable.190 advancing paired source/
native presentations inspected in four full boards;14synthetic guard pairs also
inspected.204pairs/408files,8APNGs/380decoded advancing intervals retained.
New lift reduces captured pose gap; colour and helmet remain coherent. Guard
material clears to normal source on takeover. Synthetic death/stage snapshots
are not natural death completion or priority dispatch; raw guard thumbnails are
not common-pivot registered. Continuous unpaused motion and physical floor/
buoyancy support remain unproven. Older checkpoint/Title proofs cover older bank;
new source-bank Continue is pending. No normal admission or commit/export.

Next: review actual continuous contact/material motion and current-bank checkpoint
restoration, then guarded normal integration and other cardinal transitions.
Cargo lifecycle and full Bill master/style/perspective/proportion/grade cross-
family polish remain. Full objective active/incomplete.
Review:character/bill-land-water-material-east-v4/index.html.
Handoff:character/bill-land-water-material-east-v4/HANDOFF.md.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel; t=p.read_text(encoding='utf-8')
 if heading not in t: p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t: p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill East water lift

## Objective and acceptance
Full master-consistent Bill set, followed by cross-family consistency and polish.
This staged East candidate leaves the full goal active.

## Accepted decisions and constraints
Preserve master anatomy/matte detail, common canvas and canonical helmet. Use
neighbor canvas edits for new articulated poses; never scale body per bounding box.
Preserve owner saves and concurrent crew work. New banks require new Continue proof.

## Current state
Source bill-land-water-east-v5/build.py, bare/helmet manifests/frames, retained raw
sources/prompts/rejections and master/detail boards. Native material-east-v4 grid,
view, copied fixture, paired UIDs, prepare/build/finalize/record scripts, native
test and scratch runner,204capture pairs/four boards/guard board/eight APNGs.
Status, continuation, pipeline, bible and both skill references updated.

## Verification
12original poses exact;14decoded source frames/500ms each gear.3487native checks,
0fail/engine0/125.38s;2931owner files unchanged.13targeted hashes stable.190native/
source advancing presentations and14synthetic guard pairs visually inspected.
380advancing APNG intervals verified. Source grade/helmet coherent; floor support
and continuous unpaused motion not accepted. No current-bank Continue proof.

## Next action
Actual continuous contact/material motion and new-bank checkpoint restoration;
then guarded normal integration and other cardinal transitions. Cargo lifecycle
and full cross-family master/style/proportion/grade polish remain. No commit/export.
''',encoding='utf-8')
print('Recorded source and native review milestone in six guidance files and handoff.')
