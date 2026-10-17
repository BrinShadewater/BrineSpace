from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
path=P/'continue-review-evidence.json';d=json.loads(path.read_text(encoding='utf-8'))
for name,digest in d['bindings'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
d['visualReview']='All4boards/72source-native pairs inspected October2;24before/after room/source/contact pairs retain displayed appearance at sampled save clocks. Continuous motion/normal admission pending.'
path.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
block='''## Veld South partial sofa ordinary Continue — October 2, 2026

Staged paired six-pose fall family passes79775checks0fail/895.7s/engine0:
24actual world mortality cases/all6partial poses/both sit and rise/both gears,
ordinary RunSave disk writes/reads/fresh-main restores and7200reference/resumed
future20msactor ticks. Independent source clock, fractional seat release/floor
depth, source/foot/gear/needs/recipe and paused-source checks retain exact future.
All4boards/72source-native pairs reviewed; displayed before/after source/contact
retained.84targeted inputs and2931owner non-log files unchanged with scratch APPDATA.
Fresh scene explicitly injects candidate; not normal partial selection or Title/
new-process/natural chooser/traffic/hazard proof. Normal reader/bunk/North retained.

All24native30fpsmotion captures now running after corrected fixture-only duplicate
variable declaration. Initial3.05sparse failure/unchanged owner profile retained;
not an artwork/controller regression. Full1176frame playback review and guarded
paired normal admission pending. Full goal active/incomplete. Source master gaps
in older East/West sit and East/West/North read remain. Earlier staged East pair
found; compare current candidates before authoring more. New unselected built-in
East raw study/refs/prompt/one148/494ruler extracted and reviewed beside both old
selected and earlier staged poses; face/proportion/grade/gear/motion not admitted.

Lesson: prove partial contact through ordinary world checkpoint/future, not merely
actor-file snapshots. Original catalog, selected overrides and staged candidates
are separate evidence inventories; missing override does not mean missing source.
Next inspect30fpsnative motion/joins, normal paired admission and remaining full
cardinal/context/master polish. Evidence:character/veld-sofa-partial-fall-south-v1/
continue-review-evidence.json; HANDOFF.md. No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=path.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:path.write_text(block+old,encoding='utf-8')
handoff=P/'HANDOFF.md';old=handoff.read_text(encoding='utf-8')
old+='''
## Ordinary Continue milestone — supersedes pending notes above
Session34137 completed engine0:79775checks0fail/24fresh disk restores/7200future
ticks,895.7s;84targeted inputs and2931owner files unchanged. All4boards/72source-native
pairs reviewed; continue-review-evidence.json records hashes/scope. Candidate-only
injection, prescribed paused-world context, no normal/Title/new-process admission.
30fpsfixture initial terminal parse failure (duplicate started local) retained in
motion output interval-before archive. Generator renamed local motion_started;
production/source untouched. Corrected run session83958 is live; output:
output/veld-sofa-partial-south-motion-v1. Poll83958, do not restart on timeout.
Motion wrappers freeze84inputs; do not modify them mid-run. Native1176frames/all24
cases and subsequent decoded lossless playback review pending. Goal active.
New competing East source/HANDOFF:character/veld-seated-east-master-v1; earlier
staged East pair remains baseline. No generated art admitted as current master.
'''
handoff.write_text(old,encoding='utf-8')
print('24ordinaryworld Continue/7200ticks and72reviewedpairs recorded in5references+handoff')
