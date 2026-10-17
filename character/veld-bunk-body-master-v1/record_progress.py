from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-body-master-v1'
result=json.loads((O/'validation.json').read_text());assert result['passed'] and not result['realProfileChanges']
note='''## Veld complete master-body bunk candidate — October 1, 2026

character/veld-bunk-body-master-v1 replaces the obsolete specialised East bunk
body with complete authored poses referenced to the selected contemporary idle.
One148/408 source ruler and pooled master material grade; exact native standing
entry for both gears. Blue boxed science patch, cream instruments, specimen rack,
brown bun, warm skin and matte charcoal suit retained. Canvas256x272 adds hanging
leg padding while original pivot128,224 and standing148 remain. Original seven
pose entry/reverse exit/held clocks and furniture/depth metadata retained. Upright
canonical helmet plus existing authored reclining components fitted to new head
landmarks; calibrated bare-to-equipped master face offset preserves neck attachment.
20RGBA exports, paired four states/36 references; no normal selection changes.

12source,16helmet and94package checks0failures. Native1306checks0failures/78.02s,
engine0:112 prescribed lowering/rising samples in actual four habitation rotations
and both gears;8actual held-sleep deaths,32actor-file fresh dead restores at same
world clock and56invalid recipe guards. Scratch APPDATA,2931real non-log owner
files unchanged. Initial51.34s failed interval retained: relaxed authored glove
sat1native pixel below support plane. Bounded complete arm insert translated up1,
preserving head/body/legs; strict exact bounds guard retained and passes. No
production script changes this milestone. Five native boards and paired source
board visually reviewed;6source-clock GIFs at one-third speed are not continuous
native gameplay footage. No full RunSave/fresh-scene Continue, natural approach,
partial-transition death or full lifecycle proof. Owner acceptance remains open.

Lesson: compare whole body with selected master using common anatomical ruler,
not equal image boxes. Additional transparent padding preserves complete hanging
limbs without shrinking stature. Helmet fidelity does not cure obsolete body art.
Register authored arm relaxation to actual support rather than weakening a failed
contact guard. Same-source actor restores are narrower than complete Continue.
Next full-scene Continue/approach/interruptions and partial/seated death sources,
then normal selection and cross-family/full-set polish. Full goal remains active.
Handoff/review/evidence: character/veld-bunk-body-master-v1.
'''
handoff='''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld complete bunk body

## Objective and acceptance
Full Veld animation set matching selected masters; this milestone repairs obsolete
specialised East bunk body, then pairs helmet and checks actual bed presentation.

## Accepted decisions and constraints
Exact contemporary idle entry, one anatomical ruler, matte master palette and
equipment. Preserve accepted choreographic clocks, bed geometry and contact.
Reversible staged candidate; no commit, export or normal-loader selection.

## Current state
New sources/builders/paired manifests/20frames and review in this folder.
tests/test_veld_bunk_body_master.gd plus UID and isolated runner under tools.
Bounded relaxed arm now translated upward1pixel to original support plane.
Other source pixels unchanged by repair; source result and prompt preserved.

## Verification
12source/16helmet/94package checks and1306native checks pass;78.02seconds,
engine0.112 prescribed live samples,8held deaths,32actor-file fresh dead restores;
all4actual habitation rotations/both gears.2931owner files unchanged. Five native
boards and paired source reviewed. Failed51.34s interval retained separately.
Source-clock GIFs are review media; natural approach/full-scene Continue/partial
death coverage and normal selection not certified. Evidence contains after-run
bindings, not interval-frozen proof. Owner visual acceptance remains open.

## Next action
Actual disk RunSave/fresh-scene Continue at lowering/held/rising and held death,
paired staged-loader admission; then natural approach/interruptions and partial
life death sources, normal integration and complete cross-family master polish.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,p in enumerate(paths):
    old=p.read_bytes()
    if note.splitlines()[0].encode() not in old:
        payload=note.replace('\n','\r\n').encode('utf-8')
        p.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
files=list((P/'frames').rglob('*.png'))+[P/n for n in ['build_bare.py','build_helmet.py','bare-manifest.json','helmet-manifest.json','bare-registration.json','helmet-registration.json','package-checks.json','material-grade.json','sources/bunk-body-v1.png','sources/prompt-v1.txt','HANDOFF.md']]+[R/'tests/test_veld_bunk_body_master.gd',R/'tests/test_veld_bunk_body_master.gd.uid',R/'tools/run_veld_bunk_body_master.py',O/'validation.json',O/'native.log',O/'records.json']
(P/'evidence.json').write_text(json.dumps({'native':result,'checks':1306,'normalSelection':False,'visualReview':'five native boards and paired source inspected; owner acceptance pending','bindingsAfterRun':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'prescribed native clocks/actor-file restores; not full-scene Continue or natural approach'},indent=2)+'\n')
print('Handoff, after-run evidence and five milestone records saved')
