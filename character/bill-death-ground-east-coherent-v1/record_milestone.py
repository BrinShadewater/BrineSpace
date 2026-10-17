from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'output/bill-death-ground-east-candidate-native-v1'
report=json.loads((OUT/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
assert json.loads((P/'verification.json').read_text())['passed']
summary='''Bill east bare ground-collapse candidate — October 1, 2026.
Independent built-in exec-e80aa2db-698c-41fd-81ec-09c4a7d2da89/raw/exact prompt
retained. Five authored interiors1..5 after exact selected east idle donor;
six finite slots250/300/350/400/400/300ms,2s,terminal frame5 holds,never loops.
Fixed[.31,.343] ruler from source standing size; natural lowered bodies,not
standing-height normalization. Authored knee/forearm/boot floor contacts and
local lateral collapse on256plane/pivot128,224/H148/dry0. Master matte neutral,
hair/skin/burgundy palette; circular head-local grade regions for rotated heads.
20 source checks PASS;37 native checks PASS13.46s,explicit scratch profile,
2,920 owner non-log files unchanged for this interval. Native148/82/idle reviewed.
Crown progression76/94/133/169/183/184. Final1px settlement is authored lowering,
not an upright loop's constant-height invariant; cadence/detail/terminal contact
and full-set identity polish remain. Hash-bound independent east/west comparison
reviewed,5 shared plane/timing checks pass; physical anatomy/detail differences
remain for full-set polish. Exact loaded pixels,pacing,dry metadata,
preserved helmet source and finite corpse hold proven. Candidate only,not
selected normal mortality behavior,room clearance/interruption/Continue proof.
Next other dry-death directions and paired canonical helmets,then actual mortality
and restore/clearance; generic rest sources and unfinished meal/inspection runtime
proof/full-set polish remain. Bill's furniture-specific bunk is intentionally
east-only; do not generate unused cardinal bunk variants to satisfy a coverage count.
Lesson: use physical source floor-contact registration for collapse and let body
height lower; constant crown tests belong to upright loops,not authored falls.
Full goal active; no actor/reward/geometry/normal selection/commit/export changes.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · BrineSpace · Bill east ground-collapse candidate

## Objective and acceptance
Complete Bill's master-consistent full animation set, then cross-animation polish.
East bare ground death source packaged; paired/full directional runtime acceptance open.

## Accepted decisions and constraints
Selected east master identity, matte finish, camera and physical density.
Independent full figures; exact idle entry; natural body lowering and finite corpse.
Existing reversible work authorized; source/prompt retained; scratch profiles only.

## Current state
'''+summary+'''
## Verification
20 package/37 native checks pass. Full-size/game-scale visual review completed.
No normal mortality route or saved corpse restoration demonstrated by this fixture.
Earlier meal profile guard failures remain historical failures; this clean interval
does not retroactively certify those runs.

## Next action
Author remaining cardinal dry-ground collapse sources and canonical helmet versions;
assemble paired family and prove actual mortality, collision clearance and Continue.
Keep generic rest, meal/inspection runtime and full-set polish on the open scope.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[f for f in P.iterdir() if f.is_file() and f.name!='candidate-evidence.json']+list((P/'sources').glob('*'))+list((P/'frames/death-ground-east').glob('*.png'))+[OUT/'validation.json',OUT/'native.log',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_death_ground_east_candidates.gd',ROOT/'tools/run_bill_death_ground_east_candidate_validation.py']
evidence={'status':'staged_candidate','checks':{'package':20,'native':37},'native':report,'scope':'east bare dry collapse candidate source/native/terminal hold; paired family/actual mortality/restore/full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file()}}
(P/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
heading='## Bill east ground-collapse candidate — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/relative).open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-east-coherent-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded east dry collapse candidate, visual/native scope and full remaining objective')
