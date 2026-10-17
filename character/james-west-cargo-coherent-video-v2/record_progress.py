from pathlib import Path
import hashlib,json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];still=r/'character/james-west-upper-midpoint-v1'
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
path=still/'v2-review.json';review=json.loads(path.read_bytes())
review.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
 finding='Two V2 raw sources, five whole/five upper comparisons and15station-size presentations inspected. Endpoint-targeted revisions improve shoulder/badge resemblance relative to V1, but all three authored head/collar orientations still cluster; incoming-to-first step remains visibly abrupt. No final progressive source acceptance. Midpoint remains provisional; no helmet/native expansion or normal selection.')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
job=json.loads((p/'generation.json').read_bytes())
section='''### James endpoint-targeted still review and continuous source trial — October 2, 2026

Early/late V2 built-in edits use actual incoming/outgoing upper endpoints as edit
targets, midpoint as support. Raw1254 sources/exact prompts/frozen inputs preserved
in james-west-upper-midpoint-v1. Common80/1254 crop reduction, original origin,
61476 outside pixels exact each. Two raws, five whole/five upper comparison views
and15station-size presentations inspected. Shoulder/badge resemblance improved,
but authored head/collar poses still cluster and incoming join remains abrupt.
No accepted progressive bank, helmet/native expansion or normal source changes.

Next bounded source approach is one continuous MiniMax direct motion from actual
carry-turnEastWest010, rather than V1 video's wrong unloadWest0 starting pose.
New james-west-cargo-coherent-video-v2 uses exact256canvas4x white input, no grade,
translation or pose fit. Small coherent profile-to-three-quarter settle with feet
planted, then hold; source must independently match actual exit endpoint. Exact
prompt/input/helper hashes frozen; one exclusive job448162817507840, last verified
Preparing,6s768P Fast2.3. EstimatedUSD0.19, billing unverified; official pricing
rechecked https://platform.minimax.io/docs/guides/pricing-paygo. Never resubmit
this ledger. Reserved Higgsfield motion-transfer run untouched. No profile access.

Lesson: even changing edit targets can produce similar static portraits rather
than temporal articulation. Stop expanding a stalled still sequence; continuous
authoring must begin at the actual outgoing runtime source, and its ending still
needs independent identity/contact/pose proof. Five guides/handoff updated. Full
James/master/context/cross-family goal remains incomplete; cap/V9/riseV6/caseV7
still selected. Next poll this same task, then inspect every raw frame before
extraction, equipment pairing or any runtime replacement.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James single midpoint and adjacent');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
(p/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James continuous West join V2

## Objective and acceptance
Full James master/style/camera/size/height/proportion/matte set, then cross-family
polish. Incomplete. Continuous candidate must match BOTH actual runtime endpoints.

## Accepted decisions and constraints
Normal cap/V9/riseV6/caseV7 unchanged; no source accepted from technical tests.
Use established direct MiniMax route; reserved Higgsfield transfer untouched.

## Current state
Adjacent still V2 reviewed/unaccepted in sibling james-west-upper-midpoint-v1:
early-v2-raw.png,late-v2-raw.png,early-v2-prompt.txt,late-v2-prompt.txt,v2-review.json.
Here: exact incoming carry master-input.png,exit-reference.png,prompt.txt,input
hashes and exclusive generation.json. One job448162817507840, verified Preparing.

## Verification
Still raw/five whole/five upper/15station-size presentations inspected.61476
outside pixels exact; shoulder resembles endpoints better but orientations cluster.
New video input/helper hashes frozen, actual incoming source exact before4x white
composition. EstimatedUSD0.19, official rate rechecked; billing unverified.
No source clip/native/owner-profile work yet; no normal selection changed.

## Next action
Poll SAME job448162817507840 using maintained helper; do not submit again. On
success inspect all raw decoded frames, actual entry/exit identity and foot contact
before fixed extraction or helmet/native expansion. Other directions/contexts and
full master/cross-family polish remain. Goal active, no blocker, no commit/export.
''',encoding='utf-8')
print('Still V2 verdict and continuous trial ledger recorded;five guides/handoff updated.')
