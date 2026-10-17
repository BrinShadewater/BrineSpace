from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
for name in ['inputs.json','grade-inputs.json','rephase-inputs.json','late-inputs.json']:
    inventory=json.loads((p/name).read_bytes())['preCallSha256']
    root=r if name=='inputs.json' else p
    assert all(hashlib.sha256((root/k).read_bytes()).hexdigest()==v for k,v in inventory.items()),name
inventory=json.loads((p/'alpha-inputs.json').read_bytes())
assert all(hashlib.sha256((p/k).read_bytes()).hexdigest()==v for k,v in inventory.items())
job=json.loads((p/'generation.json').read_bytes());assert job['status']=='Success' and job['task_id']=='448164885340650'
findings={
 'raw-review/review.json':'All142 raw frames reviewed on six chronology boards in prior source interval; final two boards rechecked now. Local crop avoids whole-body spin, but temporal purple material drift and failure to attain exact outgoing face angle remain. Source REJECTED for direct bridge admission; motion resource retained.',
 'grade-review.json':'Grade removes purple cast but deterministic white extraction leaves pale edge; whole/upper/original/station comparisons reviewed. White-key package REJECTED.',
 'alpha-review.json':'Generated alpha removes pale outline; all whole/upper/original/station comparisons reviewed. Head stays near profile through four selected phases28/56/84/112 then changes to exact outgoing three-quarter source. Face/patch brightening and one-pixel row3 crown rise remain. Full bridge REJECTED; no helmet/native/normal admission.',
 'late-review.json':'Raw1254alpha and all whole/upper/late-join/station boards inspected. Outgoing-target late source more closely retains terminal material and crown, but largely repeats outgoing orientation; new sequence shifts unresolved head/shoulder jump to row3->4. Isolated late pose retained provisionally as terminal-side reference, full sequence NOT accepted.'
}
for name,finding in findings.items():
    path=p/name;review=json.loads(path.read_bytes());review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,finding=finding)
    if name=='late-review.json':review['isolatedPoseDisposition']='Provisional reference only; insufficient angular progression for bridge acceptance'
    atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James upper-crop video, matte/alpha and late-angle source review — October 2, 2026

Exact80-square incoming/outgoing upper crops uniformly8x to640; one Hailuo02
first/last job448164885340650 completed Success.142raw24fps768square frames/all
six chronology boards reviewed, final two rechecked in closeout. Small upper
adjustment avoids earlier whole-body spin, but mid purple material drift and
terminal face-angle mismatch remain. Source conditioning is not proof the last
rendered frame matches supplied endpoint. No further video job/live process.
EstimatedUSD0.28,billing unverified; reserved transfer untouched.

Actual phases28/56/84/112 assembled into equal1280atlas; built-in grade edit
1254source removes purple but white-key package has pale outline. Built-in alpha
extraction removes that outline; whole/original/upper/82/54/27station-size views
reviewed. Four627cells->80 uniformly at original96/56 origin, no per-pose fit/
grade.61476original outside-region pixels exact per intermediate, first/last
exact. Six decoded APNG RGB/80ms holds pass; not continuous/native acceptance.
Alpha sequence REJECTED: head remains near-profile then jumps to outgoing pose;
face/patch brightening and one-pixel row3 crown rise remain.

Diagnostic rephase35/70/105/135 atlas frozen/reviewed, not sent for generation:
late raw still lacks final angle, so retiming cannot repair pose geometry.
One built-in outgoing-target late-pose edit exec-136a994d-fb80-43cc-adf0-547196dc4085,
1254genuinealpha retained. Raw and full/upper/join/station boards inspected;
uniform1254->80, original region/61476outside pixels and exact endpoints retained.
Head-region opaque180top76/76/76/75/76/76 is a crop diagnostic, not anatomy proof.
Another six decoded APNG RGB/80ms holds pass. New late source matches terminal
material/crown more closely but largely repeats terminal angle, moving the jump
to row3->4. Isolated source provisional reference; full bridge NOT accepted.

