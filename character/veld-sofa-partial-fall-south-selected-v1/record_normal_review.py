from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
path=P/'normal-continue-review-evidence.json';e=json.loads(path.read_text(encoding='utf-8'))
for relative,digest in e['bindings'].items():assert hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,relative
assert e['validation']['passed'] and e['validation']['targetedInputCount']==86
e['reviewedBoards']=e['boards'];e['reviewedSourceNativePairs']=72
e['checks']=85500
e['visualReview']='All four normal-loader boards/72 source-native presentations inspected. Before/after restart retain pose, material, helmet and physical seat/floor contact in these prescribed cases. Normal integration accepted within fixture scope; no natural scheduler, all-clips continuous playback or final owner acceptance claim.'
path.write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
block='''## Veld normal South partial-fall continuation verified — October 2, 2026

Normal selected loader, without candidate injection, passes85500checks/0failures:
24actual world mortality cases,24ordinary RunSave disk/fresh-main restores and
7200reference/resumed future actor ticks. All six partial sit/rise entrances in
both gear variants; each fresh scene checks all72normal source slots/markers.
903.17seconds/engine0/cleanlog;86targeted inputs and2931owner non-log files unchanged
under scratch APPDATA. All four new normal Continue boards/72source-native pairs
reviewed: before/after retain pose, colour, shared shell and seat/floor contact.

Earlier staged native30fps evidence remains independently scoped:1176chronological
presentations reviewed,2400lossless decode checks pass. The normal Continue run
adds normal-loader evidence; it does not retroactively relabel the staged capture.
No art/controller/grade/scale change for this verification. Normal package status
may now be marked selected using descriptive-only metadata, retaining tested bytes.

Lesson: explicitly verify actual normal source selection across every fresh scene
and inspect native before/after contact. Living256x256 sources are review-padded
to256x272; padding is not a source resize or new registration. Same-clock pixel
checks and future state checks answer distinct resume failures. Do not equate this
controlled sofa fixture with natural chooser/traffic/hazards, Title/new-process
Continue or full-library visual acceptance. Those and directional/master polish
remain open; full goal active/incomplete. No commit/export.
Handoff:character/veld-sofa-partial-fall-south-selected-v1/HANDOFF.md.

'''
for dest in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
    old=dest.read_text(encoding='utf-8')
    if block.splitlines()[0] not in old:dest.write_text(block+old,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Normal South partial falls

## Objective and acceptance
Full master-consistent Veld set followed by full-library polish. This milestone
verifies normal paired partial South falls; full goal remains incomplete.

## Accepted decisions and constraints
Exact canonical sit/rise entrances and authored ground/neutral fall poses. H148,
256x272/p128224,180msincoming; early0/1floor340ms,late2–5floor780ms. Preserve
owner furnishings, source anatomy, grade and original staged evidence.

## Current state
Normal loader/registry selects six partial states pergear/72slots. New normal-only
fixture has no manifest injection. review_continue.py builds four native boards;
record_normal_review.py records verified evidence/status/pipeline/bible/skills.
Manifest descriptive status still selected_pending_normal_verification; normal
proof now complete within prescribed scope. No artwork/runtime metadata edits.

## Verification
Session54472 terminal0:85500checks0fail/24actualworld deaths/24ordinary disk-fresh
restores/7200futureticks/903.17s.86inputs/2931ownerfiles unchanged,cleanlog. All four
boards/72source-native presentations viewed; before/after pose/material/sharedshell/
contact retained. Normal-only source assertions also preserve older reader/bunk
paths. Candidate1176native30fps presentations/all24boards reviewed separately;
2400lossless decoded checks pass. No continuously watched all24clip claim.

## Next action
Preserve original tested manifest bytes before descriptive-only status promotion;
validate runtime metadata/source equality and refresh inventory with prior snapshot
retained. No extra runtime rerun needed for a descriptive-only field. Continue full
directional source polish/current natural eligibility and original-master comparison
of carry face/prone rear-hardware flags in coverage audit. Natural chooser/traffic/
hazards/Title/new-process and full-library final visual acceptance remain open.
Default loungeNorth/readSouth; do not invent side furniture to admit staged art.
No commit/export/full-goal completion.
''',encoding='utf-8')
print('Normal verification recorded: 85500 checks / 24 restores / 72 reviewed presentations')
