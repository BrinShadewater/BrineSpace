from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
job=json.loads((p/'generation.json').read_bytes());assert job['status']=='Success' and job['task_id']=='448162817507840'
path=p/'raw-review/review.json';review=json.loads(path.read_bytes());assert review['decodedFrames']==141
review.update(visualReviewPending=False,selected=False,sourceAcceptance=False,
 finding='All six chronological contact boards/141raw frames and two exact-endpoint join boards/ten whole+ten upper presentations inspected. Starts from actual carry-turn entry with coherent native-like material, but continues to full South/front orientation rather than slight West settle. Feet spread/rotate as whole body turns; purple chest/case markings invented. Early frames24..48 compared to actual exit: no accepted full endpoint join. Reject source as final bridge; no alpha extraction, helmet expansion or native admission.',
 next='Official first/last API supports MiniMax-Hailuo-02 at768P6s; estimatedUSD0.28. Add optional endpoint mode to maintained helper with offline payload/security/ledger checks, then prepare exact paired endpoint images before one bounded trial.',
 documentation='https://platform.minimax.io/docs/api-reference/video-generation-fl2v')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James continuous V2 source terminal review — October 2, 2026

Job448162817507840 completed Success; source.mp4 downloaded, no live job. All six
chronological boards/141 decoded24fps768square frames inspected plus two actual
endpoint join boards/ten whole and ten upper views at common1/3 canvas scale.
Actual incoming carry source preserved initially, coherent familiar material;
clip overshoots slight West settle into full South/front turn, spreading/rotating
feet and inventing purple chest/case marks. Early24..48 source views compared to
actual unloadWest0 exit; no accepted full endpoint join. REJECTED before extraction,
paired helmet or native admission. Source/input/helper hashes retained, estimated
USD0.19, billing unverified. No owner-profile access or normal bank change.

Endpoint-targeted still revisions remain unaccepted; cap/V9/riseV6/caseV7 selected.
Official first/last-frame API checked: supports MiniMax-Hailuo-02,6s768P (estimated
USD0.28 from current paygo page);2.3Fast is not a documented first/last model.
https://platform.minimax.io/docs/api-reference/video-generation-fl2v
https://platform.minimax.io/docs/guides/pricing-paygo
Next add optional explicit end-image mode to maintained helper, preserving Fast
default and exclusive ledger/no paid retry/key redaction; validate payload offline.
Then freeze actual equal-size incoming/outgoing images for one endpoint-bound
trial. Do not resubmit terminal V2 job or claim prompt-only small-angle control.

Lesson: correct initial source does not constrain end orientation or equipment.
After the demonstrated overshoot, use explicit supported endpoint conditioning
rather than repeating prose constraints. Native playback cannot fix a failed
source. Five guides/handoff updated; full master/context/cross-family goal open.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James endpoint-targeted still');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James continuous West join V2

## Objective and acceptance
Full James master/style/perspective/size/height/proportion/matte set, then cross-
family polish. Incomplete; actual incoming AND outgoing source joins must match.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 unchanged. Preserve source/endpoint inputs, no pose
normalization. Reserved Higgsfield transfer untouched; existing generation scope.

## Current state
Two built-in endpoint-targeted still revisions in sibling midpoint folder reviewed
unaccepted. Here: source.mp4, exact master-input.png/exit-reference.png/prompt.txt,
input hashes, terminal generation.json,141frame raw boards/two join boards.
V2 job448162817507840 Success, source REJECTED; no live job or native replacement.
Five guides updated. No owner-profile writes, commit/export.

## Verification
All141raw frames and10whole/10upper endpoint samples inspected. Initial identity
and grade closer, but full front turn/boot movement/purple equipment marks fail.
Input/helper hashes unchanged. EstimatedUSD0.19, verified billing unknown.
Official first/last API supports Hailuo02,6s768P at estimatedUSD0.28; Fast2.3
not documented for that mode. Documentation URLs in raw-review/review.json.

## Next action
Add explicit optional end-image mode to maintained tools/minimax_video.py and
offline payload/ledger/security checks; retain existing Fast default. Freeze both
actual equal-size endpoints, then one endpoint-conditioned trial. Do not resubmit
terminal V2. All remaining contexts/cardinals/master/cross-family polish open.
Goal active/incomplete; no blocker.
''',encoding='utf-8')
print('Terminal V2 rejected after141frame review;input hashes unchanged;endpoint-conditioned next step documented in five guides/handoff.')
