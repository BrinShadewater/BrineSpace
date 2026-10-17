from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
inputs=json.loads((p/'inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
path=p/'review.json';review=json.loads(path.read_bytes());review.update(visualReviewPending=False,sourceAcceptance=False,
 finding='Raw joint2x2 source and twelve whole/twelve enlarged upper presentations inspected. Source framing differs by row: diagnostic crowns148,146,146,148,148,149 versus original148,148,148,149,149,149. Larger/warmer face rendering and altered badge geometry; temporal upper articulation still clusters into two similar-pose pairs instead of four small advances. REJECTED before matched helmet/native expansion.61476original pixels protected each, case/hands/lowerbodyfeet and exact endpoints unchanged. Registration/identity/temporal source failure; pixel protection is not acceptance.')
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''### James joint upper-atlas source gate — October 2, 2026

Built-in imagegen edits four actual V9 upper intermediates jointly in2x2 atlas,
using real carry-turn010/unloadWest0 upper endpoints and original80square crop at
96/56 enlarged8x. Raw1254/exact prompt/pre-call hashes retained; all input/source
hashes unchanged. Common80/627cell reduction/original crop origin, no translation,
grade or per-pose fit. Rect10464..162134 admitted only;61476original pixels exact
per trial, lowerbody/case/hands/feet and whole first/last endpoints unchanged.

Raw and twelve whole/twelve upper views inspected: REJECTED. Crowns diagnostic
148,146,146,148,148,149 versus148,148,148,149,149,149; inconsistent row placement,
larger/warmer face and altered badge geometry. Upper articulation remains grouped
in two similar-pose pairs rather than four small advances. No paired helmet/native
expansion or normal override. Cap fix remains selected; shared West join unresolved.

Lesson: joint generation avoids independent-call seams but still does not prove
uniform framing, master identity or progressive articulation. Judge every cell
against BOTH whole endpoints before native work, not merely relative to each other.
Protected lowerbody pixels and a coherent-looking atlas do not rescue source head
drift. Next compare accepted near-West angular sources against exact endpoints
before choosing a missing intermediate or another source repair; avoid repeated
broad face redesign or pose normalization. Five guides updated; full goal active/
incomplete. Evidence: character/james-upper-bridge-atlas-v1/review.json,prompt.txt,
inputs.json,raw.png,whole-upper-review.png and HANDOFF.md. No owner-profile access.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James normal turn dispatch and West walking join');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James shared West join

## Objective and acceptance
Full James set matching masters/style/perspective/height/proportions/matte grade,
then cross-family polish. Incomplete. Cap selected; normal V9 join unchanged.

## Accepted decisions and constraints
Use actual carry-turn010/unloadWest0 endpoints. Protect lowerbody/case/feet.
No per-pose normalization or new identity; source failure precedes native work.

## Current state
character/james-upper-bridge-atlas-v1 stores exact original4crop atlas/endpoints,
pre-call hashes/prompt/built-in1254raw/common-cell package/12whole+12upper review.
Candidate REJECTED, no selected source replaced. Five guides updated.

## Verification
Input hashes unchanged;61476outside-region pixels exact per intermediate, endpoints
exact. Raw/all24presentations inspected. Inconsistent row crown/face/badge and
two-pair motion grouping fail source gate. No helmet/native expansion. Previous
normal dispatch2151/0/46paired views stays valid; no runtime change this turn.
No owner profile access, live job, commit or export; full goal not accepted.

## Next action
Compare accepted near-West angular sources to exact incoming/outgoing master
identity before choosing/authoring a genuinely missing upper pose. Repair shared
source join then verify work-return and turn/settle/walk lifecycles separately.
Other cardinals/contexts/master/material/proportion/cross-family polish remain.
Goal active/incomplete, no blocker.
'''
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Joint source rejected; raw/prompt/pre-call hashes retained; five guides/handoff updated; normal artwork unchanged.')
