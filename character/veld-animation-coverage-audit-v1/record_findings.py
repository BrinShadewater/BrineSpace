from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
path=P/'furniture-review-evidence.json';d=json.loads(path.read_text(encoding='utf-8'))
for name,digest in d['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
d['visualReview']='Both registered source boards/all48presentations inspected October2. East/West sit and East/West/North read master continuity FAILED; South and North sit rows coherent sampled. Not native or motion acceptance.'
d['findings']=['East/West exact sit-down entrance differs from selected standing master: narrower body, darker/cooler hair and suit, altered face detail.',
 'East/West seated reading uses visibly different body/head/shell from sitting and current standing masters; helmet front/visor/neck shape changes.',
 'North reading still uses original catalog body, which differs in back silhouette/material/backpack/head from selected coherent North sitting.',
 'All inspected rows declare H148 and share review registration. Differences are authored identity/material/pose, not a reason to force equal per-frame alpha heights.']
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld selected furniture master gaps — October 2, 2026

Actual normal loader/catalog resolution records192bare/186helmet final selected
state IDs from116manifest files, zero absent referenced source files. This is
static inventory, not completeness/dispatch/master acceptance. Exact override
order, slot paths and hashes saved in character/veld-animation-coverage-audit-v1.
Including original catalog matters: East/West sitting and East/West/North reading
are still selected from older dr-veld-v2 packs, despite newer North/South sitting.

All48registered source presentations/both gears/four directions reviewed at shared
H148/p128224 padding. Visual master continuity FAILED for East/West sit and
East/West/North read: narrower/darker older body, cooler hair/changed face details;
reader torso/backpack and helmet front/visor/neck differ across the join. Selected
South and North sitting retain coherent sampled bodies; South reader reviewed here
is current selected family. No artwork/controller/normal selection changed.

Lesson: selected overrides are not the whole selected library. Resolve original
catalog plus actual loader order before declaring coverage or polish complete.
Manifest presence and identical declared height do not prove authored proportions,
material identity or shared helmet continuity. Next finish staged South partial
save/motion gates, then source-author master-continuous East/West sit/read and North
reader joins, full native contact/interruptions/Continue and cross-family polish.
Full goal active/incomplete; not a new restricted definition of the requested set.
Evidence:character/veld-animation-coverage-audit-v1/SELECTED_COVERAGE.md and
furniture-review-evidence.json; HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=path.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:path.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld selected-library fidelity

## Objective and acceptance
Full Veld set, continually matched to masters, then cross-family polish.
Inventory/static source comparison identifies remaining repairs; no full acceptance.

## Accepted decisions and constraints
Current owner-approved masters/shared helmet/height/materials govern. Preserve
whole authored proportions; no per-pose height normalization. Original catalog
and later normal loader overrides jointly define selected assets.

## Current state
audit.py resolves current Veld normal catalog/load order into selected-library.json
and SELECTED_COVERAGE.md; review_furniture.py creates two registered source boards.
48source presentations inspected, hashes retained; no source or runtime mutation.
Docs/status/pipeline/bible/maintained+installed crew-life reference record findings.

## Verification
192bare/186helmet selected IDs,116manifests, zero absent source files. Static only;
not actual dispatch or full visual completeness. Both48-source boards reviewed.
East/West sitting and East/West/North reading fail master/helmet continuity.
Newer North/South sitting rows retain sampled coherent proportions/materials.

## Next action
Finish partial South running disk/future test (session34137), then native30fps
capture via already prepared tests/test_veld_sofa_partial_south_motion.gd(+uid)
and tools/run_veld_sofa_partial_south_motion.py; do not run it concurrently against
the current native fixture. Partial-family HANDOFF owns exact current live state.
Next author East/West sit/read bodies and North reader from selected masters,
review native furniture contact, all source joins/gear, interruptions/Continue.
Full-library traffic/hazards/cadence/material/perspective polish remains open.
No commit/export/full-goal completion.
''',encoding='utf-8')
print('Recorded master continuity failures and full-loader coverage in5references+handoff')
