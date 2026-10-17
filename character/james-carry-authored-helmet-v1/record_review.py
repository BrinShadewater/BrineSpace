from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def stable(data,key):
    assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in data[key].items())
native=json.loads((p/'native-review.json').read_bytes());assert native['checks']==709 and native['failures']==0 and native['profileUnchanged']
stable(json.loads((p/'native-inputs.json').read_bytes()),'preLaunchSha256')
native.update(visualReviewPending=False,sourceNativePairsReviewed=20,comparisonBoardsReviewed=4,findings=['All four chronological native/source boards inspected at148/82/54/27rulers. Fixed feet and source ordering retained in both gears/directions.','Independent software filtering is a comparison, not native RGB equivalence. Continuous cadence and actual crew cargo dispatch remain unverified.'])
(p/'native-review.json').write_text(json.dumps(native,indent=2)+'\n',encoding='utf-8')
review=json.loads((p/'review.json').read_bytes());stable(review,'sourceSha256')
review.update(visualReviewPending=False,disposition='provisional_paired_turn_join_mismatch',findings=['Whole/head/station chronological boards and all20native/source pairs reviewed. Helmet crown69/69/68/69/68; soles224. Equipment extends above148body ruler as standing master does.','All62992paired pixels outside53x48head/collar exact; no body fit, movement or regrade. Middle/late helmet angles remain similar and require cadence refinement.','Normal cargo comparison reveals West face/torso/case-placement mismatch, plus differing gait stance. South case/grip also differs. A matching full carrying family is needed before normal admission.'])
(p/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
for name in ['middle','early-v2','middle-v2','late-v2','endpoint']:
    f=p/(name+'-review.json');data=json.loads(f.read_bytes());data.update(visualReviewPending=False,sourceAcceptance=False,selected=False,disposition='rejected_undersized_helmet' if name=='middle' else 'provisional_source_frame_reviewed');f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
join=json.loads((p/'join-inputs.json').read_bytes());stable(join,'sourceSha256')
join.update(visualReviewPending=False,disposition='normal_cargo_family_mismatch',findings=['Four rows/sixteen normal source references inspected at common148ruler with pivot translation only. Candidate and idle match head family; West normal carry/unload face and torso differ and case placement changes.','South candidate case/grip differs from existing carry/unload. Gait foot lift is legitimate walking motion; do not flatten gait to repair a turn.','Literal last-loader source inventory is offline evidence, not live actor scheduling or continuous transition acceptance.'])
(p/'join-inputs.json').write_text(json.dumps(join,indent=2)+'\n',encoding='utf-8')
section='''### James paired carrying turn and cargo-family join audit — October 2, 2026

Candidate:character/james-carry-authored-helmet-v1. Actual selected shared helmet
standing South/West masters provide gear endpoints; three generated intermediate
heads preserve62992paired body pixels outside53x48head/collar. Starting with bare
head as edit target undersized the helmet: retain rejected middle source; using
correct-size helmet master as edit target restored crown69/69/68/69/68,sole224.
Equipment crown is naturally above148body ruler; never shrink shell to bare hair.
Both finite800ms forward/reverse candidates preserve same five carried bodies.

Standalone paired native709checks/0failures,168prescribed20ms samples,20post-draw
captures; all20source/native pairs onfour boards visually reviewed. Whole/head/
station source boards reviewed,20APNG decode checks passed. Prelaunch source,
manifest/player/helper hashes stable; scratchAPPDATA owner profile unchanged.
These checks do not prove continuously watched cadence, normal cargo dispatch,
room contact, interruptions, fresh Continue or owner/full-master acceptance.

Four static gear/direction join rows compare candidate with actual ordered literal
normal idle/carry first/last/unload first sources at fixed148ruler. West normal
carry/unload changes face/torso and case placement from candidate/master idle;
South case/grip also differs. Walking foot lift remains legitimate gait. New turn
alone cannot solve a mismatched cargo family. Middle/late helmet angle progression
also remains a cadence concern. Candidate unselected, sourceAcceptance false;
normal cap/V9/riseV6/caseV7 and save bindings unchanged.

Next rebuild West carrying gait from master-based cargo endpoint and then South,
match pickup/unload joins, refine helmet angles and review real motion/context
before versioned normal admission. Continue full cardinal/master/context coverage
and cross-family matte/proportion/tool polish. Full goal active/incomplete.
Handoff:character/james-carry-authored-helmet-v1/HANDOFF.md.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James carried head contours');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James paired cargo turn

## Objective and acceptance
Full master-matched James animation set then full cross-family polish. Incomplete.

## Accepted decisions and constraints
Keep fixed256canvas/p128224/148body ruler; helmet naturally extends above body.
No perpose fit/grade/mirroring; existing normal selections/save bindings preserved.

## Current state
Five paired source poses and two finite800ms manifests, APNG previews and source
boards. Three intermediate helmet v2 raw/prompt/input pairs; undersized middle v1
rejected. Exact62992outside-head/collar paired pixels. New audit_joins.py creates
normal-cargo-joins.png and frozen source inventory; record_review.py closes reports
and updates five guides. Candidate provisional/unselected/sourceAcceptance false.

## Verification
709/0standalone paired checks,168prescribed clock samples,20postdraw captures;
all20native/source pairs/four boards inspected. Source full/head/station review,
20APNG decode checks and LFS rasters/previews pass. Prelaunch inputs stable;
scratch owner profile unchanged. No normal actor/room/Continue or watched cadence.
Join comparison four rows/sixteen normal references reviewed: West face/torso/case
position changes; South case/grip differs. Middle/late helmet angles too similar.

## Next action
Rebuild West carrying gait around master-based cargo endpoint, then South and
matching pickup/unload transitions. Refine helmet angular progression; continuous
motion, room/interruptions/Continue and versioned admission. Finish all cardinals,
contexts and cross-family matte/proportion/tool polish; full goal remains active.

## Source provenance
Builtin middle v1 exec-bd45ac19-a5de-4ee2-85b1-1e7189d8d47e rejected;
middle v2 exec-74cd5e88-4c29-43a9-bc1b-75ef7b4b0ef7;
early v2 exec-4ebd8414-2b7a-4f78-a8c4-c48d6f716c99;
late v2 exec-b08e68f6-4f05-4512-948b-6f0029891c21.
Saved raw/prompt/input files retain respective middle, middle-v2, early-v2 and
late-v2 prefixes. Early/late v1 prompts prepared only, not submitted.
''',encoding='utf-8')
print('Paired source/native and static normal joins reviewed; five guides updated; full goal incomplete.')