Normal helmet-cap/V9/riseV6/caseV7 selection unchanged. No helmet/native expansion,
Godot/profile/commit/export write. Exact prompts/raw sources/precalls/helper hashes
retained and verified; white-key failure retained. All four review records closed
with sourceAcceptance=false, not left pending. Full James goal incomplete.
Next author the missing middle upper angle between incoming and new terminal-side
pose, reviewing head/collar/shoulder progression and matte palette as a whole;
do not repeat video retiming or expand gear/runtime before source pass. Remaining
directions/contexts/master/cross-family polish still required.
Evidence:character/james-west-upper-video-v1/HANDOFF.md and *-review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James exact-endpoint video terminal source review');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
lesson='''
James upper first/last job448164885340650 avoids whole-body spin but final crop
still undershoots supplied terminal face angle; inspect actual final pixels, not
only configured input hashes. Picking later frames cannot create missing angular
progression. Grade/alpha edits can remove magenta and white halos yet leave pose
discontinuity or alter identity/patch detail. Preserve transparent generated alpha,
review exact full-body joins and source geometry separately from colour success.
Outgoing-target late edit can repeat final angle and merely move the jump earlier;
do not infer a solved bridge from one endpoint-side pose. Raw/grade/alpha/late trials
and verdicts:character/james-west-upper-video-v1. No normal admission.
'''
for path in [r/'skills/brinespace-character-pipeline/references/direct-video.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/direct-video.md')]:
    old=path.read_bytes()
    if b'James upper first/last job448164885340650' not in old:atomic(path,old+lesson.encode())
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James upper source repair

## Objective and acceptance
Full James animations matching masters/style/perspective/size/height/proportions/
matte grade, then whole-set/cross-family polish. Active and incomplete.

## Accepted decisions and constraints
Normal helmet-cap/V9/riseV6/caseV7 preserved. Source first/last conditioning, colour
success and decoded preview checks do not establish pose or motion acceptance.

## Current state
Here: exact upper references/prompts/hashes, terminal job448164885340650/source.mp4,
142raw chronology boards, grade/raw alpha atlases and whole-body source trials.
White-key and alpha bridge rejected. Rephase diagnostic not generated. New built-in
late-raw.png and late-prompt.txt retained; isolated late pose provisional reference,
whole sequence still rejected. Five guides/direct-video mirrors updated.

## Verification
All raw chronology previously inspected; final two rechecked. Grade/alpha whole,
upper, original and station-size boards reviewed. New late raw/full/upper/join/
station boards reviewed. Source/helper/prompts hashes unchanged.61476outside pixels
exact per changed frame, original endpoints exact; six APNG RGB/80ms checks each
alpha and late preview. Head top76/76/76/75/76/76 diagnostic. No native/helmet/
owner-profile writes or continuous motion acceptance. EstimatedvideoUSD0.28,
billing unknown. No live generation/process.

## Next action
Author a true middle head/collar/shoulder angle between incoming and terminal-side
reference; source palette/geometry across all phases must pass before helmet/native.
Retiming a source missing terminal angle will not solve it. Normal West integration
and other family selections remain; cardinals/contexts/full master consistency and
cross-family polish open. No blocker, no goal completion claim.

Built-in generation sources: grade exec-c9fbf66f-e7ca-4d6d-97bc-2e7952504676;
alpha exec-21b6c8c4-0d25-4d1b-bfbf-deab2c0cf38c;
late exec-136a994d-fb80-43cc-adf0-547196dc4085. Raw copies grade-raw.png,
alpha-raw.png,late-raw.png; prompts grade-prompt.txt,alpha-prompt.txt,late-prompt.txt.
''',encoding='utf-8')
print('Four source reviews closed; frozen inputs intact; five guides/direct-video mirrors and handoff updated. Goal incomplete.')
