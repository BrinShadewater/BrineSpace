from pathlib import Path
import hashlib,json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
inputs=json.loads((p/'inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==h for k,h in inputs['preCallSha256'].items())
job=json.loads((p/'generation.json').read_bytes());assert job['status']=='Success' and job['task_id']=='448180480450899'
path=p/'raw-review/review.json';review=json.loads(path.read_bytes())
assert hashlib.sha256((p/'source.mp4').read_bytes()).hexdigest()==review['sourceSha256']
review.update(visualReviewPending=False,sourceAcceptance=False,disposition='rejected',reviewedPages=review['pages'],endpointSamplesReviewed=True,findings=['All142 raw frames inspected chronologically on six boards, plus actual endpoint samples.','Starts South, rotates toward East and through North, passes West, returns South, then reaches West again. Requested shortest quarter turn failed.','Visible foot lifts/strides and changing lower-body stance; purple backpack rectangle appears mid-spin.','Final128..141 moves South toward West but cannot be admitted alone: begins from changed stance/material after foot movement, very few transition frames, and complete canonical joins are unproven.','No extraction, helmet fitting, native playback, normal selection or owner acceptance.'])
path.write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
section='''### James matched carrying turn terminal review — October 2, 2026

Job448180480450899 is Success/downloaded, not Processing. All142 raw frames on
six chronological boards and endpoint samples inspected. New selected-head South/
West carrying references did not constrain the route: it turns toward East,
through North and West, returns South, then reaches West again. Foot lifts/stride
and an invented purple backpack rectangle remain. Source REJECTED; no extraction,
helmet/native/normal admission. Last128..141 South-to-West section is not a proved
usable bridge: altered stance/material and canonical joins still require review.
Frozen source/helper/prompt/closed source reviews and downloaded-video hash stable.

Lesson: matched endpoint identity and a terminal match do not prove the intervening
turn. Repeated whole-body full spins require a different source-authoring method,
not another unconstrained prompt retry. Next single authored45degree whole-body
midpoint from exact256 South/West carrying references, common standing148 ruler,
pivot128/224 and full-canvas margins; assess scale/feet/material before expansion.
No per-pose fitting, palette correction or anatomy warping to hide drift. Existing
normal cap/V9/riseV6/caseV7 remain selected. Full goal active/incomplete.
Evidence:character/james-master-cargo-turn-south-west-v2/raw-review/review.json;
new source work:character/james-carry-authored-midpoint-v1.
'''
def append(path,text):
    old=path.read_bytes()
    if text.splitlines()[0].encode() in old:return
    new=old+b'\n\n'+text.encode();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:append(path,section)
lesson='''James matched endpoint video448180480450899 terminal review:142frames/all six
chronology boards and actual endpoint samples inspected; rejected full spin,
foot lifting and purple backpack. Identity-aligned inputs do not ensure shortest
quarter path. Do not repeat uncontrolled whole-turn jobs after equivalent route
failures; move to explicitly authored intermediate whole-body poses. Final128..141
segment is not accepted without stance/material and exact cardinal join evidence.
Evidence:character/james-master-cargo-turn-south-west-v2/raw-review/review.json.
'''
for path in [r/'skills/brinespace-character-pipeline/references/direct-video.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/direct-video.md')]:append(path,lesson)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James matched cargo turn

## Objective and acceptance
Full master-matched James animations, then cross-family consistency/polish. Active/incomplete.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 remain selected. South/West carried prototypes provisional.
No per-pose height fitting/grade or reserved motion-transfer use.

## Current state
Job448180480450899 Success; source.mp4 and142frame review evidence retained.
All six chronology boards and endpoint samples reviewed; raw-review/review.json closed REJECTED.
No extraction, helmet/native/normal-bank or profile changes. Five guides and direct-video mirrors updated.

## Verification
Frozen generation inputs and video hash stable. Actual route spins through wrong
directions, lifts feet and invents a purple backpack patch. Terminal West reach
does not certify a valid shortest quarter turn. Late segment remains unaccepted.

## Next action
Single authored45degree whole-body carrying midpoint in james-carry-authored-midpoint-v1.
Check common master scale, feet, head and material before building paired motion.
Then full cardinal cargo joins, actual lifecycle/Continue and cross-family polish.
''',encoding='utf-8')
print('Terminal whole-video rejection closed; frozen inputs/video stable; five guides and two direct-video mirrors updated.')
