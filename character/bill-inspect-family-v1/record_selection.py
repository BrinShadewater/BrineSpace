from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
ROOT=P.parent.parent
OUT=ROOT/'output/bill-inspection-selected-renderer-v1'
v=json.loads((P/'verification.json').read_text())
n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '1036 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill normally selected cardinal inspection

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
This milestone proves normal art selection, not actual draw/stow activity integration.

## Accepted decisions and constraints
24 states/144 source references across four directions and both gear states.
Shared256 plane/pivot128,224/H148/dry depth0; native master helmets and matte grading.
Draw/stow480ms each, inspection960ms loop. Exact idle/held joins and reversed stow.
Keep existing service durations and isolate future behavior changes to Bill.

## Current state
grid_canvas.gd normally loads both family manifests; ACTIVE_ASSETS.json records
bare and equipment overrides. Existing inspect consumers select the new loops.
Source candidate packages preserve all generation provenance. No actor changes
in this milestone; enter/exit actions load but are not yet chosen by activities.
Interactive index.html previews draw/two inspection cycles/stow;2.88s preview only.

## Verification
80 source binding/timing/metadata checks and1,036 normal native renderer checks
pass. All144 loaded references match source pixels; finite timing, loop repeat,
exact held joins and registered idle joins pass. Native82 board visually reviewed.
Idle184 canvases/pivot92,172 and action256 canvases/pivot128,224 have identical
pixels on the common pivot plane; failed raw-buffer comparisons and the diagnostic
probe are preserved in output runner archives. No artwork change for this test fix.
Scratch APPDATA; all2,914 owner non-log files unchanged. Native run10.90seconds.
Actual activity transitions, interruptions, disk restore and clearance remain unproved.

## Next action
Integrate Bill draw/inspect/stow into cold-store life_inspect, workshop inspection
and equipped eat/drink mapping, preserving clocks and snapshot/cleanup behavior.
Prove actual activity, interruption, disk restore and world clearance separately.
Then meals, generic rest/dry death and full-set material/proportion/pacing polish.
Remaining2–3px interior motion variation is reserved for final polish. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill cardinal inspection normally selected — September30,2026.
Normal grid loader/ACTIVE_ASSETS now select24states/144refs across four directions
and both gear states.80 source checks and1,036 native normal selection checks pass;
exact loaded pixels, dry metadata, finite timing/loop repeat and idle/held joins.
Native82 frame board reviewed; scratch APPDATA preserved2,914 owner non-log files.
Idle184/pivot92,172 and action256/pivot128,224 must be compared on a shared pivot
plane at equalH148, not by raw differently sized buffers. Diagnostic and failed
runs retained. No art change required for this fixture correction.
Existing inspect consumers get new loops; draw/stow actions are loaded but actual
activity phase selection remains pending. No BillNPC/CrewLife behavior changes.
Next actual cold-store/workshop/equipped meal activity transitions, interruption,
disk restore and world clearance; then meals, generic rest/dry death/full polish.
Full goal active. Handoff: character/bill-inspect-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md'
status.write_bytes(('## Bill cardinal inspection normally selected — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','bare-manifest.json','helmet-manifest.json','verification.json','HANDOFF.md','index.html']]+[ROOT/'scripts/grid_canvas.gd',ROOT/'character/ACTIVE_ASSETS.json',ROOT/'tests/test_bill_inspection_selected_renderer.gd',ROOT/'tools/run_bill_inspection_selected_renderer_validation.py',OUT/'validation.json',OUT/'loaded-water-carry.png']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'selected_runtime','checks':{'package':80,'native':1036},'states':24,'refs':144,'native':n,'scope':'normally selected source pixels/timing/joins and native visual review; actual draw/stow activity/interruption/restore/clearance pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded normal inspection selection; actual activity integration remains pending')
