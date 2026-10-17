from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
reports={}
for d in ['east','west']:
 p=P.parent/f'bill-death-ground-helmet-{d}-coherent-v1';out=ROOT/f'output/bill-death-ground-helmet-{d}-candidate-native-v1'
 r=json.loads((out/'validation.json').read_text());v=json.loads((p/'verification.json').read_text());assert r['passed'] and v['passed'] and not r['realProfileChanges'];reports[d]=r
summary=f'''Bill east/west canonical-helmet dry-collapse candidates — October 1, 2026.
Two native dry components copied from selected seated helmet packs; fixed scale1,
no fresh anatomy generation or material changes. Five neck positions/head tilts
fit over each independently authored bare fall; west not a mirror of east.
Exact equipped selected standing entries; paired six-slot2s250/300/350/400/400/300ms
clock and held terminal5.256plane/pivot128,224/H148/dry0 unchanged.
East source necks772,216/1291,326/340,820/873,870/1387,870, tilts20/35/35/90/90;
west712,238/1206,322/165,812/632,876/1146,878, tilts-20/-30/-35/-90/-90.
Frozen component neck anchors19,29east/16,29west. Head-local warm erasure;
every pixel outside declared head/equipment region matches paired bare body.
34 package checks each PASS;38 native checks each PASS:
east{reports['east']['seconds']}s/west{reports['west']['seconds']}s, explicit scratch profiles,
2,920 owner non-log files unchanged in each interval. Native148/82/idle and
paired helmet/bare sheets reviewed. Collar/shoulder/terminal floor contact,
fine identity/detail/cadence remain visual polish; selected face stays unchanged,
no separately authored final expression. Native loaded pixels/metadata/timing
and finite corpse hold demonstrated, not actual kill/clearance/Continue.
Initial east fixture incorrectly loaded gear as bare, then gear loader rejected
old base timing/pivot. Those failed runs retained. Corrected fixture explicitly
loads paired bare candidate first and checks load_equipment_manifest return;
matching frame counts, timing, pivots and standing density are prerequisites.
Do not infer equipment selection from a manifest's root equipment label or from
unchanged legacy gear frames. No loader/controller or normal selection change.
Next north/south helmet perspective, paired cardinal family and actual mortality
restoration/clearance. Axial lying equipment needs camera projection review;
do not blindly rotate an upright rear/front shell as if it were a side profile.
Generic rest, meal/inspection runtime and full-set consistency/polish remain open.
Full objective active; no owner art acceptance, commit or export claim.
'''
for d in ['east','west']:
 p=P.parent/f'bill-death-ground-helmet-{d}-coherent-v1';out=ROOT/f'output/bill-death-ground-helmet-{d}-candidate-native-v1'
 handoff=f'''# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Bill {d} helmet dry collapse

## Objective and acceptance
Complete Bill's master-consistent full animation set, then cross-animation polish.
This paired direction is a staged candidate. Actual mortality/owner acceptance open.

## Accepted decisions and constraints
Native accepted dry helmet identity/material/scale; independently authored bare
body; exact idle entry; finite corpse hold; scratch profiles and source preservation.

## Current state
'''+summary+f'''
Changed package build/prepare/verify, canonical component, six frames, manifest,
helmet registration/hashes/review sheet/index/evidence. Native fixture
tests/test_bill_death_ground_helmet_{d}_candidates.gd (+paired UID),
runner tools/run_bill_death_ground_helmet_{d}_candidate_validation.py.

## Verification
34 package and38 native checks pass for this direction. Native full/game scale
and paired art reviewed; raster LFS attributes verified. Body invariance excludes
declared head/equipment region; tests cannot certify anatomical collar joins.

## Next action
North/south helmet projections, paired family and actual kill/held corpse/Continue
and floor clearance; then remaining rest/meal/inspection and full-set polish.
'''
 (p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
 paths=list(p.glob('*.*'))+list((p/'sources').glob('*'))+list((p/f'frames/death-ground-{d}').glob('*.png'))+[out/'validation.json',out/'native.log',out/'loaded-water-carry.png',ROOT/f'tests/test_bill_death_ground_helmet_{d}_candidates.gd',ROOT/f'tests/test_bill_death_ground_helmet_{d}_candidates.gd.uid',ROOT/f'tools/run_bill_death_ground_helmet_{d}_candidate_validation.py']
 e={'status':'staged_candidate','packageChecks':34,'nativeChecks':38,'native':reports[d],'scope':'native canonical helmet registration, exact body outside head/gear region, finite metadata; art/actual mortality/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file() and f.name!='candidate-evidence.json'}}
 (p/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill east/west helmet dry-collapse candidates — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/relative).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoffs: character/bill-death-ground-helmet-east-coherent-v1/HANDOFF.md and west counterpart.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded two paired helmet candidates, loader compatibility lesson and remaining scope')
