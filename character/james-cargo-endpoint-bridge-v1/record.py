from pathlib import Path
import json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
path=p/'review.json';review=json.loads(path.read_bytes())
review.update(visualReviewPending=False,sourceAcceptance=False,
 finding='Raw1237x1271 four-pose atlas and six endpoint/intermediate whole views plus six upper crops inspected. Correct carry-to-unload semantic direction, but generated margins do not honor equal-cell root registration: right column shifted, lower row raised. First alpha32 ruler yields148px top poses vs152px lower poses; alpha bounds not anatomical proof. Face/hair and shoulder emblem drift; middle pair is a larger advance than first/last pair. REJECTED before helmet/native expansion. Cell-placement offsets are atlas layout failure, not proven animated foot sliding. Do not treat independent relocation as motion repair.')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James whole endpoint atlas source gate — October 2, 2026

Built-in imagegen four-intermediate coherent2x2 whole-pose atlas references actual
carry-turnEastWest010 and unloadWest0, uniformly4x. Exact prompt/pre-call endpoint
hashes retained unchanged; raw1237x1271 transparent source saved in workspace.
One first alpha32-height ruler/common offset diagnostic preserves all other pose
sizes/margins. Raw atlas and six whole endpoint/intermediate views/six upper crops
inspected: REJECTED. Correct action direction, but equal-cell root framing violated
(right-column shifted/lower-row raised), face/hair/emblem drift, disproportionate
middle advance. Top alpha bounds148 versus lower152 do not prove anatomical height.
Layout offsets are not proof of animated foot sliding. No per-pose fitting/grade,
helmet/native/normal admission or owner profile access. Normal selection unchanged.

Lesson: both real endpoints improve action semantics but cannot guarantee coherent
intermediate identity, spacing or anatomical scale. Separate atlas cell placement
from source motion before diagnosing sliding; a common first-figure ruler exposes
remaining scale differences but does not certify proportions. Reject source-level
failure before costly paired/native expansion. Next source needs consistent whole
identity and calibrated framing, then six-pose endpoint motion/master review.
Evidence: character/james-cargo-endpoint-bridge-v1/{raw.png,prompt.txt,inputs.json,
review.json,whole-head-review.png,review.py}. Five guides updated; full goal active.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James coherent cargo fixed-scale rejection');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff=r/'character/james-floor-case-west-v1/HANDOFF.md'
atomic(handoff,('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James cargo source gate

## Objective and acceptance
Full James set matching masters, camera, height/proportions and matte grade,
then cross-family polish. Incomplete; current normal V9/riseV6/caseV7 retained.

## Accepted decisions and constraints
Use actual whole carry/unload endpoints. No per-pose anatomical scale fitting,
independent head patches, owner profile access, commit or export.

## Current state
character/james-cargo-endpoint-bridge-v1 stores endpoint inputs/pre-call hashes,
exact prompt, built-in raw atlas, common-ruler diagnostic exports and source review.
Five guides updated. Earlier coherent-video study rejected for bridge replacement.

## Verification
Endpoint hashes unchanged. Raw atlas and six whole/six upper views inspected.
Action correct; framing, face/emblem identity, scale and middle advance fail.
Top/lower alpha heights148/152 are diagnostics; layout offsets not foot sliding.
No helmet/native expansion, normal selection change or full motion acceptance.
No live provider/native job. Prior normal save/title checks retain their revisions.

## Next action
Repair whole source identity/calibrated atlas framing with actual endpoints; review
all six poses before matched helmet and full native lifecycle/Continue. Other
cardinals/contexts/master and cross-family polish remain. Goal active, no blocker.
''').encode())
print('Source rejection recorded; five guides and concise handoff updated; normal bank unchanged.')
